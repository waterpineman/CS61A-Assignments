def tree(label, branches = []):
    for branch in branches:
        assert is_tree(branch), "branches must a tree"
    return [label] + list(branches)

simple = [2, [2, [8], [10], [20]], [9]]

def is_tree(tree):
    if type(tree) != list or len(tree) < 1:
        return False
    for branch in branches(tree):
        if not is_tree(branch):
            return False
    return True


def branches(tree):
    return tree[1:]


def label(tree):
    return tree[0]


def fib_tree(n):
    if n <= 1:
        return tree(n)
    else:
        right, left = fib_tree(n - 1), fib_tree(n - 2)
        return tree(label(right) + label(left), [right, left])
    

def reverse(n):
    if n <= 1:
        return n
    else:
        a, b = reverse(n - 2), reverse(n - 1)
        return a + b

def is_leaf(tree):
    return not branches(tree)

def increment_leaves(t):
    if is_leaf(t):
        return tree(label(t) + 1)
    else:
        bs = [increment_leaves(b) for b in branches(t)]
        return tree(label(t), bs)
    
def inccrement(t):
    return tree(label(t) + 1, [inccrement(b) for b in branches(t)])


