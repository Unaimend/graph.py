"""Module which contains all the ui widgets"""
from typing import List
import tkinter as tk
from tkinter import filedialog, Widget, ttk
from graph import Graph, GraphNode
from algorithms.layouting.layout_algorithm import LayoutAlgorithm


class OpenGraphDialog:
    """This is the window in which all setup options for algorithms and the algorithm you be chosen"""
    def __init__(self, root) -> None:
        """
        Ctor
        :param root: The root window in which this Dialog should be opened
        """
        self.filename: str = "test"
        self.eades = tk.BooleanVar()
        self.fruchterman_reingold = tk.BooleanVar()
        self.lefty = tk.BooleanVar()

        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.wm_title("Open new graph")

        # self.open_new_graph_but = tk.Button(self.window, text="Open...", command=self.open_graph)
        # self.open_new_graph_but.pack()

        self.window.attributes("-topmost", True)


        self.open_graph()
        # TODO Seed auswahl fuer den RNG
        # TODO Show menue on if graph in none empty

    def open_graph(self):
        """The functions which opens the window and adds all the options"""
        var = tk.IntVar()
        self.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("graph files", "*.json"), ("all files", "*.*")))
        button = tk.Button(self.window, text="Ok", command=lambda: var.set(1))
        button.pack()
        label = tk.Label(self.window, text="Which layouting algorithm do you want to use")
        label.pack()
        # TODO Combobox statt Checkbutton oder Radiobuttons
        c = tk.Checkbutton(self.window, text="Eades", variable=self.eades,
                           onvalue=True, offvalue=False)
        c.pack()
        c1 = tk.Checkbutton(self.window, text="Fruchterman-Reingold",
                            variable=self.fruchterman_reingold, onvalue=True,
                            offvalue=False)
        c1.pack()
        c2 = tk.Checkbutton(self.window, text="Lefty", variable=self.lefty,
                            onvalue=True,
                            offvalue=False)
        c2.pack()
        button.wait_variable(var)
        self.window.destroy()


class NoteBookTab(tk.Frame):
    """
    Verwaltungs-Class to handle the tab functionality like closing, opening, moving etc
    """
    def __init__(self, nb, graph_vis, algo: LayoutAlgorithm, root, index) -> None:
        tk.Frame.__init__(self, root)
        self.index = index
        self.CANVAS_WIDTH = 1400
        self.CANVAS_HEIGHT = 700
        self.nb = nb
        self.widgetName = index

        self.root = root
        self.xscrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(column=0, row=2, sticky=tk.E + tk.W)

        self.yscrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.yscrollbar.grid(column=2, row=0, sticky=tk.S + tk.N, rowspan=1)

        self.canvas: tk.Canvas = tk.Canvas(self.root, relief=tk.SUNKEN, bd=4,
                                           width=self.CANVAS_WIDTH,
                                           height=self.CANVAS_HEIGHT,
                                           background='white',
                                           scrollregion=(-2000, -2000, 2000, 2000),
                                           xscrollcommand=self.xscrollbar.set,
                                           yscrollcommand=self.yscrollbar.set)
        self.canvas.grid(column=0, row=1)

        self.graph_vis = graph_vis
        # TODO Dynamisch statt hardcoded
        self.original_canvas_width = 1414
        self.algorithm = algo

        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)


        # Frame der die Label und TextInputs h�lt
        self.algorithm_options_frame = tk.Frame(root)


    def set_graph(self, graph):
        self.graph = graph

    def set_graph_vis(self, graph_vis):
        self.graph_vis = graph_vis

    def zoom_in(self, event=None):
        # pylint: disable=W0613
        # 0.9 if event.delta < 0 else 1.1
        amount = 1.1
        # DIe Null sollte width/2, height/2 sein aber das fuckt die berechnugn ab,
        # self.canvas.scale(tk.ALL, 0, 0, amount, amount)
        self.canvas.scale(tk.ALL, self.graph_vis.width / 2, self.graph_vis.height / 2, amount, amount)

    def zoom_out(self, event=None):
        # pylint: disable=W0613
        print("WOOT")
        # 0.9 if event.delta < 0 else 1.1
        amount = 0.9
        self.canvas.scale(tk.ALL, self.graph_vis.width / 2, self.graph_vis.height / 2, amount, amount)




class InfoMenu(tk.Frame):
    # pylint: disable=R0901
    def __init__(self, parent) -> None:
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.label: List[str] = []
        self.label_val: List[str] = []
        self.buttons = []
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

    def add_button(self, text="", fnc=lambda: print("hello"), row=-1, column=0):
        if row == -1:
            row = self.row_ctr
        button = tk.Button(self, text=text, anchor=tk.W, command=fnc)
        button.grid(row=row, column=column)
        self.buttons.append(button)



    def toggle(self):
        if self.visible:
            self.visible = False
            self.grid_remove()
        else:
            self.visible = True
            self.grid()

    def print(self, event=None):
        # pylint: disable=W0613
        print("TEST")


class NodeInfo:
    def __init__(self, root, node: GraphNode, adjacent_nodes: List[GraphNode]) -> None:
        self.root = root
        self.window = tk.Toplevel(self.root)
        # Sorgt dafuer das die Info Fenster nicht durch das "Main"-Fenster verdeckt
        self.window.attributes("-topmost", True)

        self.window.bind("<Escape>", self.close )
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

    def close(self, event=None):
        self.window.destroy()
