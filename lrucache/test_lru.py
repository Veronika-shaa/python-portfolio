import unittest
from lru import LRUCache


class TestCustomMeta(unittest.TestCase):

    def test_set_and_get(self):
        cache = LRUCache(2)

        cache.set("k1", "val1")
        cache.set("k2", "val2")

        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "val1")

        # перезапись одного из ключей
        cache.set("k1", "new_val1")

        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k1"), "new_val1")

    def test_limit(self):
        # лимит равен 0
        cache_0 = LRUCache(0)

        cache_0.set("k1", "val1")

        self.assertEqual(cache_0.get("k1"), None)

        # лимит равен 1
        cache_1 = LRUCache(1)

        cache_1.set("k1", "val1")
        self.assertEqual(cache_1.get("k1"), "val1")

        cache_1.set("k2", "val2")
        self.assertEqual(cache_1.get("k1"), None)
        self.assertEqual(cache_1.get("k2"), "val2")

    def test_get_unset_key(self):
        cache = LRUCache(2)

        self.assertEqual(cache.get("k1"), None)

    def test_del_first_el(self):
        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        cache.set("k4", "val4")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k4"), "val4")

    def test_del_middle_el(self):
        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        cache.get("k1")
        cache.get("k3")

        cache.set("k4", "val4")

        self.assertEqual(cache.get("k2"), None)
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k3"), "val3")
        self.assertEqual(cache.get("k4"), "val4")

    def test_del_last_el(self):
        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        cache.get("k1")
        cache.get("k2")

        cache.set("k4", "val4")

        self.assertEqual(cache.get("k3"), None)
        self.assertEqual(cache.get("k1"), "val1")
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k4"), "val4")

    def test_reset(self):
        cache = LRUCache(3)

        cache.set("k1", "val1")
        cache.set("k2", "val2")
        cache.set("k3", "val3")

        cache.get("k1")
        cache.get("k2")
        cache.set("k3", "new_val3")

        cache.set("k4", "val4")

        self.assertEqual(cache.get("k1"), None)
        self.assertEqual(cache.get("k2"), "val2")
        self.assertEqual(cache.get("k3"), "new_val3")
        self.assertEqual(cache.get("k4"), "val4")
