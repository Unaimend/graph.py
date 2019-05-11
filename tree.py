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
    def __init__(self, graph_vis):
        #TODO Check if graph can be represented as a tree(see definition)
        #This check could be make while building the tree in build tree(tink of cycle detention with dfs)
        #At least the acyclic check can be made while building, the connectedness check hase to be made after the build step
        root = graph_vis.graph_nodes[0]
        self.node_adj_list = graph_vis.to_cycle_free_list()
        self.root = self.build_tree(parent_=None, children=self.node_adj_list[0],id_=root.id, value_=root.value)


    # https://stackoverflow.com/questions/8991840/recursion-using-yield

    # Anschauen weil rekursion manchmal suckt
    # https://stackoverflow.com/questions/159590/way-to-go-from-recursion-to-iteration
    # https://web.archive.org/web/20120227170843/http://cs.saddleback.edu/rwatkins/CS2B/Lab%20Exercises/Stacks%20and%20Recursion%20Lab.pdf
    def iternodes(self):
        stack = [self.root]
        while stack:
            node = stack.pop()
            yield node
            for child in reversed(node.children):
                stack.append(child)

    def build_tree(self, parent_, children, id_, value_) -> TreeNode:
        if len(children) == 0:
            return TreeNode(parent_, id_, value_, [])
        else:
            tree_node =  TreeNode(None, id_, value_, [])
            tree_node_children = list()
            for node in children:
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
