"""This module is the dfs-implementation which this program will be using"""
import time
from threading import Thread
from graph import Graph, EmptyGraphError


class DepthFirstSearch:
    """This class is the dfs-implementation which this program will be using"""
    def __init__(self, graph: Graph, start_node) -> None:
        """
        :param graph: The on which the algorithm will be acting
        :param start_node: The start node from dfs, important if the graph isn't connected
        """
        if graph.vertice_count == 0:
            raise EmptyGraphError
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


class DfsVisual:
    def __init__(self, graph_visuals, colour="red"):
        self.graph_visuals = graph_visuals
        self.colour = colour
        self.thread = None

    def run(self):
        self.thread = Thread(target=self.sleeper, args=(1,))
        self.thread.start()

    def sleeper(self, time_between_draws):
        for node in self.graph_visuals.graph_nodes:
            time.sleep(time_between_draws)
            self.graph_visuals.graph_nodes[node.id].node_fill_colour = "green"
            print(node.id, node.node_fill_colour)
            self.graph_visuals.redraw_nodes()





