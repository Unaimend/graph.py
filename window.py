import graph as Graph
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

import graphvisual as gv
import Eades
import time

class OpenGraphDialog:
    def __init__(self, root):
        self.filename = "test"
        self.eades = tk.BooleanVar()

        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.wm_title("Open new graph")

        # self.open_new_graph_but = tk.Button(self.window, text="Open...", command=self.open_graph)
        # self.open_new_graph_but.pack()

        self.open_graph()
        # TODO Auswahl der graph.json
        # TODO Auswahl des Layout Algorithmuses
        # TODO Seed auswahl fuer den RNG

    def open_graph(self):
        nb = ttk.Notebook(self.window)


        var = tk.IntVar()
        self.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("graph files", "*.json"), ("all files", "*.*")))
        button = tk.Button(self.window, text="Ok", command=lambda: var.set(1))
        button.pack()
        label = tk.Label(self.window, text="Which layouting algorithm do you want to use")
        label.pack()
        c = tk.Checkbutton(self.window, text="eades", variable=self.eades, onvalue=True, offvalue=False)
        c.pack()
        button.wait_variable(var)
        self.window.destroy()


class NoteBookTab:
    def __init__(self,canvas,graph,graph_vis):
        self.canvas = canvas
        self.graph = graph
        self.graph_vis = graph_vis

    def set_graph(self, graph):
        self.graph = graph

    def set_graph_vis(self, graph_vis):
        self.graph_vis = graph_vis


class Window:
    CANVAS_WIDTH = 1200
    CANVAS_HEIGHT = 800
    EADES = False
    # TODO In graph_visuals auslagern da dies jetzt pro tab also pro graph_visuals gespeichert werden muss
    def __init__(self, root):
        self.root = root
        self.graph = None
        self.graph_visuals = None
        # Four textboxes and labels for the eades constants
        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.l4 = None
        # self.root.geometry("1400x800")
        # Init. canvas
        self.tabs = {}
        self.canvases = []
        self.graph_vis = []
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(expand=1, fill="both")
        self.root.bind("<n>", self.open_new_graph)
        self.root.bind("<t>", self.add_canvas)

    def get_current_notebook_tab(self, event=None):
        return self.nb.index("current")

    def add_canvas(self, event):
        index = len(self.nb.tabs())
        self.tabs[index] = (NoteBookTab(tk.Canvas(self.nb, relief=tk.SUNKEN, bd=4,
                                                  width=Window.CANVAS_WIDTH, height=Window.CANVAS_HEIGHT,
                                                  background='white'), None, None))
        self.nb.add(self.tabs[index].canvas,  text="Canvas " + str(index))

    def run(self):
        self.root.mainloop()

    def open_new_graph(self, event="nothing"):
        current_instance = OpenGraphDialog(self.root)

        Window.EADES = current_instance.eades.get()
        self.load_graph(current_instance.filename)

    def load_graph(self, filepath):
        print("Loading graph...")
        current_tab = self.tabs[self.get_current_notebook_tab()]
        current_tab.set_graph((Graph.Graph.from_file(width=Window.CANVAS_WIDTH,
                                                     height=Window.CANVAS_HEIGHT,
                                                     filepath=filepath)))

        current_tab.set_graph_vis(gv.GraphVisual.from_graph(
                                                     canvas=self.tabs[self.get_current_notebook_tab()].canvas,
                                                     width=Window.CANVAS_WIDTH, height=Window.CANVAS_HEIGHT,
                                                     graph=self.tabs[self.get_current_notebook_tab()].graph))

        # Bind actions to the last added graph_vis
        current_tab.canvas.bind("<g>", current_tab.graph_vis.change_node_look)
        current_tab.canvas.bind("<c>", current_tab.graph_vis.redraw_graph)
        current_tab.canvas.bind("<Button-1>", current_tab.graph_vis.set_focus)


        self.del_eades_constant_widgets()
        # Show eades constant choices only if user selected eades as algorithm
        if Window.EADES:
            # Dem Algorithmus eine Zeichenflaeche zuweisen mit der er arbeiten soll
            current_tab.canvas.bind("<s>", self.do_eades_new)
            current_tab.canvas.bind("<f>", self.do_eades_old)
            self.init_eades_constant_widgets()
        # Next algorithm gui stuff

        current_tab.graph_vis.redraw_graph()


    def do_eades_old(self, event="nothing"):
        # TODO Kosntanten fuer Eades auf der Werte aus den Textboxen setzen
        start = time.time()
        for x in range(0, 100):
            Eades.Eades.calculate_attractive_force_for_all_nodes_and_move_accordingly_old()
            Eades.Eades.calculate_repelling_force_for_all_nodes_and_move_accordingly_old()
        end = time.time()
        print("Old elapsed Time", end - start)
        self.graph_visuals.generate_edges()

    def do_eades_new(self, event="nothing"):
        # TODO https://github.com/Unaimend/graph.py/issues/2
        current_tab = self.tabs[self.get_current_notebook_tab()]
        Eades.Eades.graph_visuals = current_tab.graph_vis

        text = str()

        text = self.t1.get("1.0", 'end-1c')
        Eades.Eades.c1 = float(text)

        text = self.t2.get("1.0", 'end-1c')
        Eades.Eades.c2 = float(text)

        text = self.t3.get("1.0", 'end-1c')
        Eades.Eades.c3 = float(text)

        text = self.t4.get("1.0", 'end-1c')
        Eades.Eades.c4 = float(text)

        start = time.time()
        for x in range(0, 100):
            Eades.Eades.calculate_attractive_force_for_all_nodes_and_move_accordingly_new()
            Eades.Eades.calculate_repelling_force_for_all_nodes_and_move_accordingly_new()
        end = time.time()

        # Update positions
        current_tab.graph_vis.redraw_nodes()
        print("Elapsed Time", end - start)
        # Update adjacency list
        current_tab.graph_vis.generate_adj_list()
        # Update edges between nodes
        current_tab.graph_vis.generate_edges()

    def del_eades_constant_widgets(self):
        if self.l1 != None:
            self.l1.destroy()
            self.l2.destroy()
            self.l3.destroy()
            self.l4.destroy()
            self.t1.destroy()
            self.t2.destroy()
            self.t3.destroy()
            self.t4.destroy()

    def init_eades_constant_widgets(self):

        self.l1 = tk.Label(self.root, text="c1")
        self.l1.pack(side=tk.LEFT)
        # Textfield for ... Eades constant
        self.t1 = tk.Text(self.root, height=1, width=5, relief="sunken", borderwidth=2)
        self.t1.pack(side=tk.LEFT)
        self.t1.insert(tk.END, Eades.Eades.c1)

        self.l2 = tk.Label(self.root, text="c2")
        self.l2.pack(side=tk.LEFT)
        # Textfield for ... Eades constant
        self.t2 = tk.Text(self.root, height=1, width=5, relief="sunken", borderwidth=2)
        self.t2.pack(side=tk.LEFT)
        self.t2.insert(tk.END, Eades.Eades.c2)

        self.l3 = tk.Label(self.root, text="c3")
        self.l3.pack(side=tk.LEFT)
        # Textfield for ... Eades constant
        self.t3 = tk.Text(self.root, height=1, width=5, relief="sunken", borderwidth=2)
        self.t3.pack(side=tk.LEFT)
        self.t3.insert(tk.END, Eades.Eades.c3)

        self.l4 = tk.Label(self.root, text="c4")
        self. l4.pack(side=tk.LEFT)
        # Textfield for ... Eades constant
        self.t4 = tk.Text(self.root, height=1, width=5, relief="sunken", borderwidth=2, takefocus = 0)
        self.t4.pack(side=tk.LEFT)
        self.t4.insert(tk.END, Eades.Eades.c4)
