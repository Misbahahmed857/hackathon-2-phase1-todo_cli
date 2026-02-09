# Data Model for Phase 1 In-Memory Application

## Overview
This document defines the core data structures and relationships for the in-memory application.

## Core Entities

### 1. InMemoryRecord
The primary entity for storing data in memory.

```typescript
interface InMemoryRecord {
  id: string;              // Unique identifier for the record
  key: string;             // Primary key for lookup operations
  value: any;              // The actual data stored
  createdAt: Date;         // Timestamp when the record was created
  updatedAt: Date;         // Timestamp when the record was last updated
  ttl?: number;            // Optional time-to-live in seconds
  metadata?: Record<string, any>; // Additional metadata about the record
}
```

### 2. InMemoryStore
The main container for managing records in memory.

```typescript
interface InMemoryStore {
  records: Map<string, InMemoryRecord>;  // Collection of records
  maxSize?: number;                      // Optional maximum size limit
  evictionPolicy?: EvictionPolicy;       // Policy for removing records when max size reached
  statistics: StoreStatistics;           // Runtime statistics
}
```

### 3. EvictionPolicy
Defines how records are removed when storage limits are reached.

```typescript
enum EvictionPolicy {
  LRU = "LRU",           // Least Recently Used
  FIFO = "FIFO",         // First In, First Out
  TTL = "TTL",           // Time To Live
  CUSTOM = "CUSTOM"      // Custom policy
}
```

### 4. StoreStatistics
Runtime metrics for monitoring store performance.

```typescript
interface StoreStatistics {
  totalRecords: number;        // Total number of records currently stored
  hitCount: number;            // Number of successful lookups
  missCount: number;           // Number of unsuccessful lookups
  evictionCount: number;       // Number of records evicted
  memoryUsage: number;         // Approximate memory usage in bytes
  timestamp: Date;             // When statistics were captured
}
```

## Relationships
- One `InMemoryStore` contains many `InMemoryRecord` instances
- Each `InMemoryRecord` belongs to exactly one `InMemoryStore`
- `EvictionPolicy` is referenced by `InMemoryStore` to determine removal strategy
- `StoreStatistics` is maintained by `InMemoryStore` for observability

## Operations
The data model supports the following core operations:
- CREATE: Add new records to the store
- READ: Retrieve records by key
- UPDATE: Modify existing records
- DELETE: Remove records from the store
- LIST: Enumerate records with optional filters
- STATS: Retrieve store statistics

## Constraints
- Record keys must be unique within a store
- Record IDs should follow UUID format for global uniqueness
- TTL values must be positive integers when specified
- Metadata size should be limited to prevent excessive memory consumption