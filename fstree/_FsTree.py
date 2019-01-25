import sys
from . _DirNode import DirNode
from . _FileNode import FileNode
from . _shared import TYPE_FILE, TYPE_DIR


class FsTree(DirNode):
    def __init__(self, flip_backslashes=None):
        DirNode.__init__(self, 'root')

        if flip_backslashes is None:
            self._flip_backslashes = sys.platform == 'win32'
        else:
            self._flip_backslashes = flip_backslashes

    def get_fs_filepaths(self):
        res = [desc.get_fspath() for desc in self.descendants if isinstance(desc, FileNode)]
        return res

    def get_fs_dirpaths(self):
        res = [desc.get_fspath() for desc in self.descendants if isinstance(desc, DirNode)]
        return res

    def add(self, path, content=None):
        '''
            Convenience wrapper to add a file OR directory.
            If `path` endswith a backslash, consider this a directory, otherwise a file.
        '''
        if path.endswith('/'):
            self.add_dir(path)
        else:
            self.add_file(path, content)

    def add_file(self, file_path, content=None):
        if self._flip_backslashes:
            file_path = file_path.replace('\\', '/')
        parts = file_path.rsplit('/', 1)

        if len(parts) == 1:
            res = self.get_or_add_child_filenode(parts[0], content)
            return res
        else:
            dirpath, filename = parts
            dirnode = self.add_dir(dirpath)
            if dirnode is None:
                dirnode = self
            else:
                filenode = dirnode.get_or_add_child_filenode(filename, content)
                return filenode

    def add_dir(self, dirpath):
        if self._flip_backslashes:
            dirpath = dirpath.replace('\\', '/')
        dirpath = dirpath.rstrip('/')

        res = None
        cur_dirnode = self
        for part in dirpath.split('/'):
            exist_child = cur_dirnode.get_child(part)
            if exist_child:
                if isinstance(exist_child, FileNode):
                    raise IOError("A file '{}' already exists.".format(exist_child.get_fspath()))
                cur_dirnode = exist_child
            else:
                cur_dirnode = DirNode(part, parent=cur_dirnode)
            res = cur_dirnode
        return res

    def add_dict(self, dictionary, root_parent_dir=None):
        # TODO: Move onto `DirNode`
        for parent_dirname, child in dictionary.items():
            if root_parent_dir is None:
                parent_path = parent_dirname
            else:
                parent_path = '/'.join([root_parent_dir, parent_dirname])

            if isinstance(child, dict):
                if child == {}:
                    self.add_dir(parent_path)
                else:
                    self.add_dict(child, root_parent_dir=parent_path)
            else:
                self.add_file(parent_path, content=child)

    def walk(self, top=None):
        if top is None:
            node = self.children[0]
        else:
            node = self._find_or_raise(top, TYPE_DIR)
        return node.walk()

    def open(self, file_path, mode='r'):
        if 'w' in mode:
            filenode = self.add_file(file_path)
            res = filenode.create_new_io()
            return res

        elif 'a' in mode:
            filenode = self.add_file(file_path)
            if filenode.io is None:
                res = filenode.create_new_io()
            else:
                res = filenode.get_exist_io()
                # Move cursor to the end so
                # we can append to it.
                res.seek(0, 2)
            return res

        elif 'r' in mode:
            filenode = self._get_exist_filenode(file_path)
            res = filenode.get_exist_io()
            res.seek(0)
            return res

    def _get_exist_filenode(self, file_path):
        curnode = self
        parts = file_path.split('/')
        for part in parts[:-1]:
            if curnode is None:
                self._raise_file_not_found(file_path)
            curnode = curnode.get_child(part, DirNode)

        if curnode is None:
            self._raise_file_not_found(file_path)

        filenode = curnode.get_child(parts[-1], FileNode)
        if not filenode:
            self._raise_file_not_found(file_path)

        return filenode

    def _raise_file_not_found(self, file_path):
        msg = "No such file or directory: '{}'".format(file_path)
        raise IOError(msg)

    def _find_or_raise(self, path, type_):
        nodes = self.find(path, type_)
        if not nodes:
            raise IOError("The system cannot find the path specified: '{}/*.*'".format(path))
        res = nodes[0]
        return res
