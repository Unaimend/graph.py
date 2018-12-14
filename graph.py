"""
.. module:: graph
   :platform: Unix, Windows, Mac
   :synopsis: This module includes classes necessary for working with graphs
.. moduleauthor:: Thomas Dost(Unaimend@gmail.com)
"""
import tkinter as tk
from typing import List
import json
from vector import Vector
from logger import logger
# typedefs
AdjacencyList = List[List[int]]
AdjacencyListEntry = List[int]
AdjacencyMatrix = List[List[int]]

# TODO Should GraphNode and GraphEdge be in the graphvisual module since the are only important for the graphical
# TODO representation of graphs
# TODO Siehe https://stackoverflow.com/questions/13212300/how-to-reconfigure-tkinter-canvas-items
# TODO Graphen als n-gon aufstellen und dann algorithmen anwenden einfach for the lullz
# TODO Natuerlich nur optional
# TODO mit with  verpacken


# BUG Die letzte Node is nicht auswaehlebar
# TODO DFS Visualisierung und ueberlegen wie ich mit Graphen umgehe die nicht integer vertices haben
# IDEE Als isomorphen graphen zu einem integer graphen betrachtemn


class GraphNode:
    """
    Class which represents a node in a graph
    """
    #: Radius of the nodes
    graphNodeRadius = 12
    # TODO Save and load seed for current graph so you can draw the "same" graph if you want to

    def __init__(self, canvas: tk.Canvas, x: float, y: float, draw_ids: bool, id: int, colour="black", node_fill_colour="black") -> None:
        """
        :param canvas: The canvas on which the node should be drawn
        :type x0: tk.Canvadraw_ids: Whether to draw ids or not
        :type draw_ids: bool
        :param id: The id which should be drawn in node
        :type id: int
        """


        #: Canvas position for the node
        self.position = Vector(x, y)
        #: The canvas on which the node should be drawn(for multi-canvas support)
        self.canvas = canvas
        #: The id that will be drawn "in the node"
        self.id = id
        #: The id to identify this node on the canvas
        self.canvas_id = 0
        #: Id to identify the text of this node
        self.canvas_text_id = "-1"

        self.colour = colour
        self.node_fill_colour = node_fill_colour
        """
        Boolean which determines if the node is represented through a black dot or
        through a circle with a number inside
        """
        self.draw_ids = draw_ids

        # TODO Magic number ersetzen

        left_corner = self.position - Vector(self.graphNodeRadius/1.5, self.graphNodeRadius / 1.5)
        right_corner = self.position + Vector(self.graphNodeRadius, self.graphNodeRadius)
        if draw_ids:
            self.canvas_id = canvas.create_oval(left_corner.x,
                                                left_corner.y,
                                                right_corner.x,
                                                right_corner.y, fill="white")
            text_id_pos = Vector(self.position.x + 2, self.position.y + 2)
            self.canvas_text_id = canvas.create_text(text_id_pos.x, text_id_pos.y, text=self.id, fill=self.colour)
        else:
            self.canvas_id = canvas.create_oval(left_corner.x,
                                                left_corner.y,
                                                right_corner.x,
                                                right_corner.y, fill=node_fill_colour)

    def move(self, x: float, y: float):
        """
        NOTE: Does not change the position on the canvas, a redraw must be called to do that
        :param x: The x-offset which should be added
        :param y: The y-offset which should be added
        :return:
        """
        # update current position
        self.position.x += x
        self.position.y += y

    def __str__(self):
        return "Position x:%s y:%s, id:%s" % (self.position.x, self.position.y, self.id)

    def set_pos(self, x: float, y: float) -> None:
        """
        Sets the position of the node to the specified x,y coordinates
        :param x: x-coordinate on the canvas 
        :param y: y-coordinate on the cnavas
        :return: 
        """
        self.position.x = x
        self.position.y = y


class Graph:
    """
    Class for representing graphs
    """
    def __init__(self, filepath: str = None, adjacency_list: AdjacencyList = None,
                 adjacency_matrix: AdjacencyMatrix = None) -> None:
        """
        Note: All the variables are exlusive, that means if on is supplied the others should not be used
        :param filepath: The path from which the graph should be loaded
        :param adjacency_list: The ajd. list from which the graph should be load
        :param adjacency_matrix:
        """
        # Filepath to the grad which should be loaded
        self.filepath = filepath
        # 2d list. which holds all adjacent nodes in the form of and adjacency list
        self.adjacency_list = adjacency_list
        # 2d list. which holds all adjacent nodes in the form of and adjacency matrix
        self.adjacency_matrix = adjacency_matrix
        # Total number of vertices
        self.vertice_count = None

        # Load from a file
        # https://stackoverflow.com/questions/1369526/what-is-the-python-keyword-with-used-for
        if filepath:
            logger.info("Loading from" + filepath)
            # print("Loading from " + filepath)
            # Get file descriptor
            f = open(self.filepath, "r")
            # Load data into the adjacency_list
            self.adjacency_list = json.load(f)
            # Close file
            f.close()
            # Get the vertice count
            self.vertice_count = len(self.adjacency_list)
            logger.info("Adjacency list" + str(self.adjacency_list))
        else:
            pass
        # print("WP", self.subtree_index(0))
        self.is_binary_tree = True
        self.node_id = 0

    @classmethod
    def from_file(cls, filepath: str) -> 'Graph':
        """
        :param filepath: The file from which the graph sould be loaded
        :return:  A new graph instance
        """
        return cls(filepath=filepath)

    @classmethod
    def from_adjacency_list(cls, adjacency_list: AdjacencyList) -> 'Graph':
        """
        :param adjacency_list: The adj. list from which the graph sould be loaded
        :return:  A new graph instance
        """
        return cls(adjacency_list=adjacency_list)

    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix: AdjacencyMatrix) -> 'Graph':
        """
        :param adjacency_matrix: The adj. matrix from which the graph sould be loaded
        :return: A new graph instance
        """
        return cls(adjacency_matrix=adjacency_matrix)

    def adjacent_to(self, node: GraphNode) -> AdjacencyListEntry:
        """
        :param node: The node from which you want the ajd. list
        :return: adjacency_list from the give node
        """
        return self.adjacency_list[node.id]

    def root_index(self):
        """Returns the  index of the root"""
        if self.is_binary_tree:
            return 0
        return -1

    def traverse_binary_tree(self, index):
        # pylint: disable=C1801
        """Traverse the whole binary tree"""
        if len(self.adjacency_list) > 0:
            if index == 0:
                for child_index in self.adjacency_list[0]:
                    self.traverse_binary_tree(child_index)
            else:
                # print("TRAV", index)
                # In current node has children(>1 because every node has its parent node as an adj. list entry)
                if len(self.adjacency_list[index]) > 1:
                    for counter in range(1, len(self.adjacency_list[index])):
                        self.traverse_binary_tree(self.adjacency_list[index][counter])
                else:
                    pass

        else:
            print("Cant traverse an emtpy graph")

    def subtree_index(self, index):
        # pylint: disable=C1801
        """
        Calculates all indices of of the subtree from node[index]
        :param index: The index to the node from which you want the subtree 
        :return: A List made of the indices to the nodes of the subtree 
        """
        indices = []
        if len(self.adjacency_list) > 0:
            if index == 0:
                indices.append(0)
                for child_index in self.adjacency_list[0]:
                    self.traverse_binary_tree(child_index)
            else:
                indices.append(index)
                # In current node has children(>1 because every node has its parent node as an adj. list entry)
                if len(self.adjacency_list[index]) > 1:
                    for counter in range(1, len(self.adjacency_list[index])):
                        self.traverse_binary_tree(self.adjacency_list[index][counter])
                else:
                    pass

        else:
            print("Cant traverse an emtpy graph")

        return indices

    def parent(self, index):
        """
        Calculates the index from to parent from node[index]
        :param index: The index of the node from which you want the parent
        :return: The parent of node[index] or -1 if you ask for the parent of the root
        """
        if index == 0:
            return -1
        return self.adjacency_list[index][0]

    def dist_from_root(self, index):
        """
        Calculates the distance from root to node[index], should be the number of edges
        :param index: The index of the node from which you want the distance
        :return: The distance from root to node[index]  
        """
        if index == 0:
            return 0
        return self.dist_from_root(self.parent(index)) + 1

    def left(self, index):
        """
        Get the index left child of index
        :param index: index of the node from which you wan't the left child index
        :return: The index oft the left child of index or -1 if node[index] doesnt exist
        """
        try:
            if index == self.root_index():
                index = self.adjacency_list[index][0]
            else:
                index = self.adjacency_list[index][1]
            return index
        except IndexError:
            return -1

    def right(self, index):
        """
        Get the index right child of index
        :param index: index of the node from which you wan't the right child index
        :return: The index of the right child of index or -1 if node[index] doesnt exist
        """
        try:
            if index == self.root_index():
                index = self.adjacency_list[index][1]
            else:
                index = self.adjacency_list[index][2]
            return index
        except IndexError:
            return -1


class GraphEdge:
    """
    This class represents a graph edge
    """
    def __init__(self, canvas: tk.Canvas, start_node: GraphNode, end_node: GraphNode) -> None:
        """
        :param canvas: The canvas on which the edge should be drawn
        :type canvas: tk.Canvas
        :param start_node: The lines starting node
        :param end_node: The lines ending node
        """
        self.start_node = start_node
        self.end_node = end_node
        # Start der Kanten
        self.start = Vector(start_node.position.x, start_node.position.y)
        # Ende der Kanten
        self.end = Vector(end_node.position.x, end_node.position.y)
        # Create line and save id
        self.id = canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, smooth=True)



