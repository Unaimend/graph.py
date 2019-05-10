import tkinter as tk
from abc import ABC, abstractmethod
from graphvisual import GraphVisual

class LayoutAlgorithm(ABC):
    def __init__(self, name: str, graph_visual: GraphVisual=None, algorithm_gui_area: tk.Frame = None):
        self.name = name
        self.aga = tk.Frame(None)

    @abstractmethod
    def init_widgets(self):
        pass

    @abstractmethod
    def run(self):
        pass
