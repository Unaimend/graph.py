from graphvisual import  GraphVisual
from graph import Graph

from algorithms.layouting.layout_algorithm import LayoutAlgorithm

class_name = "Bt"

class Bt(LayoutAlgorithm):
    """Class which implements an algorithm similiar to the first Algorithm from Iidy drawing of Trees[WH79["""
    def __init__(self, graph_visuals):
        """
        Ctor. 
        :param graph_visuals: Handles all the stuff that has to do with drawing
        :param canvas_width: Width of the canvas
        :param canvas_height: Height of the canvas 
        """
        LayoutAlgorithm.__init__(self, class_name)
        self.graph_visuals = graph_visuals
        self.canvas_width = self.graph_visuals.width
        self.canvas_length = self.graph_visuals.height
        self.graph = self.graph_visuals.graph

    def init_widgets(self):
        pass

    def run(self) -> None:
        return
