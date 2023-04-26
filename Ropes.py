maxLeafSize = 5
minLeafSize = 1
class Node:
    def __init__(self, value):
        self.value = value
        self.weight = len(value)
        self.left = None
        self.right = None

class Rope:
    
    def __init__(self, s, minLeafSize=1, maxLeafSize=5):
        self.root = Node(s)
        self.minLeafSize = minLeafSize
        self.maxLeafSize = maxLeafSize
        
    def search(self, node, pattern, start=0):
        if node.left is None and node.right is None:
            print(pattern)
            print(node.value)
            index = node.value.find(pattern, start)
            if index != -1:
                index += start
            return index
        if pattern < node.value:
            print('x')
            return self.search(node.left, pattern, start)
        else:
            return self.search(node.right, pattern[len(node.left.value):], start + len(node.left.value))

    def insert(self, node, s, i):
        if node.left is None and node.right is None:
            node.value = node.value[:i] + s + node.value[i:]
            node.weight = len(node.value)
            if node.weight > self.maxLeafSize:
                self.split(node)
        elif i <= node.left.weight:
            self.insert(node.left, s, i)
            node.weight += len(s)
            if node.left.weight > self.maxLeafSize:
                self.split(node.left)
        else:
            self.insert(node.right, s, i - node.left.weight)
            node.weight += len(s)
            if node.right.weight > self.maxLeafSize:
                self.split(node.right)

    def delete(self, node, i, j):
        if node.left is None and node.right is None:
            node.value = node.value[:i] + node.value[j:]
            node.weight = len(node.value)
            if node.weight < self.minLeafSize:
                self.merge(node)
        elif i < node.left.weight and j <= node.left.weight:
            self.delete(node.left, i, j)
            node.weight -= (j - i)
            if node.right is not None and node.right.weight < self.minLeafSize:
                self.merge(node.right)
        elif i >= node.left.weight and j > node.left.weight:
            self.delete(node.right, i - node.left.weight, j - node.left.weight)
            node.weight -= (j - i)
            if node.left is not None and node.left.weight < self.minLeafSize:
                self.merge(node.left)
        else:
            self.delete(node.left, i, node.left.weight)
            self.delete(node.right, 0, j - node.left.weight)
            node.value = node.left.value + node.right.value
            node.weight = len(node.value)
            if node.left.weight < self.minLeafSize:
                self.merge(node.left)
            elif node.right.weight < self.minLeafSize:
                self.merge(node.right)

    def replace(self, node, pattern, replace_with):
        indices = []
        index = self.search(node, pattern)
        while index != -1:
            indices.append(index)
            index = self.search(node, pattern, index + 1)
        for i in reversed(indices):
            self.delete(node, i, i + len(pattern))
            self.insert(node, replace_with, i)

    def split(self, node):
        if node.left is None and node.right is None:
            return
        mid = node.weight // 2
        left = Node(node.value[:mid])
        right = Node(node.value[mid:])
        node.left = left
        node.right = right
        node.value = None
        node.weight = None

    def merge(self, node):
        if node.left is None and node.right is None:
            return
        node.value = node.left.value + node.right.value
        node.weight = len(node.value)
        node.left = None
        node.right = None


rope = Rope("Hello, world!")

# print(rope.index(0))  # H
print(rope.root.weight)

print(rope.search(rope.root, "l"))
rope.replace(rope.root, "Hello", "Hi")

print(rope.root.weight)
print(rope.search(rope.root, "l"))

rope.insert(rope.root, "Kumail ", 4)

print(rope.root.weight)
rope.insert(rope.root, " How are you?", 17)

print(rope.search(rope.root, "l"))