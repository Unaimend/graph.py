import tkinter as tk
from abc import ABC, abstractmethod


class LayoutAlgorithm(ABC):
    def __init__(self, name, graph_visuals, algorithm_gui_area: tk.Frame):
        self.name = name
        self.graph_visuals = graph_visuals
        self.algorithm_gui_area = algorithm_gui_area
    
    @abstractmethod
    def init_widgets(self):
        pass
