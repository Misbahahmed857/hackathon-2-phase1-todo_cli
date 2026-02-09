"""
InMemoryStore for the Phase I In-Memory Python Console App.

This module implements an in-memory storage system with basic CRUD operations.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import sys
from enum import Enum
from src.models.task import Task


class EvictionPolicy(Enum):
    """Defines how records are removed when storage limits are reached."""
    LRU = "LRU"  # Least Recently Used
    FIFO = "FIFO"  # First In, First Out
    TTL = "TTL"  # Time To Live
    CUSTOM = "CUSTOM"  # Custom policy


class StoreStatistics:
    """Runtime metrics for monitoring store performance."""

    def __init__(self):
        self.total_records: int = 0
        self.hit_count: int = 0
        self.miss_count: int = 0
        self.eviction_count: int = 0
        self.memory_usage: int = 0
        self.timestamp: datetime = datetime.now()


class InMemoryStore:
    """The main container for managing records in memory."""

    def __init__(self, max_size: Optional[int] = None, eviction_policy: Optional[EvictionPolicy] = None):
        """
        Initialize the in-memory store.

        Args:
            max_size: Optional maximum size limit for the store
            eviction_policy: Optional policy for removing records when max size reached
        """
        self.records: Dict[str, Task] = {}
        self.insertion_order: List[str] = []  # Track insertion order for FIFO eviction
        self.max_size: Optional[int] = max_size
        self.eviction_policy: EvictionPolicy = eviction_policy or EvictionPolicy.FIFO
        self.statistics: StoreStatistics = StoreStatistics()

    def create(self, key: str, value: Task) -> bool:
        """
        Add a new record to the store.

        Args:
            key: The key for the record
            value: The Task object to store

        Returns:
            True if the record was created, False if it already existed
        """
        if key in self.records:
            return False

        self.records[key] = value
        self.insertion_order.append(key)  # Track insertion order for FIFO
        self.statistics.total_records += 1

        # Check if we need to evict records due to size limit
        if self.max_size and len(self.records) > self.max_size:
            self._evict_if_needed()

        self._update_memory_usage()
        return True

    def read(self, key: str) -> Optional[Task]:
        """
        Retrieve a record from the store by key.

        Args:
            key: The key of the record to retrieve

        Returns:
            The Task object if found, None otherwise
        """
        if key in self.records:
            self.statistics.hit_count += 1
            return self.records[key]
        else:
            self.statistics.miss_count += 1
            return None

    def update(self, key: str, value: Task) -> bool:
        """
        Update an existing record in the store.

        Args:
            key: The key of the record to update
            value: The new Task object

        Returns:
            True if the record was updated, False if it didn't exist
        """
        if key in self.records:
            self.records[key] = value
            self._update_memory_usage()
            return True
        return False

    def delete(self, key: str) -> bool:
        """
        Remove a record from the store.

        Args:
            key: The key of the record to remove

        Returns:
            True if the record was deleted, False if it didn't exist
        """
        if key in self.records:
            del self.records[key]
            # Remove from insertion order list if it exists
            if key in self.insertion_order:
                self.insertion_order.remove(key)
            self.statistics.total_records -= 1
            self._update_memory_usage()
            return True
        return False

    def list(self) -> List[Task]:
        """
        Retrieve all records from the store.

        Returns:
            A list of all Task objects in the store
        """
        return list(self.records.values())

    def get_statistics(self) -> StoreStatistics:
        """
        Get store statistics.

        Returns:
            StoreStatistics object with current metrics
        """
        self.statistics.timestamp = datetime.now()
        self._update_memory_usage()
        return self.statistics

    def _evict_if_needed(self) -> None:
        """Evict records if the store has exceeded its maximum size."""
        if not self.max_size or len(self.records) <= self.max_size:
            return

        # Calculate how many records to evict
        excess_count = len(self.records) - self.max_size

        # Apply eviction policy
        if self.eviction_policy == EvictionPolicy.FIFO:
            # Remove the oldest entries based on insertion order
            keys_to_remove = self.insertion_order[:excess_count]
            for key in keys_to_remove:
                if key in self.records:
                    del self.records[key]
                    self.insertion_order.remove(key)  # Remove from insertion order
                    self.statistics.eviction_count += 1
                    self.statistics.total_records -= 1
        elif self.eviction_policy == EvictionPolicy.LRU:
            # For now, just remove oldest entries (would need access time tracking for true LRU)
            keys_to_remove = self.insertion_order[:excess_count]
            for key in keys_to_remove:
                if key in self.records:
                    del self.records[key]
                    self.insertion_order.remove(key)  # Remove from insertion order
                    self.statistics.eviction_count += 1
                    self.statistics.total_records -= 1
        elif self.eviction_policy == EvictionPolicy.TTL:
            # For now, just remove oldest entries (would need TTL tracking for true TTL)
            keys_to_remove = self.insertion_order[:excess_count]
            for key in keys_to_remove:
                if key in self.records:
                    del self.records[key]
                    self.insertion_order.remove(key)  # Remove from insertion order
                    self.statistics.eviction_count += 1
                    self.statistics.total_records -= 1

    def _update_memory_usage(self) -> None:
        """Update the memory usage statistic."""
        # This is a simplified approximation of memory usage
        try:
            self.statistics.memory_usage = sys.getsizeof(self.records)
        except:
            # If sys.getsizeof fails, set to a default value
            self.statistics.memory_usage = len(self.records) * 1024  # 1KB per record estimate