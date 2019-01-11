TYPE_ALL = 'all'
TYPE_FILE = 'file'
TYPE_DIR = 'dir'

def node_matches_type(node, type):
    if type == TYPE_ALL:
        return True
    elif type == TYPE_DIR and node.__class__.__name__ == 'DirNode':
        return True
    elif type == TYPE_FILE and node.__class__.__name__ == 'FileNode':
        return True
    return False

