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

    def __init__(self, canvas: tk.Canvas, x: float, y: float, draw_ids: bool, id: int, colour) -> None:
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
        #: The id to identify this node
        self.canvas_id = 0
        #: Id to identify the text of this node
        self.canvas_text_id = "-1"

        self.colour = colour
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
                                                right_corner.y, fill="black")


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
            print("Loading from " + filepath)
            # Get file descriptor
            f = open(self.filepath, "r")
            # Load data into the adjacency_list
            self.adjacency_list = json.load(f)
            # Close file
            f.close()
            # Get the vertice count
            self.vertice_count = len(self.adjacency_list)
            print("Adjacency list", self.adjacency_list)
        else:
            print("TODO exception")

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



