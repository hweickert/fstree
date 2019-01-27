TYPE_ALL = 'all'
TYPE_FILE = 'file'
TYPE_DIR = 'dir'

def node_matches_type(node, type):
    from . _FileNode import FileNode
    from . _DirNode import DirNode

    if type == TYPE_ALL:
        return True
    elif type == TYPE_DIR and isinstance(node, DirNode):
        return True
    elif type == TYPE_FILE and isinstance(node, FileNode):
        return True
    return False

