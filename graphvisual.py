import tkinter as tk
import Vector as Vector
import Graph as Graph
import random
import tkinter as tk
import math
import json

import Eades


class GraphVisual:
    def __init__(self, canvas, width, height, graph):
        self.canvas = canvas
        # Specifies the minimal distance two nodes are allowed to have
        self.graphNodesMinDistance = 2*Graph.GraphNode.graphNodeRadius
        # Array for the the nodes of the graph
        self.graphNodes = []
        # Array for the the edges of the graph
        self.graphEdges = []

        #Adjacency list but with nodes instead of integers
        self.node_adjacency_list = []


        # Höhe und Breite des Canvas
        self.width = width
        self.height = height
        self.graph = None


        # Saves the coordinates of the last two clicked notes
        self.clickedNodes = []
        # Specifies whether the node ids should be drawn or not
        self.drawNodeIds = False;
        # Helper variable for the node id
        self.nodeCounter = 0;


        if graph:
            self.graph = graph

        # Wasn das fuern ne datenstruktur bzw whyyyy ddoes this work
        self.int_adj_to_node_adj()
        self.int_edges_to_node_edges()
        self.generate_edges()
        #TODO Algorithmus zum Zeichen von Graphen anschauen (graph drawing wikipedia)


        print(self.width,self.height)
        # Array which represents the isConnectedTo relationship
        # self.adjacencyList = [
        #     [1,2],
        #     [0],
        #     [2]
        # ]



    #Methoden um einen Graphen von einem vordefinierten Graphen zu zeichnen
    @classmethod
    def fromGraph(cls,cavas, height: int=None, width: int=None, graph :Graph=None):
        return cls(canvas=cavas, height=height, width=width, graph=graph)


    def int_adj_to_node_adj(self):
        for x in self.graph.adjacency_list:
            self.graphNodes.append(Graph.GraphNode(self.canvas, random.randint(0, self.width),
                                                   random.randint(0, self.height),
                                                   "black", self.drawNodeIds, self.nodeCounter))
            self.nodeCounter+=1

    #Im Eintrag node_adjacency_list[x] stehen als nodes alle nodes drin die zu x adj. sind.
    def int_edges_to_node_edges(self):
        counter = 0
        for x in self.graph.adjacency_list:
            self.node_adjacency_list.append([])
            for y in x:
                self.node_adjacency_list[counter].append(self.graphNodes[y])
            counter += 1




    def toPixelPos(self, x, y):
        pos = {"x": 1 / self.width * x, "y": 1 / self.height * y}
        return pos


    def changeNodeLook(self, event="nothing"):
        self.canvas.delete("all")


        if not self.drawNodeIds:
            self.drawNodeIds = True
        else:
            self.drawNodeIds = False;

        self.redrawNodes()
        self.graphEdges()

    def redrawNodes(self):
        alternativNodeList = []
        for node in self.graphNodes:
            alternativNodeList.append(Graph.GraphNode(self.canvas, node.x,
                                                node.y, "", self.drawNodeIds, node.id))
        self.graphNodes = alternativNodeList

    def generate_edges(self):

        for edges in self.graphEdges:
            self.canvas.delete(edges.id)

        self.graphEdges = []

        for node in self.graphNodes:
            for nodes in self.node_adjacency_list[node.id]:
                edge = Graph.GraphEdge(canvas=self.canvas, x0=node.x, y0=node.y,xn=nodes.x, yn=nodes.y )
                self.graphEdges.append(edge)

    # def redrawEdges(self):
    #     alternativEdgeList = []
    #     for edge in self.graphEdges:
    #         alternativEdgeList.append(Graph.GraphEdge(self.canvas, edge.start.x,
    #                                             edge.start.y, edge.end.x, edge.end.y))
    #     self.graphEdges = alternativEdgeList

    def clearGraph(self, event="nothing"):
       # clear canvas

       # clear nodes and edges
       self.graphNodes = []
       self.graphEdges = []
       # reset nodeCounter and also the ids
       self.nodeCounter = -1





    def createNodeAtMousePos(self,event):
        isInCircle = False
        for node in self.graphNodes:
            if (abs((node.x - event.x)) <= Graph.GraphNode.graphNodeRadius
                and abs((node.y - event.y)) <= Graph.GraphNode.graphNodeRadius):
                isInCircle = True;

        isFarEnough = True
        for node in self.graphNodes:
            if(abs((node.x - event.x)) <= self.graphNodesMinDistance
               and abs((node.y - event.y)) <= self.graphNodesMinDistance):
                isFarEnough = False;

        if isFarEnough and not isInCircle:
            self.nodeCounter += 1
            self.graphNodes.append(Graph.GraphNode(self.canvas, event.x, event.y,
                                             "black", self.drawNodeIds, self.nodeCounter))

        if not isFarEnough and isInCircle:
            self.clickedNodes.append(event.x)
            self.clickedNodes.append(event.y)
            if (len(self.clickedNodes) == 4):
                self.graphEdges.append(Graph.GraphEdge(self.canvas, self.clickedNodes[0],
                                                 self.clickedNodes[1], self.clickedNodes[2],
                                                 self.clickedNodes[3]))
                self.clickedNodes = []


class Window:
    def __init__(self, root):
        self.root = root

        # Init. canvas
        self.canvas = tk.Canvas(self.root, relief=tk.SUNKEN, bd=4,
                                width=1200, height=800,  background='white')

        # Sth. with the layout
        self.canvas.pack()

        test = Graph.Graph(width=1200, height=800, filepath="graph.json")

        self.graph = GraphVisual.fromGraph(cavas=self.canvas, width=1200, height=800, graph=test)

        # id = self.graph.canvas.create_oval(500, 500, 10, 10, tags="MOVE")
        # print(id)

        # # Mouse and keyboard bindings
        # self.root.bind("<Button 1>", self.graph.createNodeAtMousePos)
        # self.root.bind("<g>", self.graph.changeNodeLook)
        # self.root.bind("<c>", self.graph.clearGraph)


        Eades.Eades.graph = self.graph


        self.root.bind("<d>",self.doEades )

        print("Edges", self.graph.graphEdges)



        #ddddddadd
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


    def run(self):
        self.root.mainloop()

    def move(self, event="nothing"):
        self.graph.graphNodes[0].move(10, 0)

    def doEades(self, event="nothing"):
        for x in range(0,100):
            Eades.Eades.calculate_attractive_force_for_all_nodes_and_move_accordingly()
            Eades.Eades.calculate_repelling_force_for_all_nodes_and_move_accordingly()

        self.graph.generate_edges()




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
