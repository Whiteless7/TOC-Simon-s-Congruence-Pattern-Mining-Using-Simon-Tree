"""
Simon Tree construction
"""

import sys

snd_id = 1


class SimonNode:
    def __init__(self, block_s=-1, block_f=0):
        """
        Creates a node without any connections in the simon tree.
        :param block_s: Starting position of the block. -1 denotes an open block.
        :param block_f: Ending position of the block.
        """
        global snd_id
        self.prnt = None
        self.chld = [None]
        self.block_s = block_s
        self.block_f = block_f
        self.id = snd_id
        snd_id += 1

    def has_chld(self):
        return not (len(self.chld) == 1 and self.chld[0] is None)

    def has_prnt(self):
        return self.prnt is not None

    def append_chld(self, chld, option=None):
        """
        Appends a child.
        :param chld: Child SimonNode
        :param option: Determine where to put a child. Available options: 'left', 'right' (default)
        :return:
        """
        chld.prnt = self
        if option is None or option == 'right':
            if self.chld[0] is None:
                self.chld[0] = chld
            else:
                self.chld.append(chld)
        elif option == 'left':
            if self.chld[0] is None:
                self.chld[0] = chld
            else:
                self.chld.insert(0, chld)

    def __str__(self):
        if self.block_s == -1:
            if self.has_prnt():
                return f'[?:{self.block_f}] ({self.id}, p={self.prnt.id})'
            else:
                return f'[?:{self.block_f}] ({self.id})'
        else:
            if self.has_prnt():
                if self.block_s == self.block_f:
                    return f'[{self.block_s}] ({self.id}, p={self.prnt.id})'
                else:
                    return f'[{self.block_s}:{self.block_f}] ({self.id}, p={self.prnt.id})'
            else:
                if self.block_s == self.block_f:
                    return f'[{self.block_s}] ({self.id})'
                else:
                    return f'[{self.block_s}:{self.block_f}] ({self.id})'

    def __repr__(self):
        return self.__str__()


class SimonTree:
    def __init__(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def get_leftmost_child(self):
        c = self.root
        while c.chld[0] is not None:
            c = c.chld[0]
        return c

    def remove_node(self, node):
        """
        Do nothing if the node is the root.
        """
        if not node.has_prnt():
            return
        t_id = node.id
        for i in range(len(node.prnt.chld)):
            if node.prnt.chld[i].id == t_id:
                node.prnt.chld.pop(i)
                return

    def clean_up(self, n):
        next = [self.root]
        rm = self.root.id
        while True:
            m = len(next)
            if m == 0:
                return
            for i in range(m):  # For all node in next
                node = next.pop(0)
                if node.block_s == n+1 and node.block_f == n+1:
                    self.remove_node(node)
                    continue
                if node.block_s == -1:
                    node.block_s = 0
                if rm == node.id:
                    node.block_f = n
                    if node.chld[len(node.chld)-1] is not None:
                        rm = node.chld[len(node.chld)-1].id
                for c in node.chld:
                    if c is None:
                        break
                    next.append(c)

    def __str__(self):
        next = [self.root]
        lv = 0
        s = ''
        while True:
            n = len(next)
            if n == 0:
                return s.strip('\n')
            s += f'k={lv}: '
            for i in range(n):  # For all node in next
                node = next.pop(0)
                s += f'{node} '
                for c in node.chld:
                    if c is None:
                        break
                    next.append(c)
            s += f'\n'
            lv += 1

    def __repr__(self):
        return self.__str__()


def comp_x(w):
    """
    Calculates array X. Uses from-0 indexing instead of from-1.
    :param w: Target string.
    :return: The array X. We denote 'inf' as n+2 for QoL.
    """
    n = len(w)
    X = [-1] * n
    last_occ = {}
    for i in range(n, 0, -1):
        try:
            X[i-1] = last_occ[w[i-1]]
            last_occ[w[i-1]] = i-1
        except KeyError:
            X[i-1] = n+2
            last_occ[w[i-1]] = i-1
    return X


def find_node(i, T, a):
    """
    Simulates findNode subroutine of the construction alg.
    :param i: Pass this as from-0 index.
    """
    global X
    while a.prnt is not None:
        r = a.block_f
        rp = a.prnt.block_f
        if r <= X[i] < rp:
            return a
        else:
            a.block_s = i+1
            a = a.prnt
    return a


def split_node(i, T, a):
    """
    Simulates splitNode subroutine of the construction alg.
    :param i: Pass this as from-0 index.
    """
    if a == T.get_leftmost_child():
        a.append_chld(SimonNode(i+1, i+1))
        b = SimonNode(-1, i)
        a.append_chld(b, option='left')
        return b
    else:
        b = SimonNode(-1, i)
        a.append_chld(b, option='left')
        return b


if __name__ == '__main__':
    w = sys.argv[1]
    n = len(w)

    if n < 2:
        print(f'Wrong argument: Input should be at least 2 characters long')
        sys.exit(1)

    wp = w + '\0'
    T = SimonTree(SimonNode(-1, n))  # From-0 indexing -> block_f is n instead of n+1
    p = T.get_root()
    X = comp_x(wp)

    for i in range(n, 0, -1):
        a = find_node(i-1, T, p)
        p = split_node(i-1, T, a)

    T.clean_up(n-1)
    print(T)
