from . _Node import Node
from . _FileNode import FileNode
from . _shared import node_matches_type, TYPE_ALL


class DirNode(Node):
    def find(self, path, type=TYPE_ALL):
        pat_parts = path.split('/')
        res = _find_nodes_recursive(self, pat_parts, 0, type)
        return res

    def get_or_add_child_filenode(self, filename, content):
        exist_node = self.get_child(filename)
        if exist_node:
            if isinstance(exist_node, DirNode):
                raise IOError("A directory '{}' already exists.".format(exist_node.get_fspath()))
            return exist_node
        else:
            res = FileNode(filename, parent=self)
            if content is not None:
                res.create_new_io().write(content)
                res.io.seek(0)
            return res

def _find_nodes_recursive(node, pat_parts, level, type_):
    res = []
    islast = level == len(pat_parts) - 1
    for childnode in node.children:
        name_matches = childnode.name == pat_parts[level]
        if not name_matches:
            continue
        if islast:
            if node_matches_type(childnode, type_):
                res.append(childnode)
        else:
            subchild_nodes = _find_nodes_recursive(childnode, pat_parts, level+1, type_)
            res.extend(subchild_nodes)
    return res
