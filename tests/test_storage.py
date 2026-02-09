"""
Unit tests for the InMemoryStore in the Phase I In-Memory Python Console App.
"""

import unittest
from src.storage.in_memory_store import InMemoryStore, EvictionPolicy, StoreStatistics
from src.models.task import Task


class TestInMemoryStore(unittest.TestCase):
    """Test cases for the InMemoryStore."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.store = InMemoryStore()

    def test_initialization(self):
        """Test that the store is initialized correctly."""
        self.assertEqual(len(self.store.records), 0)
        self.assertIsNone(self.store.max_size)
        self.assertEqual(self.store.eviction_policy, EvictionPolicy.FIFO)
        self.assertIsInstance(self.store.statistics, StoreStatistics)

    def test_create_record(self):
        """Test creating a record in the store."""
        task = Task("Test task")
        key = "test-key"
        result = self.store.create(key, task)

        self.assertTrue(result)
        self.assertIn(key, self.store.records)
        self.assertEqual(self.store.records[key], task)

    def test_create_duplicate_key(self):
        """Test creating a record with a duplicate key."""
        task1 = Task("Test task 1")
        task2 = Task("Test task 2")
        key = "test-key"

        # First creation should succeed
        result1 = self.store.create(key, task1)
        self.assertTrue(result1)

        # Second creation with same key should fail
        result2 = self.store.create(key, task2)
        self.assertFalse(result2)

        # Record should still be the first task
        self.assertEqual(self.store.records[key], task1)

    def test_read_existing_record(self):
        """Test reading an existing record."""
        task = Task("Test task")
        key = "test-key"
        self.store.create(key, task)

        retrieved_task = self.store.read(key)
        self.assertEqual(retrieved_task, task)

    def test_read_nonexistent_record(self):
        """Test reading a nonexistent record."""
        retrieved_task = self.store.read("nonexistent-key")
        self.assertIsNone(retrieved_task)

    def test_update_existing_record(self):
        """Test updating an existing record."""
        original_task = Task("Original task")
        updated_task = Task("Updated task")
        key = "test-key"

        # Create the original task
        self.store.create(key, original_task)
        self.assertEqual(self.store.records[key], original_task)

        # Update the task
        result = self.store.update(key, updated_task)
        self.assertTrue(result)
        self.assertEqual(self.store.records[key], updated_task)

    def test_update_nonexistent_record(self):
        """Test updating a nonexistent record."""
        task = Task("Test task")
        result = self.store.update("nonexistent-key", task)
        self.assertFalse(result)

    def test_delete_existing_record(self):
        """Test deleting an existing record."""
        task = Task("Test task")
        key = "test-key"
        self.store.create(key, task)

        result = self.store.delete(key)
        self.assertTrue(result)
        self.assertNotIn(key, self.store.records)

    def test_delete_nonexistent_record(self):
        """Test deleting a nonexistent record."""
        result = self.store.delete("nonexistent-key")
        self.assertFalse(result)

    def test_list_records(self):
        """Test listing all records."""
        task1 = Task("Task 1")
        task2 = Task("Task 2")

        self.store.create("key1", task1)
        self.store.create("key2", task2)

        records_list = self.store.list()
        self.assertEqual(len(records_list), 2)
        self.assertIn(task1, records_list)
        self.assertIn(task2, records_list)

    def test_empty_list(self):
        """Test listing records when the store is empty."""
        records_list = self.store.list()
        self.assertEqual(len(records_list), 0)
        self.assertEqual(records_list, [])

    def test_get_statistics(self):
        """Test getting store statistics."""
        stats = self.store.get_statistics()
        self.assertIsInstance(stats, StoreStatistics)
        self.assertEqual(stats.total_records, 0)

    def test_store_with_max_size_no_eviction_needed(self):
        """Test store with max size but no eviction needed."""
        store = InMemoryStore(max_size=2)
        task1 = Task("Task 1")
        task2 = Task("Task 2")

        result1 = store.create("key1", task1)
        result2 = store.create("key2", task2)

        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertEqual(len(store.records), 2)

    def test_store_with_max_size_triggers_eviction_fifo(self):
        """Test store with max size triggers FIFO eviction."""
        store = InMemoryStore(max_size=2, eviction_policy=EvictionPolicy.FIFO)
        task1 = Task("Task 1")
        task2 = Task("Task 2")
        task3 = Task("Task 3")

        store.create("key1", task1)
        store.create("key2", task2)
        store.create("key3", task3)  # This should trigger eviction

        # With FIFO policy and max size of 2, the oldest entry should be evicted
        # In our implementation, when size is exceeded, oldest entries are removed
        # We expect to have task2 and task3, but not task1
        self.assertNotIn("key1", store.records)  # Oldest should be gone
        self.assertIn("key2", store.records)     # Should still be there
        self.assertIn("key3", store.records)     # Newest should be there
        self.assertEqual(len(store.records), 2)

    def test_statistics_tracking(self):
        """Test that statistics are properly tracked."""
        task = Task("Test task")

        # Initially zero records
        initial_stats = self.store.get_statistics()
        self.assertEqual(initial_stats.total_records, 0)

        # After creating a record
        self.store.create("key1", task)
        stats_after_create = self.store.get_statistics()
        self.assertEqual(stats_after_create.total_records, 1)

        # After deleting a record
        self.store.delete("key1")
        stats_after_delete = self.store.get_statistics()
        self.assertEqual(stats_after_delete.total_records, 0)


if __name__ == '__main__':
    unittest.main()