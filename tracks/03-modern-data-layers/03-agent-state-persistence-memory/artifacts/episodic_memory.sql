-- ============================================================================
-- Enterprise Agent Episodic Memory & Temporal Decay Retrieval
-- Demonstrates: PostgreSQL + pgvector schema, HNSW cosine index, and stored procedure
--               implementing Ebbinghaus-inspired temporal decay and importance weighting.
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS vector;

-- 1. Agent Episodic Memory Persistence Table
CREATE TABLE IF NOT EXISTS agent_episodic_memories (
    memory_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_id VARCHAR(64) NOT NULL,
    session_id VARCHAR(64) NOT NULL,
    entity_id VARCHAR(128),
    -- Natural language assertion or reflection extracted from conversation
    memory_content TEXT NOT NULL,
    -- Importance weight evaluated by reflection model [1 = trivial, 10 = critical architectural rule]
    importance_weight SMALLINT NOT NULL CHECK (importance_weight BETWEEN 1 AND 10),
    -- 1536-dimensional L2-normalized embedding vector
    embedding vector(1536) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_accessed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. Performance Indexes
CREATE INDEX IF NOT EXISTS idx_agent_memories_agent_time 
ON agent_episodic_memories (agent_id, created_at DESC);

-- HNSW Vector Index for Semantic Proximity Search
CREATE INDEX IF NOT EXISTS idx_agent_memories_hnsw_cosine 
ON agent_episodic_memories 
USING hnsw (embedding vector_cosine_ops)
WITH (m = 16, ef_construction = 64);

-- 3. Stored Procedure: Hybrid Vector Distance + Exponential Temporal Decay
-- Formula: Score = 0.60 * CosineSim + 0.25 * exp(-lambda * delta_t_minutes) + 0.15 * (importance / 10)
CREATE OR REPLACE FUNCTION retrieve_agent_memories(
    p_agent_id VARCHAR(64),
    p_query_embedding vector(1536),
    p_lambda FLOAT DEFAULT 0.0001, -- Exponential decay factor per elapsed minute
    p_top_k INT DEFAULT 5
)
RETURNS TABLE (
    memory_id UUID,
    memory_content TEXT,
    similarity_score FLOAT,
    temporal_score FLOAT,
    importance_score FLOAT,
    combined_score FLOAT
) AS $$
BEGIN
    RETURN QUERY
    WITH candidate_pool AS (
        -- Step 1: Over-fetch nearest semantic candidates using HNSW index
        SELECT 
            m.memory_id,
            m.memory_content,
            (1.0 - (m.embedding <=> p_query_embedding))::FLOAT AS sim,
            EXP(-p_lambda * (EXTRACT(EPOCH FROM (NOW() - m.created_at)) / 60.0))::FLOAT AS decay,
            (m.importance_weight / 10.0)::FLOAT AS imp
        FROM agent_episodic_memories m
        WHERE m.agent_id = p_agent_id
        ORDER BY m.embedding <=> p_query_embedding
        LIMIT (p_top_k * 4)
    )
    -- Step 2: Re-rank candidates using weighted multi-objective scoring
    SELECT 
        c.memory_id,
        c.memory_content,
        c.sim,
        c.decay,
        c.imp,
        (0.60 * c.sim + 0.25 * c.decay + 0.15 * c.imp)::FLOAT AS combined_score
    FROM candidate_pool c
    ORDER BY combined_score DESC
    LIMIT p_top_k;
END;
$$ LANGUAGE plpgsql;
