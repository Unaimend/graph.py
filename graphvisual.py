
import graph as Graph
import random
import tkinter as tk

# TODO enumerate instead of index in for loops



class GraphVisual:
    seed = 25

    def __init__(self, canvas, width, height, graph):
        random.seed(GraphVisual.seed)
        self.canvas = canvas
        # Specifies the minimal distance two nodes are allowed to have
        # needed when user places nodes himself
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

        # Converts the graph arrays which represent the graph to
        # arrays which holds objects of Graph.edges and Graph.nodes
        self.int_node_to_graph_node()
        self.generate_adj_list()

        # Generate the edges between the nodes in self.node_adjacency_list
        self.generate_edges()

    @classmethod
    def from_graph(cls,
                   canvas,
                   height: int=None,
                   width: int=None,
                   graph: Graph=None):
        return cls(canvas=canvas, height=height, width=width, graph=graph)

    def int_node_to_graph_node(self):
        for x in self.graph.adjacency_list:
            self.graphNodes.append(
                Graph.GraphNode(self.canvas,
                                random.randint(0, self.width),
                                random.randint(0, self.height),
                                self.drawNodeIds, self.nodeCounter))
            self.nodeCounter += 1

    def generate_adj_list(self):
        self.node_adjacency_list = []
        counter = 0
        for x in self.graph.adjacency_list:
            self.node_adjacency_list.append([])
            for y in x:
                self.node_adjacency_list[counter].append(self.graphNodes[y])
            counter += 1

    def to_pixel_pos(self, x, y):
        pos = {"x": 1 / self.width * x, "y": 1 / self.height * y}
        return pos

    # TODO Nodes in node_adjacency_list werden nie geupdated werden sie jetzt(Unbedingt in commit)
    def redraw_nodes(self):
        # Delete nodes and node text from the canvas
        for node in self.graphNodes:
            self.canvas.delete(node.canvas_id)
            self.canvas.delete(node.canvas_text_id)

        alternative_nodelist = []
        # Redraw nodes with updated arguments
        for node in self.graphNodes:
            alternative_nodelist.append( Graph.GraphNode(self.canvas, node.position.x, node.position.y,
                                                         self.drawNodeIds, node.id))
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
                # print("Start", node.id, node.position.x, node.position.y, "End", nodes.id,nodes.position.x, nodes.position.y)
                edge = Graph.GraphEdge.from_nodes(canvas=self.canvas,start_node=node,end_node=nodes)
                # Save the edges in an array(for possible redrawing with different settings)
                self.graphEdges.append(edge)

    # Text widget doesn't loose focus if another widget is clicked
    # this function emulates this behaviour.
    def set_focus(self, event):
        caller = event.widget
        caller.focus_set()

    def redraw_graph(self, event=None):
        self.canvas.delete(tk.ALL)
        self.redraw_nodes()
        self.generate_adj_list()
        self.generate_edges()

    def change_node_look(self, event="nothing"):
        if not self.drawNodeIds:
            self.drawNodeIds = True
        else:
            self.drawNodeIds = False
        # NOTE EIg. sollte es hier reichen nur die Nodes neu zu zeichnen
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
    #             (node.x - event.x)) <= Graph.GraphNode.graphNodeRadius and abs(
    #                 (node.y - event.y)) <= Graph.GraphNode.graphNodeRadius:
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
    #             Graph.GraphNode(self.canvas, event.x, event.y,
    #                             self.drawNodeIds, self.nodeCounter))
    #
    #     # If distance is small(in another node) and I clicked in a node remember this node
    #     # to draw an edge
    #     if not is_far_enough and is_in_circle:
    #         self.clickedNodes.append(event.x)
    #         self.clickedNodes.append(event.y)
    #         if len(self.clickedNodes) == 4:
    #             self.graphEdges.append(
    #                 Graph.GraphEdge(self.canvas, self.clickedNodes[0],
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
