import sys
import pytest
import fstree


@pytest.mark.parametrize('files,dirs,exp', [
    [[],                       [],             {}],
    [[],                       ['D'],          {'D': {}}],
    [[],                       ['D', 'D'],     {'D': {}}],
    [[],                       ['D', 'D2'],    {'D': {}, 'D2': {}}],
    [['F:/file'],              [],             {'F:': {'file': None}}],
    [['F'],                    [],             {'F': None}],
    [['F', 'F'],               [],             {'F': None}],
    [[],                       ['D/D'],        {'D': {'D': {}}}],
    [[],                       ['D/D', 'D/D'], {'D': {'D': {}}}],
    [[],                       ['D/D', 'E'],   {'D': {'D': {}}, 'E': {}}],
    [[],                       ['D/D', 'E'],   {'D': {'D': {}}, 'E': {}}],
    [['D/F'],                  [],             {'D': {'F': None}}],
    [['D/F', 'D/F2'],          [],             {'D': {'F': None, 'F2': None}}],
    [['D/F', 'D/F2', 'D/D/F'], [],             {'D': {'F': None, 'F2': None, 'D': {'F': None}}}],
])
def test_add_file_and_add_dir(files, dirs, exp):
    tree = fstree.FsTree()
    map(tree.add_file, files)
    map(tree.add_dir, dirs)

    res = tree.as_dict()
    assert res == exp

def test_add_file_raises_ioerror_if_dir_exists():
    tree = fstree.FsTree()
    tree.add_file('C:/file')
    with pytest.raises(IOError):
        tree.add_file('C:/file/file')

def test_add_dir_raises_ioerror_if_file_exists():
    tree = fstree.FsTree()
    tree.add_dir('C:/dir')
    with pytest.raises(IOError):
        tree.add_file('C:/dir')

def test_add_creates_file_if_no_trailing_backslash():
    tree = fstree.FsTree()
    tree.add('p/p')
    assert tree.as_dict() == {'p': {'p': None}}

def test_add_creates_dir_if_trailing_backslash():
    tree = fstree.FsTree()
    tree.add('p/p/')
    assert tree.as_dict() == {'p': {'p': {}}}

@pytest.mark.parametrize('path', [
    'C:/temp/file.txt',
    'C:/temp',
    'C:',
])
def test_get_fspath(path):
    tree = fstree.FsTree()
    node = tree.add_file(path)
    assert path == node.get_fspath()

def test_add_file_with_content():
    tree = fstree.FsTree()
    path = 'C:/file.txt'
    text = 'hello world'

    tree.add_file(path, text)

    with tree.open(path, 'r') as file_:
        res = file_.read()

    assert res == text

def test_open_write_creates_readable_file():
    tree = fstree.FsTree()
    with tree.open('C:/temp/myfile.txt', 'w') as file_:
        pass
    with tree.open('C:/temp/myfile.txt', 'r') as file_:
        data = file_.read()
    assert '' == data

def test_open_write_written_test_can_be_read():
    tree = fstree.FsTree()
    with tree.open('C:/temp/myfile.txt', 'w') as file_:
        file_.write('test')
    with tree.open('C:/temp/myfile.txt', 'r') as file_:
        data = file_.read()
    assert 'test' == data

def test_open_append_written_test_can_be_read():
    tree = fstree.FsTree()
    with tree.open('C:/temp/myfile.txt', 'a') as file_:
        file_.write('test')
    with tree.open('C:/temp/myfile.txt', 'r') as file_:
        data = file_.read()
    assert 'test' == data

@pytest.mark.parametrize('filepath', [
    'file.txt',
    'C:/temp/myfile.txt',
])
def test_open_read_without_file_raises_ioerror(filepath):
    tree = fstree.FsTree()
    with pytest.raises(IOError):
        with tree.open(filepath, 'r') as file_:
            pass


@pytest.mark.parametrize('filepaths,exp', [
    (['file.txt',   'file2.txt'], ['file.txt',   'file2.txt']),
    (['D/file.txt', 'file2.txt'], ['D/file.txt', 'file2.txt']),
])
def test_get_fs_filepaths(filepaths,exp):
    tree = fstree.FsTree()
    map(tree.add_file, filepaths)
    assert exp == tree.get_fs_filepaths()

@pytest.mark.parametrize('filepaths, dirpaths, exp_filepaths, exp_dirpaths', [
    ([],         ['D', 'D/D2'],[],         ['D', 'D/D2']),
    (['f'],      ['D', 'D/D2'],['f'],      ['D', 'D/D2']),
    (['f','D/f'],['D', 'D/D2'],['f','D/f'],['D', 'D/D2']),
])
def test_filepaths_and_dirpaths_works(filepaths, dirpaths, exp_filepaths, exp_dirpaths):
    tree = fstree.FsTree()
    map(tree.add_file, filepaths)
    map(tree.add_dir, dirpaths)
    assert exp_filepaths == tree.get_fs_filepaths()
    assert exp_dirpaths == tree.get_fs_dirpaths()

@pytest.mark.parametrize('files, path, exp', [
    ([],          'D',    False),
    (['D'],       'D/D',  False),
    (['D/D3'],    'D/D2', False),
    (['D/D2'],    'D/D2', True),
    (['D/D2/D3'], 'D/D2', True),
    (['D/D2/D3'], 'D',    True),
])
def test_find(files, path, exp):
    tree = fstree.FsTree()
    map(tree.add_file, files)
    res = bool(tree.find(path))
    assert res == exp


# --- Platform-specific ---
def test_flip_backslashes_on_windows_defaults_to_true(monkeypatch):
    monkeypatch.setattr(sys, 'platform', 'win32')

    tree = fstree.FsTree()
    tree.add_dir('C:\\')
    assert tree.as_dict() == {'C:': {}}

    tree = fstree.FsTree()
    tree.add_file('C:\\f')
    assert tree.as_dict() == {'C:': {'f': None}}

def test_flip_backslashes_on_non_windows_defaults_to_false(monkeypatch):
    monkeypatch.setattr(sys, 'platform', 'linux2')

    tree = fstree.FsTree()
    tree.add_dir('C:\\')
    assert tree.as_dict() == {'C:\\': {}}

    tree = fstree.FsTree()
    tree.add_file('C:\\f')
    assert tree.as_dict() == {'C:\\f': None}

def test_flip_backslashes_true_works(monkeypatch):
    tree = fstree.FsTree(flip_backslashes=True)
    tree.add_dir('C:\\')
    assert tree.as_dict() == {'C:': {}}

    tree = fstree.FsTree(flip_backslashes=True)
    tree.add_file('C:\\f')
    assert tree.as_dict() == {'C:': {'f': None}}

def test_flip_backslashes_false_works(monkeypatch):
    tree = fstree.FsTree(flip_backslashes=False)
    tree.add_dir('C:\\')
    assert tree.as_dict() == {'C:\\': {}}

    tree = fstree.FsTree(flip_backslashes=False)
    tree.add_file('C:\\f')
    assert tree.as_dict() == {'C:\\f': None}

@pytest.mark.parametrize('dirpath, exp', [
    ('C:\\', {'C:': {}}),
])
def test_add_dir_flips_fwdslashes_on_win(dirpath, exp, monkeypatch):
    monkeypatch.setattr(sys, 'platform', 'win32')
    tree = fstree.FsTree()
    tree.add_dir(dirpath)
    assert tree.as_dict() == exp

@pytest.mark.parametrize('filepath, exp', [
    (r'C:\f', {'C:': {'f': None}}),
])
def test_add_file_flips_fwdslashes_on_win(filepath, exp, monkeypatch):
    monkeypatch.setattr(sys, 'platform', 'win32')
    tree = fstree.FsTree()
    tree.add_file(filepath)
    assert tree.as_dict() == exp

@pytest.mark.parametrize('fs_paths, exp', [
    ([], []),
    (['r'], ['r']),
    (['r/f'], ['r/f']),
    (['r/f/f2'], ['r/f/f2']),
    (['/r'], ['/r']),
    (['/r/d'], ['/r/d']),
    (['/r/d/c'], ['/r/d/c']),
    (['/dir/', '/bar/', '/bar/spam'], ['/dir/', '/bar/spam']),
    (['dir/', '/bar/', '/bar/spam'], ['dir/', '/bar/spam']),
])
def test_as_list_works(fs_paths, exp, monkeypatch):
    tree = fstree.FsTree()
    for fs_path in fs_paths:
        tree.add(fs_path)
    assert tree.as_list() == exp

def test_add_dict_creates_files_with_content():
    tree = fstree.FsTree()
    tree.add_dict({'C:': {'file': 'test'}})
    assert tree.open('C:/file', 'r').read() == 'test'

@pytest.mark.parametrize('fs_dict, exp_dir_paths', [
    ({'C:': {}},                     ['C:']),
    ({'C:': {'d1': {}}},             ['C:', 'C:/d1']),
    ({'C:': {'f1': None}},           ['C:']),
    ({'C:': {'d1': {}, 'f1': None}}, ['C:', 'C:/d1']),
])
def test_add_dict_adds_directories(fs_dict, exp_dir_paths):
    tree = fstree.FsTree()
    tree.add_dict(fs_dict)
    assert tree.get_fs_dirpaths() == exp_dir_paths

@pytest.mark.parametrize('fs_dict, exp_dir_paths', [
    ({'C:/d1': {}},              {'C:': {'d1': {}}}),
    ({'C:/d1/d2': {}},           {'C:': {'d1': {'d2': {}}}}),
    ({'~/dev': {}},              {'~': {'dev': {}}}),
    ({'~/dev': {'foo/bar': {}}}, {'~': {'dev': {'foo': {'bar': {}}}}}),
])
def test_add_dict_converts_paths_with_subdirs_into_nodes(fs_dict, exp_dir_paths):
    tree = fstree.FsTree()
    tree.add_dict(fs_dict)
    assert tree.as_dict() == exp_dir_paths

