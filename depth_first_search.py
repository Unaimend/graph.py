"""This module is the dfs-implementation which this program will be using"""
from graph import Graph


class DepthFirstSearch:
    """This class is the dfs-implementation which this program will be using"""
    def __init__(self, graph: Graph, start_node) -> None:
        """
        :param graph: The on which the algorithm will be acting
        :param start_node: The start node from dfs, important if the graph isn't connected
        """
        self.marked = [False] * graph.vertice_count
        self.edge_to = [-1] * graph.vertice_count
        self.start = start_node
        self._dfs(graph, start_node)

    def _dfs(self, graph: Graph, start_node):
        """
        Implements the dfs-algo
        :param graph: The on which the algorithm will be acting
        :param start_node:
        :return:
        """
        self.marked[start_node] = True
        for node in graph.adjacency_list[start_node]:
            if not self.marked[node]:
                self.edge_to[node] = start_node
                self._dfs(graph, node)

    def has_path_to(self, node):
        """
        Calculates the existence of a path from the start to the given node
        :param node: The node for which the existence should be checked
        :return:
        """
        return self.marked[node]

    def path_to(self, node):
        """
        Calculate the path to a given node
        :param node: The node for which the path should be calculated
        :return: Return the path as an list
        """
        if not self.has_path_to(node):
            return None
        path = []
        x = node
        while x != self.start:
            path.append(x)
            x = self.edge_to[x]
        path.append(self.start)
        return path
