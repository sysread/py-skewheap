def merge_nodes(a, b):
    if a is None:
        return b

    if b is None:
        return a

    if a[0] > b[0]:
        a, b = b, a

    return a[0], merge_nodes(b, a[2]), a[1]

def pop_node(root):
    item, left, right = root
    return item, merge_nodes(left, right)

def explain_node_str(root, indent=0):
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
    def __init__(self):
        self.size = 0
        self.root = None

    def __repr__(self):
        buf = f"SkewHeap<size={self.size}>:\n"

        if self.root is not None:
            buf += explain_node_str(self.root, 1)

        return buf

    @property
    def is_empty(self):
        return self.size == 0

    def put(self, *args):
        for item in args:
            self.root = merge_nodes(self.root, (item, None, None))
            self.size = self.size + 1

        return self.size

    def take(self):
        if self.is_empty:
            return None

        self.size = self.size - 1
        item, self.root = pop_node(self.root)

        return item

    def peek(self):
        if self.is_empty:
            return None

        return self.root[0]

    def items(self):
        while not self.is_empty:
            yield self.take()
