# Maximum and minimum characters a leaf node can store
maxLeafChars = 5
minLeafChars = 1


class Node:
    # Constructor for a Single Node i.e: Single Letter
    def __init__(self, value):
        self.value = value
        self.size = len(value)
        self.left = None
        self.right = None


class Rope:
    # Constructor for the Rope Class
    def __init__(self, s, minLeafChars=1, maxLeafChars=5):
        self.root = Node(s) # The root node of the rope is initialized with the input string
        self.minLeafChars = minLeafChars 
        self.maxLeafChars = maxLeafChars 

    def __repr__(self):
        return self._repr(self.root)

    def _repr(self, node):
        # Recursively creates a string representation of the rope using parentheses and commas
        # If the node is a leaf, the string representation is just the node's value enclosed in quotes
        # If the node is not a leaf, the string representation is a tuple of the string representations of its left and right children
        if node.left is None and node.right is None:
            return "Rope('{}')".format(node.value)
        else:
            return '({}, {})'.format(self._repr(node.left), self._repr(node.right))

    # Search for a pattern in the rope starting from the given node and position
    # Returns the index of the first occurrence of the pattern, or -1 if not found
    # This is implemented using recursion and a method similar to binary search
    def search(self, node, pattern, start=0):
        if node.left is None and node.right is None:
            # If the node is a leaf, search for the pattern in its value
            index = node.value.find(pattern, start)
            if index != -1:
                index += start
            return index
        if pattern < node.value:
            # If the pattern is in the left child's value
            return self.search(node.left, pattern, start)
        else:
            # If the pattern is in the right child's value
            # Subtract the length of the left child's value from the search position
            return self.search(node.right, pattern[len(node.left.value):], start + len(node.left.value))

    # Insert a string into the rope at the given index
    # This is implemented using recursion and binary search
    def insert(self, node, s, i):
        if node.left is None and node.right is None:
            # If the node is a leaf, insert the string into its value
            node.value = node.value[:i] + s + node.value[i:]
            node.size = len(node.value)
            if node.size > self.maxLeafChars:
                # If the leaf node exceeds the maximum size, split it into two leaf nodes
                self.split(node)
        elif i <= node.left.size:
            # If the insertion position is in the left child
            # Recursively insert the string into the left child
            self.insert(node.left, s, i)
            node.size += len(s)
            if node.left.size > self.maxLeafChars:
                # If the left child exceeds the maximum size, split it
                self.split(node.left)
        else:
            # If the insertion position is in the right child
            # Recursively insert the string into the right child
            # Subtract the length of the left child's value from the insertion position
            self.insert(node.right)

    def delete(self, node, i, j):
        """Deletes the characters from index i to j in the given node's value."""
        # If the node has no children, update its value by removing the characters from i to j.
        if node.left is None and node.right is None:
            node.value = node.value[:i] + node.value[j:]
            node.size = len(node.value)
            # If the node's new size is less than the minimum number of characters, merge the node with its siblings.
            if node.size < self.minLeafChars:
                self.merge(node)
        # If the characters to delete are within the left child node, recursively delete from the left child node.
        elif i < node.left.size and j <= node.left.size:
            self.delete(node.left, i, j)
            # Update the size of the current node by subtracting the number of characters deleted.
            node.size -= (j - i)
            # If the right child node exists and has a size less than the minimum number of characters, merge it.
            if node.right is not None and node.right.size < self.minLeafChars:
                self.merge(node.right)
        # If the characters to delete are within the right child node, recursively delete from the right child node.
        elif i >= node.left.size and j > node.left.size:
            self.delete(node.right, i - node.left.size, j - node.left.size)
            # Update the size of the current node by subtracting the number of characters deleted.
            node.size -= (j - i)
            # If the left child node exists and has a size less than the minimum number of characters, merge it.
            if node.left is not None and node.left.size < self.minLeafChars:
                self.merge(node.left)
        # If the characters to delete span across both child nodes, delete from both recursively and merge the children.
        else:
            self.delete(node.left, i, node.left.size)
            self.delete(node.right, 0, j - node.left.size)
            node.value = node.left.value + node.right.value
            node.size = len(node.value)
            if node.left.size < self.minLeafChars:
                self.merge(node.left)
            elif node.right.size < self.minLeafChars:
                self.merge(node.right)

    def replace(self, node, pattern, replace_with):
        """Replaces all occurrences of the given pattern with the given replacement string in the given node's value."""
        # Find all occurrences of the pattern within the node and add their indices to a list.
        indices = []
        index = self.search(node, pattern)
        while index != -1:
            indices.append(index)
            index = self.search(node, pattern, index + 1)
        # Iterate over the list of pattern occurrences in reverse order and delete each one, then insert the replacement string.
        for i in reversed(indices):
            self.delete(node, i, i + len(pattern))
            self.insert(node, replace_with, i)

    def split(self, node):
        # Check if the node has any children. If not, return.
        if node.left is None and node.right is None:
            return
        # Calculate the mid-point of the node's value.
        mid = node.size // 2
        # Create new left and right nodes, splitting the original node's value in half.
        left = Node(node.value[:mid])
        right = Node(node.value[mid:])
        # Set the original node's left and right children to the new left and right nodes respectively.
        node.left = left
        node.right = right
        # Set the original node's value and size to None, as it no longer has any value.
        node.value = None
        node.size = None

    def merge(self, node):
        # Check if the node has any children. If not, return.
        if node.left is None and node.right is None:
            return
        # Combine the values of the left and right children into the node's value.
        node.value = node.left.value + node.right.value
        # Set the node's size to the length of its new value.
        node.size = len(node.value)
        # Set the node's left and right children to None, as they have been merged.
        node.left = None
        node.right = None


rope = Rope("Hello, world! ")

# Search
searchResult = rope.search(rope.root, "ello", 0)
print(searchResult)

# Insertion
rope.insert(rope.root, "Yousuf", 14)

# Deletion
rope.delete(rope.root, 0, 14)

# Replace
rope.replace(rope.root, "Yousuf", "Uyghur")

print(rope)
print(rope.root.size)