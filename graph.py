from typing import List
import json
from Vector import Vector



#typedefs
AdjacencyList = List[List[int]]
AdjacencyMatrix = List[List[int]]


class GraphNode:
    graphNodeRadius = 12

    # TODO Save and load seed for current graph so you can draw the "same" graph if you want to
    # TODO Nodes sollte wissen zu wem sie adjazent sind
    def __init__(self, canvas, x, y, draw_ids: bool, id: int):
        # Canvas position for the node
        self.position = Vector(x, y)
        # The canvas on which the node should be drawn(for multi-canvas support)
        self.canvas = canvas
        # The id that will be drawn "in the node"
        self.id = id
        # The id to identify this node
        self.canvas_id = 0
        # Id to identify the text of this node
        self.canvas_text_id = "-1"
        #
        self.draw_ids = draw_ids

        # TODO Magic number ersetzen
        if draw_ids:
            self.canvas_id = canvas.create_oval(self.position.x - self.graphNodeRadius / 1.5,
                                                self.position.y - self.graphNodeRadius / 1.5,
                                                self.position.x + self.graphNodeRadius,
                                                self.position.y + self.graphNodeRadius, fill="white")
            self.canvas_text_id = canvas.create_text(self.position.x + 2, self.position.y + 2, text=self.id)
        else:
            self.canvas_id = canvas.create_oval(self.position.x - self.graphNodeRadius / 1.5,
                                                self.position.y - self.graphNodeRadius / 1.5,
                                                self.position.x + self.graphNodeRadius,
                                                self.position.y + self.graphNodeRadius, fill="black")

    def move_old(self, x, y):
        # update current position
        self.position.x += x
        self.position.y += y
        # update current canvas position
        self.canvas.move(self.canvas_id, x, y)
        self.canvas.move(self.canvas_text_id, x, y)

    def move(self, x, y):
        # update current position
        self.position.x += x
        self.position.y += y
        # update current canvas position
        # self.canvas.move(self.canvas_id, x, y)
        # self.canvas.move(self.canvas_text_id, x, y)


class Graph:
    def __init__(self, width: int=None, height: int=None, filepath: str=None, adjacency_list: AdjacencyList=None,
                 adjacency_matrix: AdjacencyMatrix=None):
        # Filepath to the grad which should be loaded
        self.filepath = filepath
        # dict. which holds all adjacent nodes in the form of and adjacency list
        self.adjacency_list = None
        # dict. which holds all adjacent nodes in the form of and adjacency matrix
        self.adjacency_matrix = None
        # Total number of vertices
        self.vertice_count = None
        # Heigth of the canvas in pixel
        self.canvas_height = height
        # Width of the canvas in pixel
        self.canvas_width = width

        # Load from a file
        #TODO in try catch verpacken
        #https://stackoverflow.com/questions/1369526/what-is-the-python-keyword-with-used-for
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
        # Load from an adjacency list
        elif adjacency_list:
            self.adjacency_list = adjacency_list
        # Load from adjacency matrix
        elif adjacency_matrix:
            self.adjacency_matrix = adjacency_matrix
        else:
            print("TODO exception")

    @classmethod
    def from_file(cls, width, height, filepath):
        return cls(width=width, height=height, filepath=filepath)

    @classmethod
    def from_adjacency_list(cls, width, height, adjacency_list):
        return cls(width=width, height=height, adjacency_list=adjacency_list)

    @classmethod
    def from_adjacency_matrix(cls, width, height, adjacency_matrix):
        return cls(width=width, height=height, adjacency_matrix=adjacency_matrix)

    def adjacent_to(self, node: GraphNode=None):
        return self.adjacency_list[node.id]


# TODO Edges sollte wissen zu wem sie inzident sind
class GraphEdge:
    def __init__(self, canvas, x0, y0, xn, yn):
        """
        Ctor for the GraphEdge class
        :param canvas: The canvas on which the edge should be drawn
        :type canvas: A canvas type which muss support creating a line
         canvas.create(xstart:float, ytart:float, xend:float, yend:float, smoothing:bool
        :param x0: The start on the x coordinate
        :param y0: The start on the y coordinate
        :param xn: The end on the x coordinate
        :param yn: The end on the y coordinate
        """
        # Start der Kanten
        self.start = Vector(x0, y0)
        # self.start_node = start_node
        # self.end_node  = end_node

        # Ende der Kanten
        self.end = Vector(xn, yn)
        # Create line and save id
        self.id = canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, smooth=True)

    @classmethod
    def from_nodes(cls, canvas, start_node, end_node):
        return cls(canvas=canvas, x0=start_node.position.x,
                   y0=start_node.position.y, xn=end_node.position.x, yn=end_node.position.y)


