#!/usr/bin/env python3
"""
artifacts/iceberg_ops.py
Production Apache Iceberg Operations Engine using PySpark.

Demonstrates:
1. REST Catalog and S3 FileIO Configuration.
2. Bit-for-bit Deterministic Time Travel Querying for ML Training Sets.
3. Asynchronous Bin-Pack File Compaction and Positional Delete Reconciliation.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os


@dataclass(frozen=True)
class LakehouseCatalogConfig:
    catalog_name: str = "lakehouse"
    catalog_type: str = "rest"
    catalog_uri: str = "http://iceberg-catalog.internal:8181"
    s3_endpoint: str = "https://s3.us-east-1.amazonaws.com"
    warehouse_path: str = "s3://enterprise-lakehouse-curated/warehouse"


class IcebergLakehouseManager:
    """Manages transactional table reads, time-travel snapshots, and compaction."""

    def __init__(self, config: Optional[LakehouseCatalogConfig] = None):
        self.config = config or LakehouseCatalogConfig()

    def build_spark_session(self) -> Any:
        """
        Builds a SparkSession configured with Iceberg SQL extensions and S3 FileIO.
        Returns SparkSession if PySpark is installed, otherwise prints configuration.
        """
        try:
            from pyspark.sql import SparkSession
            builder = (
                SparkSession.builder
                .appName("EnterpriseIcebergLakehouseManager")
                .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions")
                .config(f"spark.sql.catalog.{self.config.catalog_name}", "org.apache.iceberg.spark.SparkCatalog")
                .config(f"spark.sql.catalog.{self.config.catalog_name}.type", self.config.catalog_type)
                .config(f"spark.sql.catalog.{self.config.catalog_name}.uri", self.config.catalog_uri)
                .config(f"spark.sql.catalog.{self.config.catalog_name}.warehouse", self.config.warehouse_path)
                .config(f"spark.sql.catalog.{self.config.catalog_name}.io-impl", "org.apache.iceberg.aws.s3.S3FileIO")
            )
            return builder.getOrCreate()
        except ImportError:
            print("[INFO] PySpark not installed in local environment. Returning declarative execution plan.")
            return None

    def query_training_snapshot(
        self,
        table_identifier: str,
        snapshot_id: int
    ) -> str:
        """
        Generates the deterministic Time-Travel query targeting an exact snapshot.
        Guarantees that distributed PySpark workers read identical immutable data files.
        """
        sql_query = f"""
        SELECT 
            record_id,
            dataset_version,
            modality,
            token_count,
            embedding_vector,
            feature_payload_uri
        FROM {self.config.catalog_name}.{table_identifier} 
        /*+ OPTIONS('snapshot-id'='{snapshot_id}') */
        WHERE modality IN ('text', 'image')
        ORDER BY record_id;
        """
        return sql_query.strip()

    def run_binpack_compaction(
        self,
        spark: Any,
        table_identifier: str,
        target_file_size_bytes: int = 134217728  # 128 MB
    ) -> Optional[Any]:
        """
        Calls Iceberg's system rewrite_data_files procedure.
        Compacts small fragmented Parquet files and merges positional deletes into clean columnar blocks.
        """
        compaction_call = f"""
        CALL {self.config.catalog_name}.system.rewrite_data_files(
            table => '{self.config.catalog_name}.{table_identifier}',
            strategy => 'binpack',
            options => map(
                'target-file-size-bytes', '{target_file_size_bytes}',
                'min-file-size-bytes', '{target_file_size_bytes // 2}',
                'max-file-group-size-bytes', '{target_file_size_bytes * 8}'
            )
        )
        """
        print(f"[EXECUTING COMPACTION]\n{compaction_call.strip()}\n")
        if spark is not None:
            return spark.sql(compaction_call)
        return None


def main():
    manager = IcebergLakehouseManager()
    table = "ai_platform.multimodal_training_features"
    sample_snapshot = 789410294819041289

    print("--- 1. Iceberg Time Travel Query (ML Reproducibility) ---")
    query = manager.query_training_snapshot(table, snapshot_id=sample_snapshot)
    print(query)

    print("\n--- 2. Iceberg Asynchronous Binpack Compaction ---")
    manager.run_binpack_compaction(spark=None, table_identifier=table)


if __name__ == "__main__":
    main()
