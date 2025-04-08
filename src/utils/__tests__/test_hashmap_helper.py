import unittest
from src.utils.hashmap_helper import HashMap

class TestHashMap(unittest.TestCase):
    def setUp(self):
        self.hashmap = HashMap()

    def test_add_element(self):
        self.hashmap.add("key1", "value1")
        self.assertEqual(self.hashmap.size, 1)
        self.assertEqual(self.hashmap.get("key1"), "value1")

    def test_add_duplicate_key(self):
        self.hashmap.add("key1", "value1")
        self.hashmap.add("key1", "value2")
        self.assertEqual(self.hashmap.size, 1)
        self.assertEqual(self.hashmap.get("key1"), "value1")

    def test_remove_element(self):
        self.hashmap.add("key1", "value1")
        self.hashmap.remove("key1")
        self.assertEqual(self.hashmap.size, 0)
        self.assertIsNone(self.hashmap.get("key1"))

    def test_remove_nonexistent_key(self):
        self.hashmap.remove("nonexistent")
        self.assertEqual(self.hashmap.size, 0)

    def test_get_element(self):
        self.hashmap.add("key1", "value1")
        self.assertEqual(self.hashmap.get("key1"), "value1")

    def test_get_nonexistent_key(self):
        self.assertIsNone(self.hashmap.get("nonexistent"))

    def test_to_list(self):
        self.hashmap.add("key1", "value1")
        self.hashmap.add("key2", "value2")
        self.hashmap.add("key3", "value3")
        expected_list = ["value1", "value2", "value3"]
        self.assertEqual(sorted(self.hashmap.to_list()), sorted(expected_list))

    def test_size_property(self):
        self.assertEqual(self.hashmap.size, 0)
        self.hashmap.add("key1", "value1")
        self.assertEqual(self.hashmap.size, 1)
        self.hashmap.add("key2", "value2")
        self.assertEqual(self.hashmap.size, 2)
        self.hashmap.remove("key1")
        self.assertEqual(self.hashmap.size, 1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
