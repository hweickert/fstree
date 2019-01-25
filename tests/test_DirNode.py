import pytest
import fstree
from fstree._DirNode import DirNode


def test_walk_nodes_works():
    root_node = DirNode('')

    c = DirNode('C:', parent=root_node)
    d1 = DirNode('d1', parent=c)
    d2 = DirNode('d2', parent=d1)

    gen_walk = root_node.walk_nodes()
    for exp_dirnodes, exp_filenodes in zip([[c], [d1], [d2]], [[], [], []]):
        root, dirnodes, filenodes = next(gen_walk)
        assert dirnodes == exp_dirnodes
        assert filenodes == exp_filenodes

def test_walk_doesnt_return_none_root():
    root_node = DirNode(None)

    c = DirNode('C:', parent=root_node)
    d1 = DirNode('d1', parent=c)
    d2 = DirNode('d2', parent=d1)

    gen_walk = root_node.walk()
    for exp_root, exp_dirnodes, exp_filenodes in [(None, ['C:'], []), ('C:', ['d1'], [])]:
        root, dirnodes, filenodes = next(gen_walk)
        assert root == exp_root
        assert dirnodes == exp_dirnodes
        assert filenodes == exp_filenodes
