import unittest
import random

from skewheap import SkewHeap


class TestSkewHeap(unittest.TestCase):
    def test_initial_state(self):
        s = SkewHeap()
        self.assertTrue(s.is_empty)
        self.assertIsNone(s.peek())
        self.assertIsNone(s.take())

    def test_put(self):
        s = SkewHeap()

        s.put(10)
        self.assertFalse(s.is_empty)
        self.assertEqual(s.peek(), 10)
        self.assertEqual(s.size, 1)

        s.put(5)
        self.assertFalse(s.is_empty)
        self.assertEqual(s.size, 2)
        self.assertEqual(s.peek(), 5)

        s.put(4, 2)
        self.assertFalse(s.is_empty)
        self.assertEqual(s.peek(), 2)
        self.assertEqual(s.size, 4)

    def test_take(self):
        s = SkewHeap()
        s.put(5, 8, 1, 3, 2, 13)
        self.assertEqual(s.size, 6)

        self.assertEqual(s.take(), 1)
        self.assertEqual(s.size, 5)

        self.assertEqual(s.take(), 2)
        self.assertEqual(s.size, 4)

        self.assertEqual(s.take(), 3)
        self.assertEqual(s.size, 3)

        self.assertEqual(s.take(), 5)
        self.assertEqual(s.size, 2)

        self.assertEqual(s.take(), 8)
        self.assertEqual(s.size, 1)

        self.assertEqual(s.take(), 13)
        self.assertEqual(s.size, 0)
        self.assertTrue(s.is_empty)

    def test_merge(self):
        a = SkewHeap()
        b = SkewHeap()

        a.put(1, 2, 3)
        b.put(4, 5, 6)

        c = SkewHeap.merge(a, b)
        self.assertEqual(c.drain(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(a.drain(), [1, 2, 3])
        self.assertEqual(b.drain(), [4, 5, 6])

    def test_adopt(self):
        a = SkewHeap()
        b = SkewHeap()

        a.put(1, 2, 3)
        b.put(4, 5, 6)

        a.adopt(b)
        self.assertEqual(a.drain(), [1, 2, 3, 4, 5, 6])
        self.assertEqual(b.drain(), [4, 5, 6])

    def test_items(self):
        s = SkewHeap()
        s.put(5, 8, 1, 3, 2, 13)

        items = s.items()
        self.assertEqual(list(items), [1, 2, 3, 5, 8, 13])


if __name__ == '__main__':
    unittest.main()
