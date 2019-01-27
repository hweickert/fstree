import pytest
from fstree._Node import Node


def test_remove_works():
    p = Node('parent')
    c = Node('child', p)

    c.remove()
    assert p.children == tuple()

def test_remove_raises_error_if_children_exist():
    p = Node('parent')
    c = Node('child', p)
    sc = Node('subchild', c)

    with pytest.raises(EnvironmentError):
        c.remove()

