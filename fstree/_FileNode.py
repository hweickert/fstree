from StringIO import StringIO
from . _Node import Node


class FileNode(Node):
    def __init__(self, name, parent=None):
        Node.__init__(self, name, parent=parent)
        self.io = None

    def create_new_io(self):
        self.io = FileStringIO()
        return self.io

    def get_exist_io(self):
        if self.io is None:
            # An io object wasn't created yet.
            self.io = FileStringIO()
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

