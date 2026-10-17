"""
Module 01: Modern System Design & Microservices
Production Artifact: Stateless Ingress & Idempotent Event Dispatcher
Demonstrates:
  - 12-factor stateless application architecture
  - Atomic idempotency locking using Redis Sentinel/Cluster
  - Asynchronous event bus dispatch decoupling compute from storage
  - Graceful connection pooling and resource lifecycles
"""

from contextlib import asynccontextmanager
from typing import Annotated
import asyncio
import json
import uuid

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
import redis.asyncio as aioredis


class OrderItem(BaseModel):
    sku: str = Field(..., pattern=r"^[A-Z0-9_-]+$", description="Stock Keeping Unit")
    quantity: int = Field(..., gt=0, le=100, description="Quantity to purchase")
    price_cents: int = Field(..., gt=0, description="Price per unit in cents")


class CreateOrderRequest(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=64)
    items: list[OrderItem] = Field(..., min_length=1, max_length=20)
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")


class OrderEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order_id: str
    idempotency_key: str
    user_id: str
    total_cents: int
    status: str = "PENDING_PAYMENT"


class AsyncEventPublisher:
    """Simulates an asynchronous event bus publisher (Kafka / Redpanda / NATS)."""

    def __init__(self, broker_url: str):
        self.broker_url = broker_url
        self._connected = False

    async def connect(self) -> None:
        await asyncio.sleep(0.01)  # Simulated TCP handshake
        self._connected = True

    async def publish(self, topic: str, event: OrderEvent) -> None:
        if not self._connected:
            raise RuntimeError("Event bus broker is disconnected")
        # In production: KafkaProducer.send_and_wait(topic, event.model_dump_json().encode())
        await asyncio.sleep(0.02)
        print(f"[EVENT-BUS] Published event {event.event_id} to topic '{topic}'")

    async def disconnect(self) -> None:
        self._connected = False


# Shared state dependencies managed by Lifespan
redis_pool: aioredis.Redis | None = None
event_publisher: AsyncEventPublisher | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_pool, event_publisher
    # Initialize connection pool to distributed cache (Redis)
    redis_pool = aioredis.from_url(
        "redis://localhost:6379",
        encoding="utf-8",
        decode_responses=True,
        max_connections=50,
    )
    event_publisher = AsyncEventPublisher(broker_url="kafka.platform.internal:9092")
    await event_publisher.connect()

    yield

    # Clean shutdown of shared data plane sockets
    if redis_pool:
        await redis_pool.aclose()
    if event_publisher:
        await event_publisher.disconnect()


app = FastAPI(
    title="Order Ingress Microservice",
    description="Stateless, idempotent API gateway entry point for e-commerce transactions.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.post(
    "/v1/orders",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=dict,
)
async def create_order(
    payload: CreateOrderRequest,
    idempotency_key: Annotated[
        str,
        Header(
            alias="X-Idempotency-Key",
            description="Unique UUID client token for at-most-once execution",
        ),
    ],
):
    if not redis_pool or not event_publisher:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Platform dependencies are not yet initialized",
        )

    lock_key = f"idempotency:lock:{idempotency_key}"
    result_key = f"idempotency:result:{idempotency_key}"

    # 1. Check if previous execution already recorded a final response
    cached_response = await redis_pool.get(result_key)
    if cached_response:
        print(f"[IDEMPOTENCY] Cache hit for key {idempotency_key}. Returning saved response.")
        return json.loads(cached_response)

    # 2. Acquire atomic distributed lock with 60s TTL
    lock_acquired = await redis_pool.set(
        name=lock_key,
        value="IN_FLIGHT",
        nx=True,
        ex=60,
    )
    if not lock_acquired:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A request with this idempotency key is currently being processed",
        )

    try:
        total_cents = sum(item.price_cents * item.quantity for item in payload.items)
        order_id = f"ord-{uuid.uuid4().hex[:12]}"

        # 3. Construct event and dispatch to message broker asynchronously
        event = OrderEvent(
            order_id=order_id,
            idempotency_key=idempotency_key,
            user_id=payload.user_id,
            total_cents=total_cents,
        )
        await event_publisher.publish(topic="order-events", event=event)

        response_body = {
            "order_id": order_id,
            "status": "Accepted",
            "total_cents": total_cents,
            "currency": payload.currency,
            "idempotency_key": idempotency_key,
        }

        # 4. Store completed result with 24-hour retention
        await redis_pool.set(
            name=result_key,
            value=json.dumps(response_body),
            ex=86400,
        )
        return response_body

    finally:
        # 5. Release processing lock
        await redis_pool.delete(lock_key)
