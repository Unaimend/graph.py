from typing import List
import json
import random
import Vector
import tkinter as tk



#typedefs
AdjacencyList = List[List[int]]
AdjacencyMatrix = List[List[int]]


class GraphNode:
    graphNodeRadius = 12

    # TODO  x und y sollte in einem Vektor verpackt werden
    # TODO Save and load seed for current graph so you can draw the "same" graph if you want to

    def __init__(self, canvas, x, y, text, drawIds, id):
        self.x = x
        self.y = y
        self.text = text
        self.canvas = canvas
        self.id = id
        self.canvas_id = 0
        self.canvas_text_id = "-1"
        if drawIds:
            self.canvas_id = canvas.create_oval(x - self.graphNodeRadius / 1.5, y - self.graphNodeRadius / 1.5,
                           x + self.graphNodeRadius,
                           y + self.graphNodeRadius,
                           fill="white")
        else:
            self.canvas_id =  canvas.create_oval(x - self.graphNodeRadius / 1.5, y - self.graphNodeRadius / 1.5,
                           x + self.graphNodeRadius,
                           y + self.graphNodeRadius,
                           fill="black")

        self.canvas_text_id = canvas.create_text(self.x+2, self.y+2, text=self.id)

    def move(self, x,y):
        self.x += x
        self.y += y
        # TODO Nur einmal am Ende moven
        self.canvas.move(self.canvas_id, x, y)
        self.canvas.move(self.canvas_text_id, x,y)


class Graph:
    def __init__(self, width: int=None, height: int=None, filepath: str=None, adjacency_list: AdjacencyList=None,
                 adjacency_matrix: AdjacencyMatrix=None):
        self.filepath = filepath
        self.adjacency_list = None
        self.adjacencyMatrix = None
        self.vertice_count = None
        self.height = height
        self.width = width
        # Load from a file

        #TODO in try catch verpacken
        #https://stackoverflow.com/questions/1369526/what-is-the-python-keyword-with-used-for
        if filepath:
            print("Loading from " + filepath)
            f = open(self.filepath, "r")
            self.adjacency_list = json.load(f)
            f.close()
            self.vertice_count = len(self.adjacency_list)
            print(self.adjacency_list)
            # print("%s with length %s" % (''.join(self.adjacency_list), str(self.vertice_count)))
        # Load from an adjacency list
        elif adjacency_list:
            self.adjacency_list = adjacency_list
        # Load from adjacency matrix
        elif adjacency_matrix:
            self.adjacency_matrix = adjacency_matrix
        else:
            print("TODO exception")

    @classmethod
    def from_file(cls, path):
        return cls(filepath=path)

    @classmethod
    def from_adjacency_list(cls, adjacency_list):
        return cls(adjacency_list=adjacency_list)

    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix):
        return cls(adjacency_matrix=adjacency_matrix)

    def adjacent_to(self, node: GraphNode=None):
        return self.adjacency_list[node.id]








class GraphEdge():
    def __init__(self, canvas, x0, y0, xn, yn):
        # Start der Kante
        self.start = Vector.Vector(x0, y0)

        # Ender der Katen
        self.end = Vector.Vector(xn, yn)

        # Debugausgaben
        # print("x0", self.x0, "y0", self.y0)
        # print("endX", self.endX, "endY", self.endY)
        self.id = canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, smooth=True)



