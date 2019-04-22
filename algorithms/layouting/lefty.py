"""Module which implements an algorithm similiar to the first Algorithm from Iidy drawing of Trees[WH79["""
from graphvisual import  GraphVisual
from graph import Graph

from algorithms.layouting.layout_algorithm import LayoutAlgorithm

class_name = "Lefty"

class Lefty(LayoutAlgorithm):
    """Class which implements an algorithm similiar to the first Algorithm from Iidy drawing of Trees[WH79["""
    def __init__(self, graph_visuals):
        """
        Ctor. 
        :param graph_visuals: Handles all the stuff that has to do with drawing
        :param canvas_width: Width of the canvas
        :param canvas_height: Height of the canvas 
        """
        LayoutAlgorithm.__init__(self, "Lefty")
        self.graph_visuals = graph_visuals
        self.canvas_width = self.graph_visuals.width
        self.canvas_length = self.graph_visuals.height
        self.graph = self.graph_visuals.graph
        self.max_height = -1

        for x in range(0, len(self.graph.adjacency_list)):
            height = self.graph.dist_from_root(x)
            if height > self.max_height:
                self.max_height = height

        print("max height", self.max_height)

    def init_widgets(self):
        pass

    def run(self) -> None:
        """
        Executes the whole algorithm 
        """
        nexts = [100] * (self.max_height+2)
        depths = [0] * len(self.graph.adjacency_list)
        print("LEN", len(nexts))

        def pos(index, depth):
            curr_node = self.graph_visuals.graph_nodes[index]
            posit = nexts[depth]
            # Wenn diese if zutrifft kann direkt links von mir kein Knoten sein
            # also koennen wir eine positon nach links gehen ohne wen zu treffen
            if nexts[depth] < depths[self.graph.parent(index)]:
                posit = depths[self.graph.parent(index)]-100
                nexts[depth] = posit
            curr_node.set_pos(posit, (depth*100)+50)
            depths[index] = nexts[depth]
            nexts[depth] = nexts[depth] + 100

            if index == 0:
                pos(self.graph_visuals.node_adjacency_list[curr_node.id][0].id, depth + 1)
            for x in range(1, len(self.graph_visuals.node_adjacency_list[curr_node.id])):
                pos(self.graph_visuals.node_adjacency_list[curr_node.id][x].id, depth + 1)

        pos(0, 0)

        def pos2(index, depth):
            curr_node = self.graph_visuals.graph_nodes[index]
            curr_node.move(-50*depth, 0)
            if index == 0:
                pos2(self.graph_visuals.node_adjacency_list[curr_node.id][0].id, depth + 1)
            for x in range(1, len(self.graph_visuals.node_adjacency_list[curr_node.id])):
                pos2(self.graph_visuals.node_adjacency_list[curr_node.id][x].id, depth + 1)

        # pos2(0,0)


