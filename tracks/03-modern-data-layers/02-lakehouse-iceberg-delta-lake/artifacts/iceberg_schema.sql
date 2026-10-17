-- ============================================================================
-- Enterprise Apache Iceberg Table DDL & Schema Evolution
-- Demonstrates: Hidden daily partitioning, Merge-on-Read (MoR), Zstandard Parquet,
--               and snapshot retention policies for AI training workloads.
-- ============================================================================

-- 1. Create Curated AI Multimodal Training Features Table
CREATE TABLE IF NOT EXISTS lakehouse.ai_platform.multimodal_training_features (
    record_id STRING NOT NULL COMMENT 'Unique UUID idempotency key per training sample',
    dataset_version STRING NOT NULL COMMENT 'SemVer tag of the training dataset',
    tenant_id STRING NOT NULL COMMENT 'Organization tenant identifier',
    modality STRING NOT NULL COMMENT 'Input data modality: text | image | audio | multimodal',
    token_count INT COMMENT 'Pre-calculated token count for sequence pack budgeting',
    -- Dense embedding array for multi-vector retrieval or pre-computed feature representations
    embedding_vector ARRAY<FLOAT> COMMENT '1536-dimensional L2-normalized feature vector',
    feature_payload_uri STRING NOT NULL COMMENT 'Object store URI to raw asset (s3://bucket/assets/...)',
    metadata MAP<STRING, STRING> COMMENT 'Arbitrary key-value metadata tags and labels',
    ingestion_timestamp TIMESTAMP NOT NULL COMMENT 'UTC ingestion wall-clock time',
    -- Event partition column (used by hidden partition transform)
    event_date DATE NOT NULL COMMENT 'Derived calendar date of the event'
)
USING iceberg
-- Hidden Partitioning: Users query WHERE event_date = '2026-10-18'; 
-- Iceberg automatically maps to the daily partition without path leaks.
PARTITIONED BY (days(event_date), modality)
TBLPROPERTIES (
    -- Columnar Storage Format & Compression
    'write.format.default' = 'parquet',
    'write.parquet.compression-codec' = 'zstd',
    'write.parquet.compression-level' = '7',
    
    -- Merge-on-Read (MoR): Writes small positional delete files instead of rewriting Parquet blocks
    'write.delete.mode' = 'merge-on-read',
    'write.update.mode' = 'merge-on-read',
    'write.merge.mode'  = 'merge-on-read',
    
    -- Target File Sizing: Eliminates the small file problem by aiming for 128MB Parquet chunks
    'write.target-file-size-bytes' = '134217728',
    
    -- Snapshot Retention: Preserve 14 days of snapshots for deterministic ML training rollbacks
    'history.expire.max-snapshot-age-ms' = '1209600000',
    'history.expire.min-snapshots-to-keep' = '10'
);

-- 2. Schema Evolution without Rewriting Parquet Files (Metadata-Only Operation)
-- Add a new column for reinforcement learning preference scoring
ALTER TABLE lakehouse.ai_platform.multimodal_training_features 
ADD COLUMN IF NOT EXISTS rlhf_score DOUBLE COMMENT 'Human preference alignment score [-1.0, 1.0]';

-- 3. Partition Evolution: Modify partition granularity seamlessly
-- Example: As dataset scales, sub-partition high-volume modalities by tenant
-- Iceberg handles existing data under the old spec and new data under the new spec concurrently.
ALTER TABLE lakehouse.ai_platform.multimodal_training_features 
SET IDENTIFIER FIELDS record_id;

-- 4. Sample Maintenance: Expire Old Snapshots beyond SLA retention
-- Keeps metadata manifest trees lean and fast for query planning
CALL lakehouse.system.expire_snapshots(
    table => 'lakehouse.ai_platform.multimodal_training_features',
    older_than => TIMESTAMP '2026-10-04 00:00:00.000',
    retain_last => 10
);
