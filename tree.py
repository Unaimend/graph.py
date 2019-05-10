import graphvisual as G
from typing import List


class TreeNode:
    def __init__(self, parent, id: int, value, children):
        self.id = id
        self.value = value
        self.parent = parent
        self.children = children

    def set_children(self, children):
        self.children = children

class Tree:
    # TODO Define Iterator behavior
    def __init__(self, root, node_adj_list):
        #TODO Check if graph can be represented as a tree(see definition)
        #This check could be make while building the tree in build tree(tink of cycle detention with dfs)
        #At least the acyclic check can be made while building, the connectedness check hase to be made after the build step

        self.node_adj_list = node_adj_list
        self.root = self.build_tree(parent_=None, children=self.node_adj_list[0],id_=root.id, value_=root.value)

        self.print_tree(self.root)

    def build_tree(self, parent_, children, id_, value_) -> TreeNode:
        print("CHIL", children)
        if len(children) == 0:
            return TreeNode(parent_, id_, value_, [])
        else:
            tree_node =  TreeNode(None, id_, value_, [])
            tree_node_children = list()
            for node in children:
                print("node", node)
                tree_node_child = self.build_tree(parent_=tree_node, children=self.node_adj_list[node.id], id_=node.id, value_=node.value)
                tree_node_children.append(tree_node_child)
            tree_node.set_children(tree_node_children)
            return tree_node

    def print_tree(self, node):
        print(node.id)
        if len(node.children) == 0:
            pass
        else:
            for x in node.children:
                self.print_tree(x)


    def to_adj_():
        pass
        # return a tree converted to an adj_thingy
