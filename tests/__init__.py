import unittest
import asyncio
import random

from skewheap import SkewHeap, AsyncSkewHeap


class TestSkewHeap(unittest.IsolatedAsyncioTestCase):
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
        c = SkewHeap()

        a.put(1, 2, 3)
        b.put(4, 5, 6)
        c.put(7, 8, 9)

        d = SkewHeap.merge(a, b, c)
        self.assertEqual(a.drain(), [1, 2, 3])
        self.assertEqual(b.drain(), [4, 5, 6])
        self.assertEqual(c.drain(), [7, 8, 9])
        self.assertEqual(d.drain(), [1, 2, 3, 4, 5, 6, 7, 8, 9])

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

        expected = [1, 2, 3, 5, 8, 13]
        for item in items:
            self.assertEqual(item, expected.pop(0))

    async def test_async(self):
        count = 10
        s = AsyncSkewHeap()

        # Test initial state
        self.assertTrue(s.is_empty)

        # Test reading entries from the queue asynchronously
        async def reader():
            for i in range(0, count):
               item = await s.take()
               self.assertEqual(item, i)

        items = list(range(0, count))
        random.shuffle(items)
        s.put(*items)
        self.assertFalse(s.is_empty)

        await reader()
        self.assertTrue(s.is_empty)

    async def test_async_stop_join(self):
        s = AsyncSkewHeap()

        # Test initial state
        self.assertFalse(s.is_stopped)

        # Test stopping heap asynchronously with an active coro waiting to join
        async def stop_heap():
            await asyncio.sleep(0.1)
            s.stop()

        await asyncio.wait_for(
            asyncio.gather(s.join(), stop_heap()),
            timeout=2,
        )

        self.assertTrue(s.is_stopped)

        next_item = await asyncio.wait_for(s.take(), timeout=0.1)
        self.assertIsNone(next_item)


if __name__ == '__main__':
    unittest.main()
