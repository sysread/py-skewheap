import asyncio


def merge_nodes(a, b):
    """Recursively and non-destructively merges two nodes. Returns the newly
    created node.
    """
    if a is None:
        return b

    if b is None:
        return a

    if a[0] > b[0]:
        a, b = b, a

    return a[0], merge_nodes(b, a[2]), a[1]

def pop_node(root):
    """Removes the top element from the root of the tree. Returns the element
    and the merged subtrees.
    """
    item, left, right = root
    return item, merge_nodes(left, right)

def explain_node_str(root, indent=0):
    """Returns an indendeted outline-style representation of the subtree.
    """
    indent_string = "    " * indent

    buf = f"{indent_string}Node<item={root[0]}>"

    if not root[1] and not root[2]:
        buf += "\n"
    else:
        buf += ":\n"

    if root[1]:
        buf += f"{indent_string} -Left:\n"
        buf += explain_node_str(root[1], indent + 1)

    if root[2]:
        buf += f"{indent_string} -Right:\n"
        buf += explain_node_str(root[2], indent + 1)

    return buf



class SkewHeap:
    """A skew heap is a min heap or priority queue which ammortizes the cost of
    rebalancing using an elegant merge algorithm. All operations on a skew heap
    are defined in terms of the merge algorithm.

    An interesting side effect of this is that skew heaps can be quickly and
    easily merged non-destructively.

    Items added to the heap will be returned in order from lowest to highest.
    To control the ordering, implement __gt__ on the class of the items being
    inserted.
    """
    def __init__(self):
        self.size = 0
        self.root = None

    def __repr__(self):
        buf = f"SkewHeap<size={self.size}>:\n"

        if self.root is None:
            buf += "    (Empty)"
        else:
            buf += explain_node_str(self.root, 1)

        return buf

    def __str__(self):
        return self.__repr__()

    @classmethod
    def merge(cls, *heaps):
        """Non-destructively merges *heaps into a single, new heap. Returns the
        new heap.

            newheap = SkewHeap.merge(a, b, c, ...)
        """
        c = SkewHeap()

        for h in heaps:
            c.size += h.size
            c.root = merge_nodes(c.root, h.root)

        return c

    @property
    def is_empty(self):
        """Returns True if there are no elements in the heap.
        """
        return self.size == 0

    def put(self, *args):
        """Adds one or more new elements to the heap. Returns the heap's new
        size.
        """
        for item in args:
            self.root = merge_nodes(self.root, [item, None, None])
            self.size = self.size + 1

        return self.size

    def take(self):
        """Removes and returns the top element from the heap. Returns None
        if the heap is empty.
        """
        if self.is_empty:
            return None

        self.size = self.size - 1
        item, self.root = pop_node(self.root)

        return item

    def peek(self):
        """Returns the top element from the heap without removing it. Returns
        None if the heap is empty.
        """
        if self.is_empty:
            return None

        return self.root[0]

    def adopt(self, *heaps):
        """Merges the elements from additional heaps into this one. The other
        heaps are left intact.
        """
        for h in heaps:
            self.size += h.size
            self.root = merge_nodes(self.root, h.root)

        return self.size

    def items(self):
        """Returns a generator of elements in the heap.
        """
        while not self.is_empty:
            yield self.take()

    def drain(self):
        """Removes and returns all elements from the heap as a list.
        """
        items = []

        while not self.is_empty:
            items.append(self.take())

        return items



class AsyncSkewHeap:
    def __init__(self):
        super().__init__()
        self.heap = SkewHeap()
        self.ev = asyncio.Event()
        self.sem = asyncio.Semaphore(0)

    @property
    def is_empty(self):
        return self.heap.is_empty

    @property
    def is_stopped(self):
        return self.ev.is_set()

    def stop(self):
        self.ev.set()

    async def join(self):
        if not self.is_stopped:
            await self.ev.wait()

    async def take(self):
        if self.is_stopped:
            return self.heap.take()

        async with self.sem:
            return self.heap.take()

    def put(self, *args):
        for item in args:
            self.heap.put(item)

            if not self.is_stopped:
                self.sem.release()

    def adopt(self, *heaps):
        prev_size = self.heap.size
        self.heap.adopt(*heaps)
        for _ in range(0, self.heap.size - prev_size):
            self.sem.release()

