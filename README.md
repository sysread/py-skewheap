# skewheap

## Synopsis

    from skewheap import SkewHeap

    s = SkewHeap()

    # Insert a bunch of items
    for i in big_random_number_list:
      s.put(i)

    # Drain the heap
    items = s.items()
    for i in items:
      print(i)

    # Drain the heap manually
    while not s.is_empty:
      print(s.take())

    # Merge heaps (non-destructively)
    new_heap = SkewHeap.merge(a, b, c)

    # Merge heaps into an existing heap
    s.adopt(a, b, c)

## Description

A skew heap is a min heap or priority queue which ammortizes the cost of
rebalancing using an elegant merge algorithm. All operations on a skew heap are
defined in terms of the merge algorithm.

An interesting side effect of this is that skew heaps can be quickly and easily
merged non-destructively.

Items added to the heap will be returned in order from lowest to highest.  To
control the ordering, implement `__gt__` on the class of the items being
inserted.

## Installation

write me

## SkewHeap

### Class methods

#### merge

Non-destructively merges multiple skew heaps together. The new heap will
contain all of the items in each of the heaps passed in, in order. Any number
of heaps may be merged together.

  a = SkewHeap()
  b = SkewHeap()
  c = SkewHeap()

  d = SkewHeap.merge(a, b, c)

### Properties

#### is_empty

`True` when there are no elements in the queue.

### Instance methods

#### SkewHeap

Creates a new, empty skew heap.

  s = SkewHeap()

#### put

Adds any number of items to the queue.

  s.put("some message")
  s.put(1, 2, 3)
  s.put(Task())

#### take

Removes the top element from the queue. Returns `None` if the queue is empty.


  item = s.take()

#### peek

Returns the top element from the queue without removing it. Returns `None` if
the queue is empty.

  item = s.peek()

#### adopt

Merges other heaps into this one. The other heaps are left intact.

  s.merge(heap_x, heap_y, heap_z)

#### items

Returns a generator that yields each element from the queue in turn.

  items = s.items()
  for item in items:
    do_stuff_with(item)

#### drain

Removes and returns all items from the queue as a list.

  all_items = s.drain()

## AsyncSkewHeap

### Properties

#### is_empty

`True` when there are no items in the heap and a call to `take()` would block.

#### is_shutdown

`True` after `shutdown()` has been called. When a queue has been shut down, all
waiters to `take()` will be awoken and `None` will be returned to them. New items
may be added to the heap, and _will_ be returned by `take()`, but the queue will
no longer block when no items are available.

### Instance methods

#### shutdown

Shuts down the queue. See the notes in `is_shutdown` regarding the behavior of
shutdown queues.

#### async join

Blocks until the heap is shut down.

#### async take

Blocks until an item is available on the queue and returns it.

#### put

Adds any number of elements to the queue.

#### adopt

Merges other queues into this one (either `SkewHeap` or `AsyncSkewHeap`). The
other queues are left intact.


## FAQ

#### How do I change the ordering of items in the queue?

## See also

* [Skew heap on Wikipedia](https://en.wikipedia.org/wiki/Skew_heap)
