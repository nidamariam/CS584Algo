import random
import math
import sys
import time
from collections import defaultdict


class TreapNode(object):
    def __init__(self, key, data):
        self.key = key
        self.ran = random.random()
        self.size = 1
        self.cnt = 1
        self.data = data
        self.left = None
        self.right = None

    def left_rotate(self):
        a = self
        b = a.right
        a.right = b.left
        b.left = a
        a = b
        b = a.left
        b.size = b.left_size() + b.right_size() + b.cnt
        a.size = a.left_size() + a.right_size() + a.cnt
        return a

    def right_rotate(self):
        a = self
        b = a.left
        a.left = b.right
        b.right = a
        a = b
        b = a.right
        b.size = b.left_size() + b.right_size() + b.cnt
        a.size = a.left_size() + a.right_size() + a.cnt
        return a

    def left_size(self):
        return 0 if self.left is None else self.left.size

    def right_size(self):
        return 0 if self.right is None else self.right.size

    def __repr__(self):
        return '<node key:%s ran:%f size:%d left:%s right:%s>' % (str(self.key), self.ran, self.size, str(self.left), str(self.right))


class Treap(object):
    def __init__(self):
        self.root = None

    def _insert(self, node, key, data=None):
        if node is None:
            node = TreapNode(key, data)
            return node
        node.size += 1
        if key < node.key:
            node.left = self._insert(node.left, key, data)
            if node.left.ran < node.ran:
                node = node.right_rotate()
        elif key >= node.key:
            node.right = self._insert(node.right, key, data)
            if node.right.ran < node.ran:
                node = node.left_rotate()
        return node

    def insert(self, key, data=None):
        self.root = self._insert(self.root, key, data)

    def _find(self, node, key):
        if node == None:
            return None
        if node.key == key:
            return node
        if key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)

    def search(self, key):
        return self._find(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return False
        if node.key == key:
            if node.left is None and node.right is None:
                return None
            elif node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                if node.left.ran < node.right.ran:
                    node = node.right_rotate()
                    node.right = self._delete(node.right, key)
                else:
                    node = node.left_rotate()
                    node.left = self._delete(node.left, key)
        elif key < node.key:
            node.left = self._delete(node.left, key)
        else:
            node.right = self._delete(node.right, key)
        node.size = node.left_size() + node.right_size() + node.cnt
        return node

    def delete(self, key):
        if self.search(key) is None: return False
        self.root = self._delete(self.root, key)
        return True

    def _find_kth(self, node, k):
        if node is None: return None
        if k <= node.left_size():
            return self._find_kth(node.left, k)
        if k > node.left_size() + node.cnt:
            return self._find_kth(node.right, k - node.left_size() - node.cnt)
        return node

    def find_kth(self, k):
        if k <=0 or k > self.size():
            return None
        return self._find_kth(self.root, k)

    def size(self):
        return 0 if self.root is None else self.root.size

    def median(self):
        s = self.size()
        if s == 0: return 0
        result = 0
        if s % 2 == 1:
            result = self.find_kth(s / 2 + 1).key
        else:
            result = (self.find_kth(s / 2).key + self.find_kth(s / 2 + 1).key) / 2.0
        if result == int(result): result = int(result)
        return result

    def _traverse(self, node):
        if node == None: return
        self._traverse(node.left)
        print (node.key)
        self._traverse(node.right)

    def traverse(self):
        self._traverse(self.root)

    def __repr__(self):
        return str(self.root)

class SkipListNode:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level, p):
        self.MAX_LEVEL = max_level
        self.P = p
        self.header = self.create_node(self.MAX_LEVEL, -1)
        self.level = 0

    def create_node(self, lvl, key):
        n = SkipListNode(key, lvl)
        return n

    def random_level(self):
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, key):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.key != key:
            rlevel = self.random_level()

            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            new_node = self.create_node(rlevel, key)
            for i in range(rlevel + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def delete(self, key):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is not None and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1

    def get_levels(self):
        return self.level + 1

    def display_list(self):
        print("\n*****Skip List*****")
        head = self.header
        for lvl in range(self.level + 1):
            print("Level {}: ".format(lvl), end=" ")
            node = head.forward[lvl]
            while(node != None):
                print(node.key, end=" ")
                node = node.forward[lvl]
            print("")

    def search(self, key):
        current = self.header
        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]
        if current and current.key == key:
            return True
        else:
            return False

class AVLNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def getHeight(self, node):
        if not node:
            return 0
        return node.height

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.left) - self.getHeight(node.right)

    def rightRotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))
        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))

        return x

    def leftRotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        x.height = 1 + max(self.getHeight(x.left), self.getHeight(x.right))
        y.height = 1 + max(self.getHeight(y.left), self.getHeight(y.right))

        return y

    def _insert(self, node, key):
        if not node:
            return AVLNode(key)
        elif key < node.key:
            node.left = self._insert(node.left, key)
        else:
            node.right = self._insert(node.right, key)

        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))

        balance = self.getBalance(node)

        if balance > 1 and key < node.left.key:
            return self.rightRotate(node)
        if balance < -1 and key > node.right.key:
            return self.leftRotate(node)
        if balance > 1 and key > node.left.key:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        if balance < -1 and key < node.right.key:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _delete(self, node, key):
        if not node:
            return node

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            temp = self.getMinValueNode(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        balance = self.getBalance(node)

        if balance > 1 and self.getBalance(node.left) >= 0:
            return self.rightRotate(node)
        if balance > 1 and self.getBalance(node.left) < 0:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)
        if balance < -1 and self.getBalance(node.right) <= 0:
            return self.leftRotate(node)
        if balance < -1 and self.getBalance(node.right) > 0:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def getMinValueNode(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def calculate_height(self):
        return self.getHeight(self.root)

    def preOrder(self, node=None):
        if node is None:
            node = self.root
        if node is not None:
            print(f"{node.key}", end=' ')
            self.preOrder(node.left)
            self.preOrder(node.right)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return False
        elif node.key == key:
            return True
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)

class RBNode:
    def __init__(self, key, color="red"):
        self.key = key
        self.color = color
        self.left = None
        self.right = None
        self.parent = None

class RedBlackTree:
    def __init__(self):
        self.NIL = RBNode(key=None, color="black")
        self.root = self.NIL

    def insert(self, key):
        new_node = RBNode(key)
        new_node.left = self.NIL
        new_node.right = self.NIL

        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if new_node.key < current.key:
                current = current.left
            else:
                current = current.right

        new_node.parent = parent

        if parent is None:
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

        new_node.color = "red"
        new_node.left = self.NIL
        new_node.right = self.NIL

        self.fix_insert(new_node)

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.NIL:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.NIL:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def fix_insert(self, k):
        while k != self.root and k.parent.color == "red":
            if k.parent == k.parent.parent.left:
                u = k.parent.parent.right
                if u.color == "red":
                    k.parent.color = "black"
                    u.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.right_rotate(k.parent.parent)
            else:
                u = k.parent.parent.left
                if u.color == "red":
                    k.parent.color = "black"
                    u.color = "black"
                    k.parent.parent.color = "red"
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = "black"
                    k.parent.parent.color = "red"
                    self.left_rotate(k.parent.parent)
        self.root.color = "black"

    def transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def delete(self, key):
        z = self.search(self.root, key)
        if z:
            self._delete_node(z)

    def _delete_node(self, z):
        pass  

    def search(self, node, key):
        if node == self.NIL or key == node.key:
            return node
        if key < node.key:
            return self.search(node.left, key)
        else:
            return self.search(node.right, key)

    def minimum(self, node):
        while node.left != self.NIL:
            node = node.left
        return node

    def fix_delete(self, x):
        while x != self.root and x.color == "black":
            if x == x.parent.left:
                s = x.parent.right
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.left_rotate(x.parent)
                    s = x.parent.right
                if s.left.color == "black" and s.right.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.right.color == "black":
                        s.left.color = "black"
                        s.color = "red"
                        self.right_rotate(s)
                        s = x.parent.right
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.right.color = "black"
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == "red":
                    s.color = "black"
                    x.parent.color = "red"
                    self.right_rotate(x.parent)
                    s = x.parent.left
                if s.right.color == "black" and s.left.color == "black":
                    s.color = "red"
                    x = x.parent
                else:
                    if s.left.color == "black":
                        s.right.color = "black"
                        s.color = "red"
                        self.left_rotate(s)
                        s = x.parent.left
                    s.color = x.parent.color
                    x.parent.color = "black"
                    s.left.color = "black"
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = "black"

    def _delete_node(self, z):
        y = z
        y_original_color = y.color
        if z.left == self.NIL:
            x = z.right
            self.transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self.transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self.transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == "black":
            self.fix_delete(x)

    def calculate_height(self):
        def height(node):
            if node == self.NIL:
                return 0
            return max(height(node.left), height(node.right)) + 1
        return height(self.root)

def generate_inputs(num_elements):
    random_input = random.sample(range(num_elements^3), num_elements)
    sorted_input = sorted(random_input)
    almost_sorted_input = sorted_input[:]
    swaps = len(almost_sorted_input) // 100
    for _ in range(swaps):
        i, j = random.sample(range(len(almost_sorted_input)), 2)
        almost_sorted_input[i], almost_sorted_input[j] = almost_sorted_input[j], almost_sorted_input[i]
    broad_range_input = random.sample(range(num_elements * 100), num_elements)
    return {
        "Random": random_input,
        "Sorted": sorted_input,
        "Almost Sorted": almost_sorted_input,
        "Broad Range": broad_range_input
    }

def compare_structures(elements, deletion_subset, search_subset):
    max_level = int(math.log2(len(elements)))
    p = 0.5

    structures = {
        "Treap": Treap(),
        "SkipList": SkipList(max_level, p),
        "AVLTree": AVLTree(),
        "RedBlackTree": RedBlackTree()
    }

    insertion_times = defaultdict(list)
    deletion_times = defaultdict(list)
    search_times = defaultdict(list)

    for name, structure in structures.items():
        start_time = time.time()
        for element in elements:
            structure.insert(element)
        insertion_times[name].append(time.time() - start_time)

        start_time = time.time()
        for element in deletion_subset:
            structure.delete(element)
        deletion_times[name].append(time.time() - start_time)

        start_time = time.time()
        for element in search_subset:
          if name == "RedBlackTree":
            structure.search(structure.root, element)
          else:
            structure.search(element)
        search_times[name].append(time.time() - start_time)

    for name in structures:
        print(f"{name} - Insertion Time: {sum(insertion_times[name])/len(insertion_times[name]):.4f} seconds")
        print(f"{name} - Deletion Time: {sum(deletion_times[name])/len(deletion_times[name]):.4f} seconds")
        print(f"{name} - Search Time: {sum(search_times[name])/len(search_times[name]):.4f} seconds")

def main():
    num_elements = 1000000
    deletion_fraction = 0.1
    search_fraction = 0.1

    inputs = generate_inputs(num_elements)
    for input_type, elements in inputs.items():
        print(f"\nComparing on {input_type} Input")
        deletion_subset = random.sample(elements, int(num_elements * deletion_fraction))
        search_subset = elements
        compare_structures(elements, deletion_subset, search_subset)

if __name__ == "__main__":
    main()