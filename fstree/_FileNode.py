from StringIO import StringIO
from . _Node import Node


class FileNode(Node):
    def __init__(self, name, parent=None):
        Node.__init__(self, name, parent=parent)
        self.io = None

    def create_new_io(self, cls=None, *args, **kwargs):
        cls = FileStringIO if cls is None else cls
        self.io = cls(*args, **kwargs)
        return self.io

    def get_exist_io(self, cls=None, *args, **kwargs):
        cls = FileStringIO if cls is None else cls
        if self.io is None:
            # An io object wasn't created yet.
            self.create_new_io(cls, *args, **kwargs)
        return self.io

    def as_dict(self):
        res = None
        return res

class FileStringIO(StringIO):
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_info, exc_tb):
        self.seek(0)
        return False

