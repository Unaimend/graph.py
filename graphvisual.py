"""
.. module:: graphvisuals
   :platform: Unix, Windows, Mac
   :synopsis: This module includes classes for drawing graphs and graph algos.
.. moduleauthor:: Thomas Dost(Unaimend@gmail.com)
"""
from graph import Graph, GraphEdge, GraphNode
import random
import tkinter as tk
from typing import List

# TODO enumerate instead of index in for loops
# TODO add an addEdge and addNode to this class
# TODO Wenn kraefte sehr klein sind = 0 setzen wegen floating point ungenauigkeit(gute idee?)
# TODO Dokumentieren welchen Variablen veraendert werden
# TOOD Mutates:
# TODO https://youtu.be/_AEJHKGk9ns?t=19m3s


class GraphVisual:
    #: Seed which is used in the RNG to calc. the nodes positions
    seed = 50

    def __init__(self, canvas: tk.Canvas, width: int, height: int, graph: Graph):
        """
        Ctor. for GraphVisual
        
        :param canvas: The canvas on which the node should be drawn
        :param width: The width of the canvas
        :param height: The height of the canvas
        :param graph: The graph which should be drawn
        """
        self.canvas = canvas
        # Specifies the minimal distance two nodes are allowed to have
        # needed when user places nodes himself
        self.graphNodesMinDistance = 2 * GraphNode.graphNodeRadius
        # Array for the the nodes of the graph(holds GraphNodes objects)
        self.graphNodes: List[GraphNode] = []
        # Array for the the edges of the graph(holds GraphEdge objects)
        self.graphEdges: List[GraphEdge] = []
        # Adjacency list but with nodes instead of integers
        # Im Eintrag node_adjacency_list[x] stehen als nodes alle nodes drinnen die zu x adj. sind.,
        # x ist zurzeit die id der node von der die adjazenz ausgehen soll
        self.node_adjacency_list = []

        # Höhe und Breite des Canvas
        self.width = width
        self.height = height
        self.graph = None

        # Saves the coordinates of the last two clicked notes
        self.clickedNodes = []
        # Specifies whether the node ids should be drawn or not
        self.drawNodeIds = False
        # Helper variable for the node id
        self.nodeCounter = 0
        random.seed(GraphVisual.seed)
        if graph:
            self.graph = graph

        # Converts the graph arrays which represent the graph to
        # arrays which holds objects of Graph.edges and Graph.nodes
        self.int_node_to_graph_node()
        self.generate_adj_list()

        # Generate the edges between the nodes in self.node_adjacency_list
        self.generate_edges()

    @classmethod
    def from_graph(cls, canvas: tk.Canvas, height: int=None, width: int=None, graph: Graph=None):
        """
        :param canvas: The canvas on which the node should be drawn
        :param width: The width of the canvas
        :param heigth: The height of the canvas
        :param graph: The graph which should be drawn
        """
        return cls(canvas=canvas, height=height, width=width, graph=graph)

    def int_node_to_graph_node(self):
        """
        Converts the adj. list which holds integers to a list which holds GraphNodes
        Note that the here generated list doesnt hold information about how the notes are related
        """
        # For every node in the ajd. list add an node to the list which holds the GraphNodes which will be drawn
        for x in self.graph.adjacency_list:
            self.graphNodes.append(
                GraphNode(self.canvas, random.randint(0, self.width),
                          random.randint(0, self.height), self.drawNodeIds, self.nodeCounter))
            self.nodeCounter += 1

    def generate_adj_list(self):
        """
        Generates the adj. list
        """
        self.node_adjacency_list = []
        # TODO Use enumerate
        counter = 0
        for x in self.graph.adjacency_list:
            self.node_adjacency_list.append([])
            for y in x:
                self.node_adjacency_list[counter].append(self.graphNodes[y])
            counter += 1

    def to_pixel_pos(self, x, y):
        pos = {"x": 1 / self.width * x, "y": 1 / self.height * y}
        return pos

    def redraw_nodes(self):
        """
        Deletes all the nodes and their text from the canvas and redraws them again but with updated values
        """
        # TODO Hier sollte eine redraw methode der GraphNode und GraphEdge Klasse genutzt werden
        # Delete nodes and node text from the canvas
        for node in self.graphNodes:
            self.canvas.delete(node.canvas_id)
            self.canvas.delete(node.canvas_text_id)

        alternative_nodelist = []
        # Redraw nodes with updated arguments
        for node in self.graphNodes:
            alternative_nodelist.append(GraphNode(self.canvas, node.position.x, node.position.y,
                                                  self.drawNodeIds, node.id))
        self.graphNodes = alternative_nodelist

    def generate_edges(self):
        """Generates edges between graph nodes, can also be used to redraw edges"""
        # Deletes all old edges from the canvas
        for edges in self.graphEdges:
            self.canvas.delete(edges.id)

        # Init graphEdges with an new array because the old edges are not needed anymore
        self.graphEdges = []

        # Iterate over all nodes(those are GraphNode objects)
        for node in self.graphNodes:
            # Iterate over all nodes which are adjacent to node
            for nodes in self.node_adjacency_list[node.id]:
                # Draw an edge between two nodes
                edge = GraphEdge.from_nodes(canvas=self.canvas, start_node=node, end_node=nodes)
                # Save the edges in an array(for possible redrawing with different settings)
                self.graphEdges.append(edge)

    def set_focus(self, event):
        """
        Text widget doesn't loose focus if another widget is clicked
        this function emulates this behaviour.
        """
        caller = event.widget
        caller.focus_set()

    def redraw_graph(self, event=None):
        """
        Combines methods to redraw all graphical items of the graphs 
        """
        self.canvas.delete(tk.ALL)
        self.redraw_nodes()
        self.generate_adj_list()
        self.generate_edges()

    def change_node_look(self, event=None):
        """Toggles the node look from black dots to whtie circles white text inside"""
        if not self.drawNodeIds:
            self.drawNodeIds = True
        else:
            self.drawNodeIds = False
        self.redraw_graph()


        # def clear_graph(self, event="nothing"):
    #     # clear nodes and edges
    #     self.graphNodes = []
    #     self.graphEdges = []
    #     # reset nodeCounter and also the ids
    #     self.nodeCounter = -1
    #
    # def createNodeAtMousePos(self, event):
    #     is_in_circle = False
    #     # Check for all the nodes if position of the click is in another node
    #     for node in self.graphNodes:
    #         if abs(
    #             (node.x - event.x)) <= GraphNode.graphNodeRadius and abs(
    #                 (node.y - event.y)) <= GraphNode.graphNodeRadius:
    #             is_in_circle = True
    #
    #     is_far_enough = True
    #     # Check for all the nodes if position of the click is far enough away from all the other nodes
    #     for node in self.graphNodes:
    #         if (abs((node.x - event.x)) <= self.graphNodesMinDistance and abs(
    #             (node.y - event.y)) <= self.graphNodesMinDistance):
    #             is_far_enough = False
    #
    #     # If distance is big enough and I clicked not int a circle draw a node
    #     if is_far_enough and not is_in_circle:
    #         self.nodeCounter += 1
    #         self.graphNodes.append(
    #             GraphNode(self.canvas, event.x, event.y,
    #                             self.drawNodeIds, self.nodeCounter))
    #
    #     # If distance is small(in another node) and I clicked in a node remember this node
    #     # to draw an edge
    #     if not is_far_enough and is_in_circle:
    #         self.clickedNodes.append(event.x)
    #         self.clickedNodes.append(event.y)
    #         if len(self.clickedNodes) == 4:
    #             self.graphEdges.append(
    #                 GraphEdge(self.canvas, self.clickedNodes[0],
    #                                 self.clickedNodes[1], self.clickedNodes[2],
    #                                 self.clickedNodes[3]))
    #             self.clickedNodes = []






# TODO Graphen sollte so realisiert werden
#   g = { "a" : ["d"],
#           "b" : ["c"],
#           "c" : ["b", "c", "d", "e"],ddd
#           "d" : ["a", "c"],
#           "e" : ["c"],
#           "f" : []
#         }



