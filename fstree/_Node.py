from anytree import Node as BaseNode


class Node(BaseNode):
    def remove(self):
        if self.children:
            raise EnvironmentError("Cannot remove node '{}' which has children.".format(self.name))
        self.parent.children = tuple([child for child in self.parent.children if child != self])

    def as_dict(self):
        res = {}
        for child in self.children:
            res[child.name] = child.as_dict()
        return res

    def get_fspath(self):
        res = '/'.join([node.name for node in self.path[1:]])
        return res

    def get_child(self, name, type_=None):
        if type_ is None:
            type_ = Node
        for c in self.children:
            if c.name == name:
                if isinstance(c, type_):
                    return c
        return None
