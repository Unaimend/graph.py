import tkinter as tk

class Vector():
    def __init__(self, x, y):
        self.x = x;
        self.y = y;

class Window:
    def __init__(self, root):
        self.root = root

        # Init. canvas
        self.canvas = tk.Canvas(self.root, relief=tk.SUNKEN, bd=4,
                                width=1200, height=800,  background='white')
        # Sth. with the layout
        self.canvas.pack()

        # Mouse and keyboard bindings
        self.root.bind("<Button 1>", self.createNodeAtMousePos)
        self.root.bind("<g>", self.changeNodeLook)
        self.root.bind("<c>", self.clearCanvas)

        # Specifies the minimal distance two nodes are allowed to have
        self.graphNodesMinDistance = 2*GraphNode.graphNodeRadius;

        # Array for the the nodes of the graph
        self.graphNodes = []
        # Array for the the edges of the graph
        self.graphEdges = []
        # Array which represents the isConnectedTo relationship
        self.adjacencyList = []
        # Saves the coordinates of the last two clicked notes
        self.clickedNodes = []
        # Specifies whether the node ids should be drawn or not
        self.drawNodeIds = False;
        # Helper variable for the node ids
        self.nodeCounter = 0;


        self.menubar = tk.Menu(self.root)
        # File menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit")
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # View menu
        self.viewmenu = tk.Menu(self.menubar, tearoff=0)
        self.viewmenu.add_command(label="Toggle ids     (g)", command=self.changeNodeLook)
        self.viewmenu.add_command(label="Clear canvas   (cg)", command=self.clearCanvas)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)

        self.root.config(menu=self.menubar)


    def clearCanvas(self, event="nothing"):
        # clear canvas
        self.canvas.delete("all")
        # clear nodes and edges
        self.graphNodes = []
        self.graphEdges = []
        # reset nodeCounter and also the ids
        self.nodeCounter = 0


    def changeNodeLook(self, event="nothing"):
        self.canvas.delete("all")


        if not self.drawNodeIds:
            self.drawNodeIds = True
        else:
            self.drawNodeIds = False;

        self.redrawNodes()
        self.redrawEdges()

    def redrawNodes(self):
        alternativNodeList = []
        for node in self.graphNodes:
            alternativNodeList.append(GraphNode(self.canvas, node.x,
                                                node.y, "", self.drawNodeIds, node.id))
        self.graphNodes = alternativNodeList

    def redrawEdges(self):
        alternativEdgeList = []
        for edge in self.graphEdges:
            alternativEdgeList.append(GraphEdge(self.canvas, edge.start.x,
                                                edge.start.y, edge.end.x, edge.end.y))
        self.graphEdges = alternativEdgeList

    def run(self):
        self.root.mainloop()

    def createNodeAtMousePos(self,event):
        isInCircle = False
        for node in self.graphNodes:
            if (abs((node.x - event.x)) <= GraphNode.graphNodeRadius
                and abs((node.y - event.y)) <= GraphNode.graphNodeRadius):
                isInCircle = True;

        isFarEnough = True
        for node in self.graphNodes:
            if(abs((node.x - event.x)) <= self.graphNodesMinDistance
               and abs((node.y - event.y)) <= self.graphNodesMinDistance):
                isFarEnough = False;

        if isFarEnough and not isInCircle:
            self.nodeCounter += 1
            self.graphNodes.append(GraphNode(self.canvas, event.x, event.y,
                                             "black", self.drawNodeIds, self.nodeCounter))

        if not isFarEnough and isInCircle:
            self.clickedNodes.append(event.x)
            self.clickedNodes.append(event.y)
            if (len(self.clickedNodes) == 4):
                self.graphEdges.append(GraphEdge(self.canvas, self.clickedNodes[0],
                                                 self.clickedNodes[1], self.clickedNodes[2],
                                                 self.clickedNodes[3]))
                self.clickedNodes = []



class GraphNode():
    graphNodeRadius = 12

    def __init__(self, canvas, x, y, text, drawIds, id):
        self.x = x
        self.y = y
        self.text = text
        self.canvas = canvas
        self.id = id
        if drawIds:
            canvas.create_oval(x - self.graphNodeRadius / 1.5, y - self.graphNodeRadius / 1.5,
                           x + self.graphNodeRadius,
                           y + self.graphNodeRadius,
                           fill="white")
        else:
            canvas.create_oval(x - self.graphNodeRadius / 1.5, y - self.graphNodeRadius / 1.5,
                           x + self.graphNodeRadius,
                           y + self.graphNodeRadius,
                           fill="black")



        canvas.create_text(self.x+2, self.y+2, text=self.id)

class GraphEdge():
    def __init__(self, canvas, x0, y0, xn, yn):
        # Start der Kante
        self.start = Vector(x0, y0)
        # Ender der Katen
        self.end = Vector(xn, yn)




        # Debugausgaben
        # print("x0", self.x0, "y0", self.y0)
        # print("endX", self.endX, "endY", self.endY)
        canvas.create_line(self.start.x, self.start.y, self.end.x, self.end.y, smooth=True)









window = Window(tk.Tk())
window.run()
