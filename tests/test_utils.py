import pytest
import fstree
import fstree.utils

@pytest.mark.parametrize('paths, exp', [
    (['C:/d1/f1',
      'C:/d1/d2/',
      'C:/d1/d3/f2',
      'C:/d4/'], ['C:/d1/d2', 'C:/d1/d3', 'C:/d4']),
    (['/d1/f1',
      '/d1/d2/',
      '/d1/d3/f2',
      '/d4/'], ['/d1/d2', '/d1/d3', '/d4']),
    (['d1/f1',
      'd1/d2/',
      'd1/d3/f2',
      'd4/'], ['d1/d2', 'd1/d3', 'd4']),
])
def test_get_leaf_dirs_works(paths, exp):
    tree = fstree.FsTree()
    for path in paths:
        tree.add(path)

    res = fstree.utils.get_leaf_dirs(tree)
    assert res == exp

@pytest.mark.parametrize('paths, exp', [
    (['C:/d1/f1',
      'C:/d1/d2/',
      'C:/d1/d3/f2',
      'C:/d4/'], ['C:/d1/f1', 'C:/d1/d3/f2']),
    (['/d1/f1',
      '/d1/d2/',
      '/d1/d3/f2',
      '/d4/'], ['/d1/f1', '/d1/d3/f2']),
    (['d1/f1',
      'd1/d2/',
      'd1/d3/f2',
      'd4/'], ['d1/f1', 'd1/d3/f2']),
])
def test_get_files_works(paths, exp):
    tree = fstree.FsTree()
    for path in paths:
        tree.add(path)

    res = fstree.utils.get_files(tree)
    assert res == exp
