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

## Class methods

### merge

## Properties

### is_empty

## Instance methods

### SkewHeap

## put

## take

## peek

## adopt

## items

## drain

## See also

* [Skew heap on Wikipedia](https://en.wikipedia.org/wiki/Skew_heap)
