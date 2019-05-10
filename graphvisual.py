"""
.. module:: graphvisuals
   :platform: Unix, Windows, Mac
   :synopsis: This module includes classes for drawing graphs and graph algos.
.. moduleauthor:: Thomas Dost(Unaimend@gmail.com)
"""
import threading
import random
import tkinter as tk
import math
import abc
from typing import List
from graph import Graph, EmptyGraphError
from widgets import NodeInfo
from vector import Vector

import tree as T

# TODO enumerate instead of index in for loops
# TODO add an addEdge and addNode to this class
# TODO Wenn kraefte sehr klein sind = 0 setzen wegen floating point ungenauigkeit(gute idee?)
# TODO Dokumentieren welchen Variablen veraendert werden
# TOOD Mutates:
# TODO https://youtu.be/_AEJHKGk9ns?t=19m3s

#TODO Statt mittepunkt des umkreises die durchscnitspotiion benutzen bzw. gleich varaible programmieren

# TODO VISITOR PATTERN FUER GRAPHNE KRAM DAMIT MAN NICHT AM GRAPPH FUMMELN MUSS


class GraphVisual:
    """
    Class for displaying an undirected graph
    """
    #: Seed which is used in the RNG to calc. the nodes positions
    seed = 50

    def __init__(self, window, canvas: tk.Canvas, width: int = 900, height: int = 1400, graph: Graph = None, draw_circle=False, draw_mid=False, draw_node_ids=False, draw_values=False) -> None:
        """
        Ctor. for GraphVisual
        :parm window: TODO
        :param canvas: The canvas on which the node should be drawn
        :param width: The width of the canvas
        :param height: The height of the canvas
        :param graph: The graph which should be drawn
        :returns: None
        """
        self.canvas: tk.Canvas = canvas
        self.window = window
        # Specifies the minimal distance two nodes are allowed to have
        # needed when user places nodes himself
        self.graph_nodes_min_distance: int = 2 * GraphNode.graphNodeRadius
        # Array for the the nodes of the graph(holds GraphNodes objects)
        self.graph_nodes: List[GraphNode] = []
        # Array for the the edges of the graph(holds GraphEdge objects)
        self.graph_edges: List[GraphEdge] = []
        # Adjacency list but with nodes instead of integers
        # Im Eintrag node_adjacency_list[x] stehen als nodes alle nodes drinnen die zu x adj. sind.,
        # x ist zurzeit die id der node von der die adjazenz ausgehen soll
        self.node_adjacency_list: List[List[GraphNode]] = []

        # Höhe und Breite des Canvas
        self.width: float = width
        self.height: float = height
        self.graph: Graph
        # Saves the coordinates of the last two clicked notes
        self.clicked_nodes: List[GraphNode] = []
        # Specifies whether the node ids should be drawn or not
        self.draw_node_ids: bool = draw_node_ids
        self.draw_values: bool = draw_values
        # Helper variable for the node id
        self.node_counter: int = 0
        random.seed(GraphVisual.seed)
        if not graph:
            raise Exception("A graph must not be None")
        self.graph = graph

        self.current_selected_node: GraphNode
        # Reference to the latest opened NodeInfoWindow
        self.current_info: NodeInfo

        # Converts the graph arrays which represent the graph to
        # arrays which holds objects of Graph.edges and Graph.nodes
        self.int_node_to_graph_node()
        self.generate_adj_list()

        # Generate the edges between the nodes in self.node_adjacency_list
        self.generate_edges()

        min_x, max_x, min_y, max_y = self.find_max_nodes()
        midpoint_x = (max_x-min_x)/2
        midpoint_y = (max_y-min_y)/2

        if draw_circle:
            self.circle = self.canvas.create_oval(min_x, max_y, max_x, min_y, outline="#f11", width=5)
            self.circle_center = self.create_circle(min_x+midpoint_x, max_y-midpoint_y, 20)
        else:
            self.circle = None
            self.circle_center = None
        if draw_mid:
            self.middle_point =  self.create_circle(self.width/2, self.height/2, 20)
        else:
            self.middle_point = None


        self.coordinate_fuckery: Vector = Vector(1, 1)

        # Tree


        if self.graph_nodes != []:
            t = T.Tree(self.graph_nodes[0], self.node_adjacency_list)




    def create_circle(self, x, y, r): #center coordinates, radius
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0, y0, x1, y1, fill="yellow")

    def draw_canvas_mid(self):
        if self.middle_point is not None:
            self.canvas.delete(self.middle_point)
        self.middle_point =  self.create_circle(self.width/2, self.height/2, 20)

    def draw_graph_circle_center(self):
        min_x, max_x, min_y, max_y = self.find_max_nodes()
        midpoint_x = (max_x-min_x)/2
        midpoint_y = (max_y-min_y)/2
        if self.circle is not None:
            self.canvas.delete(self.circle)
        if self.circle_center is not None:
            self.canvas.delete(self.circle_center)

        self.circle = self.canvas.create_oval(min_x, max_y, max_x, min_y, outline="#f11", width=5)
        self.circle_center = self.create_circle(min_x+midpoint_x, max_y-midpoint_y, 20)

    def find_max_nodes(self):
        if len(self.graph_nodes) == 0:
            return 0,0,0,0
        # TODO look at max function kannste da nen lamda mitgeben bringt dads dwas?
        max_x = int(max([(lambda y: y.position.x)(node) for node in self.graph_nodes]))
        min_x = int(min([(lambda y: y.position.x)(node) for node in self.graph_nodes]))

        max_y = int(max([(lambda y: y.position.y)(node) for node in self.graph_nodes]))
        min_y = int(min([(lambda y: y.position.y)(node) for node in self.graph_nodes]))

        return min_x, max_x, min_y, max_y


    def translate_to_mid(self):
        min_x, max_x, min_y, max_y = self.find_max_nodes()
        midpoint_x = (max_x-min_x)/2
        midpoint_y = (max_y-min_y)/2
        diff_x, diff_y = self.width/2 - (min_x+midpoint_x),  (self.height/2) - (max_y-midpoint_y)

        for x in self.graph_nodes:
            x.move(diff_x, diff_y)

        self.generate_adj_list()
        # # update edges between nodes
        self.generate_edges()
        self.redraw_graph()

    def inc_zoomlevel(self, event=None) -> None:
        """
        Calculates the misplacement which comes from zooming(which is scaling) the canvas
        :param event: ---
        :return:
        """
        # pylint: disable=W0613
        self.coordinate_fuckery.x = self.coordinate_fuckery.x * 1.1
        self.coordinate_fuckery.y = self.coordinate_fuckery.y * 1.1

    def dec_zoomlevel(self, event=None) -> None:
        # pylint: disable=W0613
        """
        Calculates the misplacement which comes from zooming(which is scaling) the canvas
        :param event: ---
        :return:
        """
        self.coordinate_fuckery.x = self.coordinate_fuckery.x * 0.9
        self.coordinate_fuckery.y = self.coordinate_fuckery.y * 0.9

    def int_node_to_graph_node(self) -> None:
        """
        Converts the adj. list which holds integers to a list which holds GraphNodes
        Note that the here generated list doesnt hold information about how the notes are related
        """
        # For every node in the ajd. list add an node to the list which holds the GraphNodes which will be drawn
        for i in range(0, len(self.graph.adjacency_list)):
            value = None
            try:
                value = self.graph.values[i]
            except IndexError:
                value = None

            self.graph_nodes.append(
                GraphNode(canvas=self.canvas,
                          x=random.randint(0, int(self.width)),
                          y=random.randint(0, int(self.height)),
                          draw_ids=self.draw_node_ids,
                          id=self.node_counter,
                          colour = "black",
                          draw_values = self.draw_values,
                          value=value))
            self.node_counter += 1




    def generate_adj_list(self) -> None:
        """
        Generates the adj. list
        """
        self.node_adjacency_list: List[List[GraphNode]] = []
        # TODO Use enumerate
        counter = 0
        for x in self.graph.adjacency_list:
            self.node_adjacency_list.append([])
            for y in x:
                self.node_adjacency_list[counter].append(self.graph_nodes[y])
            counter += 1

    def redraw_nodes(self) -> None:
        """
        Deletes all the nodes and their text from the canvas and redraws them again but with updated values
        """
        # TODO Hier sollte eine redraw methode der GraphNode und GraphEdge Klasse genutzt werden
        # Delete nodes and node text from the canvas
        lock = threading.Lock()
        lock.acquire()
        for node in self.graph_nodes:
            self.canvas.delete(node.canvas_id)
            self.canvas.delete(node.canvas_text_id)
            self.canvas.delete(node.canvas_value_id)

        alternative_nodelist = []
        # Redraw nodes with updated arguments
        for node in self.graph_nodes:
            alternative_nodelist.append(GraphNode(canvas =self.canvas,
                                                  x = node.position.x,
                                                  y =node.position.y,
                                                  draw_ids = self.draw_node_ids,
                                                  id = node.id,
                                                  colour = node.colour,
                                                  node_fill_colour = node.node_fill_colour,
                                                  draw_values = self.draw_values,
                                                  value = node.value
            ))
        self.graph_nodes = alternative_nodelist
        lock.release()

    def generate_edges(self) -> None:
        """Generates edges between graph nodes, can also be used to redraw edges"""
        # Deletes all old edges from the canvas
        for edges in self.graph_edges:
            edges.delete()

        # Init graphEdges with an new array because the old edges are not needed anymore
        self.graph_edges = []

        # Iterate over all nodes(those are GraphNode objects)
        for node in self.graph_nodes:
            # Iterate over all nodes which are adjacent to node
            for nodes in self.node_adjacency_list[node.id]:
                # Draw an edge between two nodes
                edge = DirectedGraphEdge(canvas=self.canvas, start_node=node, end_node=nodes)
                # Save the edges in an array(for possible redrawing with different settings)
                # TODO Ich haette gerne jede Kante nur einmal in der Liste, da ich micht nicht sicher bin
                # TODO welche Auswirkungen das auf den Algorithmus von Fruchterman-Reingold hat
                # TODO aber es muesste mathematisch korrekt sein das jede Kante 2mal vorkomment
                # TODO da sie ja eig. versch. Kanten darstellen
                self.graph_edges.append(edge)

    @staticmethod
    def set_focus(event=None) -> None:
        """
        Text widget doesn't loose focus if another widget is clicked
        this function emulates this behaviour.
        """
        print("Set focus got called")
        caller = event.widget
        caller.focus_set()

    def redraw_graph(self, event=None) -> None:
        # pylint: disable=W0613
        """
        Combines methods to redraw all graphical items of the graphs
        """
        self.redraw_nodes()

        self.generate_adj_list()
        self.generate_edges()

    def change_node_look(self, event=None) -> None:
        # pylint: disable=W0613
        """Toggles the node look from black dots to white circles white text inside and the other way around"""
        self.draw_node_ids = not bool(self.draw_node_ids)
        # for node in self.graph_nodes:
        #     print(node.node_fill_colour)
        self.redraw_graph()

    def select_node(self, event) -> None:
        """Selects a node and opens a window with important informatoion about the selected node"""
        # TODO DAS MUSS ALLES NEU
        if not self.graph_nodes:
            raise EmptyGraphError
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        # Damit die if abfrage weiter unten(current_smallest_dist < 15) bei einer leeren Liste false ist.
        current_smallest_dist: float = 16

        nearest_node = self.graph_nodes[0]
        distance_dic = {}
        for node in self.graph_nodes:
            x_offset = (nearest_node.position.x - x) ** 2
            y_offset = (nearest_node.position.y - y) ** 2
            current_smallest_dist = math.sqrt(x_offset + y_offset)
            adjusted_node_pos = Vector(0, 0)
            # adjusted_node_pos.x = node.position.x
            # adjusted_node_pos.y = node.position.y
            adjusted_node_pos.x = (node.position.x-self.width/2)*self.coordinate_fuckery.x+self.width/2
            adjusted_node_pos.y = (node.position.y-self.height/2)*self.coordinate_fuckery.y+self.height / 2

            x_offset = (adjusted_node_pos.x - x) ** 2
            y_offset = (adjusted_node_pos.y - y) ** 2
            dist = math.sqrt(x_offset + y_offset)
            # print("OFF", x_offset, "\ ", y_offset, '\ ', dist, "|", current_smallest_dist)
            if dist <= current_smallest_dist:
                nearest_node = node
                distance_dic[dist] = node.canvas_text_id

        nearest_node_distance: float = min(distance_dic.keys())
        nearest_node_canvas_text_id = distance_dic[nearest_node_distance]
        if nearest_node_distance < 15:
            # Node die ausgewaehlt wurde rot farben
            self.canvas.itemconfigure(nearest_node_canvas_text_id, fill="red")
            nearest_node.colour = "red"

            self.current_selected_node = nearest_node
            # Infofenster erstellen und oeffnen
            self.current_info = NodeInfo(self.window, self.current_selected_node,
                                         self.node_adjacency_list[self.current_selected_node.id])
            for node in self.graph_nodes:
                # Alle nodes die nicht ausgeaehlt wurden schwarz faerben
                if node != self.current_selected_node:
                    node.colour = "black"
                    self.canvas.itemconfigure(node.canvas_text_id, fill=node.node_fill_colour)
        else:
            # Falls keine Node ausgewaehlt wurde sollen alle Nodes schwarz sein
            self.current_selected_node = None
            for node in self.graph_nodes:
                node.colour = "black"
                self.canvas.itemconfigure(nearest_node.canvas_text_id, fill=node.node_fill_colour)


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
    #             (node.position.x - event.x)) <= GraphNode.graphNodeRadius and abs(
    #                 (node.position.y - event.y)) <= GraphNode.graphNodeRadius:
    #             is_in_circle = True
    #
    #     is_far_enough = True
    #     # Check for all the nodes if position of the click is far enough away from all the other nodes
    #     for node in self.graphNodes:
    #         if (abs((node.position.x - event.x)) <= self.graphNodesMinDistance and abs(
    #             (node.position.y - event.y)) <= self.graphNodesMinDistance):
    #             is_far_enough = False
    #
    #     # If distance is big enough and I clicked not int a circle draw a node
    #     if is_far_enough and not is_in_circle:
    #         self.nodeCounter += 1
    #         self.graphNodes.append(
    #             GraphNode(self.canvas, event.x, event.y, self.drawNodeIds, self.nodeCounter, "blue"))
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


class GraphNode:
    """
    Class which represents a node in a graph
    """
    #: Radius of the nodes
    graphNodeRadius = 6 # TODO Save and load seed for current graph so you can draw the "same" graph if you want to

    def __init__(self, canvas: tk.Canvas, x: float, y: float, draw_ids: bool, id: int, draw_values, value = 1, colour="black", node_fill_colour="black") -> None:
        """
        :param canvas: The canvas on which the node should be drawn
        :param x:
        :param y:
        :param draw_ids: bool
        :param id: The id which should be drawn in node
        :param colour
        """
        #: Canvas position for the node
        self.position = Vector(x, y)
        #: The canvas on which the node should be drawn(for multi-canvas support)
        self.canvas = canvas
        #: The id that will be drawn "in the node"
        self.id = id
        #: The id to identify this node on the canvas
        self.canvas_id = "-1"
        #: Id to identify the text of this node
        self.canvas_text_id = "-1"
        self.canvas_value_id  = "-1"
        self.colour = colour
        self.node_fill_colour = node_fill_colour
        """
        Boolean which determines if the node is represented through a black dot or
        through a circle with a number inside
        """
        self.draw_ids = draw_ids
        self.value = value
        self.draw_values = draw_values
        # TODO Magic number ersetzen

        left_corner = self.position - Vector(self.graphNodeRadius, self.graphNodeRadius )
        right_corner = self.position + Vector(self.graphNodeRadius, self.graphNodeRadius)
        if self.draw_ids:
            self.canvas_id = canvas.create_oval(left_corner.x,
                                                left_corner.y,
                                                right_corner.x,
                                                right_corner.y, fill="white")
            text_id_pos = Vector(self.position.x + 2, self.position.y + 2)
            self.canvas_text_id = canvas.create_text(text_id_pos.x, text_id_pos.y, text=self.id, fill=self.colour)
        elif self.draw_values:
            self.canvas_id = canvas.create_oval(left_corner.x,
                                                left_corner.y,
                                                right_corner.x,
                                                right_corner.y, fill="white")
            text_id_pos = Vector(self.position.x + 2, self.position.y + 2)
            self.canvas_value_id = canvas.create_text(text_id_pos.x, text_id_pos.y, text=self.value, fill=self.colour)
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


class GraphEdge:
    """
    This class represents a graph edge
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self, canvas: tk.Canvas, start_node: GraphNode, end_node: GraphNode) -> None:
        """
        :param canvas: The canvas on which the edge should be drawn
        :type canvas: tk.Canvas
        :param start_node: The lines starting node
        :param end_node: The lines ending node
        """
        # Start der Kanten
        self.start = Vector(start_node.position.x, start_node.position.y)
        # Ende der Kanten
        self.end = Vector(end_node.position.x, end_node.position.y)
        self.start_node = start_node
        self.end_node = end_node
        self.canvas = canvas
        # Create line and save id
        self.id = None
        self.radius = 5
        self.midpoint = Vector(self.start.x - (self.start.x-self.end.x)/2, self.start.y - (self.start.y-self.end.y)/2)
        self.normal_end_point_dir: Vector = Vector(self.end.y-self.start.y, -(self.end.x-self.start.x))
        self.normal_end_point_dir = self.normal_end_point_dir.to_unit() * 50
        self.normal_end_point: Vector = self.midpoint + self.normal_end_point_dir
        # self.mid = canvas.create_oval(self.midpoint.x-self.radius, self.midpoint.y-self.radius, self.midpoint.x+self.radius, self.midpoint.y+self.radius)
        # self.normal = canvas.create_line(self.midpoint.x, self.midpoint.y, self.normal_end_point.x, self.normal_end_point.y,  fill='black')

    @abc.abstractmethod
    def delete(self):
        return


class UndirectedGraphEdge(GraphEdge):
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
        super().__init__(canvas, start_node, end_node)
        self.id = canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, smooth=True)

    def delete(self):
        self.canvas.delete(self.id)
        self.canvas.delete(self.mid)
        self.canvas.delete(self.normal)


class DirectedGraphEdge(GraphEdge):
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
        super().__init__(canvas, start_node, end_node)
        # TODO Das kann kein guter code sein
        self.id = canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, fill='black')

        self.arrow = EdgeArrow(canvas, self)

    def delete(self):
        self.canvas.delete(self.id)
        # self.canvas.delete(self.arrow.id)
        # self.canvas.delete(self.normal)
        # self.canvas.delete(self.mid)


class EdgeArrow:
    def __init__(self, canvas: tk.Canvas, edge: DirectedGraphEdge):
        self.canvas: tk.Canvas = canvas
        self.edge: GraphEdge = edge
        self.pos: Vector = Vector(self.edge.end_node.position.x, self.edge.end_node.position.y)
        line_direction: Vector = self.edge.end-self.edge.start
        line_direction = line_direction.to_unit() * 10
        point1: Vector = self.pos-line_direction*2
        point2: Vector = point1 + self.edge.normal_end_point_dir*0.1
        point3: Vector = Vector(point1.x + line_direction.x, point1.y + line_direction.y)
        point4: Vector = point1 - self.edge.normal_end_point_dir*0.1
        point5: Vector = point1

        # self.id = self.canvas.create_polygon([point1.x, point1.y, point2.x, point2.y, point3.x, point3.y, point4.x, point4.y, point5.x, point5.y], fill="green")


# TODO Graphen sollte so realisiert werden
#   g = { "a" : ["d"],
#           "b" : ["c"],
#           "c" : ["b", "c", "d", "e"],ddd
#           "d" : ["a", "c"],
#           "e" : ["c"],
#           "f" : []
#         }
