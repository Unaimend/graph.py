import tkinter as tk
import Vector as Vector
import graph as Graph
import random
import tkinter as tk
import math
import json
import profile

import Eades

import time

# TODO enumerate instead of index in for loops



class OpenGraphDialog:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.wm_title("Open new graph")
        l = tk.Label(self.window, text="This is window")
        l.pack(side="top", fill="both", expand=True, padx=100, pady=100)

        # TODO Auswahl der graph.json
        # TODO Auswahl des Layout Algorithmuses
        # TODO Seed auswahl fuer den RNG


class GraphVisual:
    seed = 25

    def __init__(self, canvas, width, height, graph):
        random.seed(GraphVisual.seed)
        self.canvas = canvas
        # Specifies the minimal distance two nodes are allowed to have
        # TODO eades doesnt implement this min. distance atm.
        # TODO Solution: Compare the distance from every node to every other node(n^2 runtime)
        self.graphNodesMinDistance = 2 * Graph.GraphNode.graphNodeRadius

        # Array for the the nodes of the graph(holds Graph.GraphEdge objects)
        self.graphNodes = []
        # Array for the the edges of the graph(holds Graph.GraphEdge objects)
        self.graphEdges = []
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

        if graph:
            self.graph = graph

        # TODO whyyyy ddoes this work
        self.int_adj_to_node_adj()
        self.int_edges_to_node_edges()

        # Generate the edges between the nodes in self.node_adjacency_list
        self.generate_edges()

    @classmethod
    def fromGraph(cls,
                  canvas,
                  height: int=None,
                  width: int=None,
                  graph: Graph=None):
        return cls(canvas=canvas, height=height, width=width, graph=graph)

    def int_adj_to_node_adj(self):

        for x in self.graph.adjacency_list:
            self.graphNodes.append(
                Graph.GraphNode(self.canvas,
                                random.randint(0, self.width),
                                random.randint(0, self.height),
                                self.drawNodeIds, self.nodeCounter))
            self.nodeCounter += 1

    def int_edges_to_node_edges(self):
        counter = 0
        for x in self.graph.adjacency_list:
            self.node_adjacency_list.append([])
            for y in x:
                self.node_adjacency_list[counter].append(self.graphNodes[y])
            counter += 1

    def to_pixel_pos(self, x, y):
        pos = {"x": 1 / self.width * x, "y": 1 / self.height * y}
        return pos

    def change_node_look(self, event="nothing"):
        # TODO BUUUUUG
        # TODO Irwas wird hier nicht richtig gelöscht :(
        if not self.drawNodeIds:
            self.drawNodeIds = True
        else:
            self.drawNodeIds = False

        self.redraw_nodes()
        # self.generate_edges()

    def redraw_nodes(self):
        # Delete nodes from the canvas
        for node in self.graphNodes:
            self.canvas.delete(node.id)

        alternative_nodelist = []
        # Redraw nodes with updated arguments
        for node in self.graphNodes:
            alternative_nodelist.append(
                Graph.GraphNode(self.canvas, node.position.x, node.position.y,
                                "", self.drawNodeIds, node.id))
        self.graphNodes = alternative_nodelist

    def generate_edges(self):
        """Generates edges between graph nodes"""
        # Deletes all old edges from the canvas
        for edges in self.graphEdges:
            self.canvas.delete(edges.id)
        # Init graphEdges with an new array because the old edges are not needed anymore
        self.graphEdges = []
        # Iterate over all nodes(those are Graph.GraphNode objects)
        for node in self.graphNodes:
            # Iterate over all nodes which are adjacent to node
            for nodes in self.node_adjacency_list[node.id]:
                # Draw an edge between two nodes
                edge = Graph.GraphEdge(
                    canvas=self.canvas,
                    x0=node.position.x,
                    y0=node.position.y,
                    xn=nodes.position.x,
                    yn=nodes.position.y)
                # Save the edges in an array(for possible redrawing with different settings)
                self.graphEdges.append(edge)

    def clear_graph(self, event="nothing"):
        # clear nodes and edges
        self.graphNodes = []
        self.graphEdges = []
        # reset nodeCounter and also the ids
        self.nodeCounter = -1

    def createNodeAtMousePos(self, event):
        is_in_circle = False
        # Check for all the nodes if position of the click is in another node
        for node in self.graphNodes:
            if abs(
                (node.x - event.x)) <= Graph.GraphNode.graphNodeRadius and abs(
                    (node.y - event.y)) <= Graph.GraphNode.graphNodeRadius:
                is_in_circle = True

        is_far_enough = True
        # Check for all the nodes if position of the click is far enough away from all the other nodes
        for node in self.graphNodes:
            if (abs((node.x - event.x)) <= self.graphNodesMinDistance and abs(
                (node.y - event.y)) <= self.graphNodesMinDistance):
                is_far_enough = False

        # If distance is big enough and I clicked not int a circle draw a node
        if is_far_enough and not is_in_circle:
            self.nodeCounter += 1
            self.graphNodes.append(
                Graph.GraphNode(self.canvas, event.x, event.y,
                                self.drawNodeIds, self.nodeCounter))

        # If distance is small(in another node) and I clicked in a node remember this node
        # to draw an edge
        if not is_far_enough and is_in_circle:
            self.clickedNodes.append(event.x)
            self.clickedNodes.append(event.y)
            if len(self.clickedNodes) == 4:
                self.graphEdges.append(
                    Graph.GraphEdge(self.canvas, self.clickedNodes[0],
                                    self.clickedNodes[1], self.clickedNodes[2],
                                    self.clickedNodes[3]))
                self.clickedNodes = []


class Window:
    CANVAS_WIDTH = 1200
    CANVAS_HEIGHT = 800
    EADES = True

    def __init__(self, root):
        self.root = root
        self.graph = None
        # self.root.geometry("1400x800")
        # Init. canvas
        self.canvas = tk.Canvas(
            self.root,
            relief=tk.SUNKEN,
            bd=4,
            width=Window.CANVAS_WIDTH,
            height=Window.CANVAS_HEIGHT,
            background='white')

        # Sth. with the layout(row = y)
        self.canvas.pack()

        # Show eades constant choices only if user selected eades as algorithm
        if Window.EADES:
            self.init_eades_constant_widgets()
        self.load_graph("graph.json")
        # TODO Nur machen wenn der Dateipfad zum Graphen nicht leer ist
        self.graph_visuals = GraphVisual.fromGraph(
            canvas=self.canvas,
            width=Window.CANVAS_WIDTH,
            height=Window.CANVAS_HEIGHT,
            graph=self.graph)
        # Dem Algorithmus eine Zeichenflaeche zuweisen mit der er arbeiten soll
        Eades.Eades.graph_visuals = self.graph_visuals

        self.root.bind("<d>", self.do_eades)
        self.root.bind("<f>", self.do_eades_old)
        # self.root.bind("<g>", self.graph_visuals.change_node_look)
        self.root.bind("<n>", self.open_new_graph)

    def run(self):
        self.root.mainloop()

    # TODO Das moven is slooooow as fuck
    # TODO 2. Modosu implementieren indem erst der Original Graph gezeichnet wird, dann wird das Canvas gecleared
    # TODO dann werden die neuen position berechnet und dann werden neue Nodes mit den neuen Koordinaten plaziertd
    def do_eades(self, event="nothing"):
        start = time.time()
        for x in range(0, 100):
            Eades.Eades.calculate_attractive_force_for_all_nodes_and_move_accordingly()
            Eades.Eades.calculate_repelling_force_for_all_nodes_and_move_accordingly()
        end = time.time()
        print("Elapsed Time", end - start)
        self.graph_visuals.generate_edges()

    def do_eades_old(self, event="nothing"):
        start = time.time()
        for x in range(0, 100):
            Eades.Eades.calculate_attractive_force_for_all_nodes_and_move_accordingly_old()
            Eades.Eades.calculate_repelling_force_for_all_nodes_and_move_accordingly_old()
        end = time.time()
        print("Old elapsed Time", end - start)
        self.graph_visuals.generate_edges()

    def open_new_graph(self, event="nothing"):
        current_instance = OpenGraphDialog(self.root)

    def load_graph(self, filepath):
        self.graph = Graph.Graph.from_file(
            width=Window.CANVAS_WIDTH,
            height=Window.CANVAS_HEIGHT,
            filepath=filepath)

    def init_eades_constant_widgets(self):
        l1 = tk.Label(self.root, text="c1")
        l1.pack(side=tk.LEFT)

        # Textfield for ... Eades constant
        t1 = tk.Text(
            self.root, height=1, width=5, relief="sunken", borderwidth=2)
        t1.pack(side=tk.LEFT)
        t1.insert(tk.END, Eades.Eades.c1)

        l2 = tk.Label(self.root, text="c2")
        l2.pack(side=tk.LEFT)

        # Textfield for ... Eades constant
        t2 = tk.Text(
            self.root, height=1, width=5, relief="sunken", borderwidth=2)
        t2.pack(side=tk.LEFT)
        t2.insert(tk.END, Eades.Eades.c2)

        l3 = tk.Label(self.root, text="c3")
        l3.pack(side=tk.LEFT)

        # Textfield for ... Eades constant
        t3 = tk.Text(
            self.root, height=1, width=5, relief="sunken", borderwidth=2)
        t3.pack(side=tk.LEFT)
        t3.insert(tk.END, Eades.Eades.c3)

        l4 = tk.Label(self.root, text="c4")
        l4.pack(side=tk.LEFT)

        # Textfield for ... Eades constant
        t4 = tk.Text(
            self.root, height=1, width=5, relief="sunken", borderwidth=2)
        t4.pack(side=tk.LEFT)
        t4.insert(tk.END, Eades.Eades.c4)


# TODO Graphen sollte so realisiert werden
#   g = { "a" : ["d"],
#           "b" : ["c"],
#           "c" : ["b", "c", "d", "e"],ddd
#           "d" : ["a", "c"],
#           "e" : ["c"],
#           "f" : []
#         }

window = Window(tk.Tk())
window.run()

# profile.run(window.run())

#
# test = list()
# test.append([1])
# test.append([2])
# test.append([3])
#
#
#
# f = open("1graph.json", "w")
#
# json.dump(test,f)
# f.close()
# f = open("1graph.json", "r")
# a = json.load(f)
# print(a)
# f.close()

# [
# 	[1,2],
# 	[0,2],
# 	[1,0],
#     [],
#     []
# ]

# ddddddadd
# self.menubar = tk.Menu(self.root)
# # File menu
# self.filemenu = tk.Menu(self.menubar, tearoff=0)
# self.filemenu.add_separator()
# self.filemenu.add_command(label="Exit")
# self.menubar.add_cascade(label="File", menu=self.filemenu)
#
# # View menu
# self.viewmenu = tk.Menu(self.menubar, tearoff=0)
# self.viewmenu.add_command(label="Toggle ids     (g)", c®ommand=self.changeNodeLook)
# self.viewmenu.add_command(label="Clear canvas   (cg)", command=self.clearCanvas)
# self.menubar.add_cascade(label="View", menu=self.viewmenu)
#
# self.root.config(menu=self.menubar)
