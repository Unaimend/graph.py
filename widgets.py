from graph import Graph, GraphNode
from typing import List
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk


class OpenGraphDialog:
    def __init__(self, root):
        self.filename = "test"
        self.eades = tk.BooleanVar()
        self.fruchterman_reingold = tk.BooleanVar()

        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.wm_title("Open new graph")

        # self.open_new_graph_but = tk.Button(self.window, text="Open...", command=self.open_graph)
        # self.open_new_graph_but.pack()

        self.open_graph()
        # TODO Seed auswahl fuer den RNG
        # TODO Show menue on if graph in none empty

    def open_graph(self):
        var = tk.IntVar()
        self.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("graph files", "*.json"), ("all files", "*.*")))
        button = tk.Button(self.window, text="Ok", command=lambda: var.set(1))
        button.pack()
        label = tk.Label(self.window, text="Which layouting algorithm do you want to use")
        label.pack()
        # TODO Combobox statt Checkbutton oder Radiobuttons
        c = tk.Checkbutton(self.window, text="eades", variable=self.eades, onvalue=True, offvalue=False)
        c.pack()
        c1 = tk.Checkbutton(self.window, text="Fruchterman-Reingold", variable=self.fruchterman_reingold, onvalue=True, offvalue=False)
        c1.pack()
        button.wait_variable(var)
        self.window.destroy()


class NoteBookTab:
    def __init__(self, canvas, graph, graph_vis, algo=""):
        self.canvas = canvas
        self.graph = graph
        self.graph_vis = graph_vis
        # TODO Dynamisch statt hardcoded
        self.original_canvas_width = 1414
        self.algorithm = algo

    def set_graph(self, graph):
        self.graph = graph

    def set_graph_vis(self, graph_vis):
        self.graph_vis = graph_vis


class InfoMenu(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.label = []
        self.label_val = []
        self.row_ctr = 0
        self.parent.bind("<Command-l>", self.print)
        self.visible = True

    def add_label(self, text=""):
        label = tk.Label(self, text=text, anchor=tk.W)
        label.grid(row=self.row_ctr, column=0)
        self.label.append(label)
        label_val = tk.Label(self, text=str(self.row_ctr * 100), anchor=tk.E)
        label_val.grid(row=self.row_ctr, column=1)
        self.label_val.append(label_val)

        self.row_ctr += 1

    def toggle(self):
        if self.visible:
            self.visible = False
            self.grid_remove()
        else:
            self.visible = True
            self.grid()

    def print(self, event=None):
        print("TEST")


class NodeInfo:
    def __init__(self,root,node: GraphNode, adjacent_nodes: List[GraphNode]):
        self.root = root
        self.window = tk.Toplevel(self.root)
        # Sorgt dafuer das die Info Fenster nicht durch das "Main"-Fenster verdeckt
        self.window.attributes("-topmost", True)
        self.info_menu = InfoMenu(self.window)
        self.info_menu.pack()
        self.info_menu.add_label("Id")
        self.info_menu.label_val[0]["text"] = str(node.id)
        self.info_menu.add_label("Position")
        self.info_menu.label_val[1]["text"] = "x: %d y: %d " % (int(node.position.x), int(node.position.y))

        adjacent_nodes_text = ""
        for x in adjacent_nodes: adjacent_nodes_text += (" " + str(x.id))

        self.info_menu.add_label("Adj. Nodes")
        self.info_menu.label_val[2]["text"] = adjacent_nodes_text

        self.info_menu.toggle()
        button = tk.Button(self.window, text="Close", command=self.window.destroy)
        button.pack()
