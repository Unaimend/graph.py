"""This module is the dfs-implementation which this program will be using"""
import time
from threading import Thread
from graph import Graph, EmptyGraphError


class DepthFirstSearch:
    """This class is the dfs-implementation which this program will be using"""
    def __init__(self, graph: Graph, start_node: int) -> None:
        """
        :param graph: The on which the algorithm will be acting
        :param start_node: The start node from dfs, important if the graph isn't connected
        """
        if graph.vertice_count == 0:
            raise EmptyGraphError
        self.marked = [False] * graph.vertice_count
        self.contains_cycle = False
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
            else:
                self.contains_cycle = True

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
    def __init__(self, graph_visuals, colour="red", func=(lambda x: x)):
        self.graph_visuals = graph_visuals
        self.colour = colour
        self.thread = None
        self.func = func
        if len(graph_visuals.graph_nodes) == 0:
            raise EmptyGraphError
        self.marked = [False] * len(graph_visuals.graph_nodes)
        self.start_node = graph_visuals.graph_nodes[0]
        self.run()

    def run(self):
        self.thread = Thread(target=self.dfs_, args=(self.start_node,))
        self.thread.start()

    # TODO In jedem Step die graph_visuals.node_adjacency_list in ne Liste KOPIEREN und dann eifnach uebschreiben udn 
    # neue zeichen wenn previous/next frame gefordert wird 
    def dfs_(self, node):
        self.marked[node.id] = True
        func(self.graph_visuals.graph_nodes[node.id])
        self.graph_visuals.redraw_nodes()
        for node in self.graph_visuals.node_adjacency_list[node.id]:
            time.sleep(0.3)
            if not self.marked[node.id]:
                self.dfs_(node)





