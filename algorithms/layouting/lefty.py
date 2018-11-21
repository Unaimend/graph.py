"""Module which implements an algorithm similiar to the first Algorithm from Iidy drawing of Trees[WH79["""
from graphvisual import  GraphVisual
from graph import Graph


class Lefty:
    """Class which implements an algorithm similiar to the first Algorithm from Iidy drawing of Trees[WH79["""
    def __init__(self, graph_visuals, graph, canvas_width, canvas_height):
        """
        Ctor. 
        :param graph_visuals: Handles all the stuff that has to do with drawing
        :param canvas_width: Width of the canvas
        :param canvas_height: Height of the canvas 
        """
        self.graph_visuals = graph_visuals
        self.canvas_width = canvas_width
        self.canvas_length = canvas_height
        self.graph = graph
        self.max_height = -1

        for x in range(0, len(self.graph.adjacency_list)):
            height = self.graph.dist_from_root(x)
            if height > self.max_height:
                self.max_height = height

        print("max height", self.max_height)

    def do_lefty(self) -> None:
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


