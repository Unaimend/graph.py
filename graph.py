import tkinter as tk

import math


class Window:
    def __init__(self, root):
        self.root = root;
        self.canvas = tk.Canvas(self.root, relief=tk.SUNKEN, bd=4,
                                width=1200, height=800,  background='white')
        self.canvas.pack()

        self.root.bind("<Button 1>", self.createNodeAtMousePos)

        self.root.bind("<g>", self.changeNodeLook)

        self.root.bind("<c>", self.clearCanvas)


        self.graphNodesMinDistance = 2*GraphNode.graphNodeRadius;

        self.graphNodes = []
        self.graphEdges = []

        self.clickedNodes = []

        self.drawNodeIds = False;

        self.nodeCounter = 0;

    def clearCanvas(self, event):
        self.canvas.delete("all")
        self.graphNodes = []
        self.graphEdges = []
        self.nodeCounter = 0


    def changeNodeLook(self, event):
        self.canvas.delete("all")

        alternativNodeList = []
        alternativEdgeList = []
        if not self.drawNodeIds:
            self.drawNodeIds = True
        else:
            self.drawNodeIds = False;
        for node in self.graphNodes:
            alternativNodeList.append(GraphNode(self.canvas, node.x,
                                            node.y, "", self.drawNodeIds, node.id))

        for edge in self.graphEdges:
            alternativEdgeList.append(GraphEdge(self.canvas, edge.x0,
                                                edge.y0, edge.endX, edge.endY))


        self.graphNodes = alternativNodeList
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
        self.x0 = x0
        self.y0 = y0

        self.endX = xn;
        self.endY = yn;

        self.middleX = 0
        self.middleY = 0

        print("x0", self.x0, "y0", self.y0)

        print("endX", self.endX, "endY", self.endY)
        # # startpunkt links endpunkt
        # if x0 <=xn:
        #     # startpunkt unter von endpunkt
        #     if y0 >= yn:
        #         self.middleX = self.x0 + (self.endX - self.x0)/2
        #         self.middleY = self.y0 + (self.endY - self.y0)/2
        #
        #         canvas.create_line(x0, y0, self.middleX, self.middleY, smooth=True)
        #
        #
        #         print("MiddleX", self.middleX, "MiddleY", self.middleY)
        #     # startpunkt ueber von endpunkt
        #     else:
        #         print("mimimimimi")
        # # startpunkt rechts vom entpunkt
        # else:
        #     print("mimimimimi")
        #     # startpunkt unter von endpunkt
        #     # startpunkt ueber von endpunkt
        canvas.create_line(x0, y0, xn, yn, smooth=True)









window = Window(tk.Tk())
window.run()
