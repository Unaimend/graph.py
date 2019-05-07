"""Module which contains all the ui widgets"""
from typing import List
import tkinter as tk
from tkinter import filedialog, Widget, ttk, StringVar
from graph import Graph
import graphvisual as gv

class OpenGraphDialog:
    """This is the window in which all setup options for algorithms and the algorithm you be chosen"""
    def __init__(self, root) -> None:
        """
        Ctor
        :param root: The root window in which this Dialog should be opened
        """
        self.filename: str = "test"
        self.root = root
        self.window = tk.Toplevel(self.root)
        self.window.wm_title("Open new graph")

        self.window.attributes("-topmost", True)


        self.open_graph()
        # TODO Seed auswahl fuer den RNG
        # TODO Show menue on if graph in none empty

    def open_graph(self):
        """The functions which opens the window and adds all the options"""
        self.filename = filedialog.askopenfilename(title="Select file",
                                                   filetypes=(("graph files", "*.json"), ("all files", "*.*")))
        self.window.destroy()



# TODO Eigenes Widget fuer das Editor Window, MVC mit EditorController, EditorView, EditorModel?
# TODO Graph in MCV auslagern? dann hat ein Tab ne GraphView und ne EditorView
class NoteBookTab(tk.Frame):
    """
    Verwaltungs-Class to handle the tab functionality like closing, opening, moving etc
    """
    def __init__(self, nb, root, index, model) -> None:
        self.root = root
        self.model = model
        tk.Frame.__init__(self, self.root, name=index)

        self.CANVAS_WIDTH = 1400
        self.CANVAS_HEIGHT = 700
        self.nb = nb
        self.widgetName = index
        self.graph_vis = None

        self.xscrollbar = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(column=0, row=2, sticky=tk.E + tk.W)

        self.yscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.yscrollbar.grid(column=3, row=1, sticky=tk.S + tk.N, rowspan=1)

        self.text = tk.Text(self, width=200, height=200)

        self.toggle = 0

        self.canvas: tk.Canvas = tk.Canvas(self, relief=tk.SUNKEN, bd=4,
                                           width=self.CANVAS_WIDTH,
                                           height=self.CANVAS_HEIGHT,
                                           background='white',
                                           scrollregion=(-2000, -2000, 2000, 2000),
                                           xscrollcommand=self.xscrollbar.set,
                                           yscrollcommand=self.yscrollbar.set,
                                           yscrollincrement=2,
                                           xscrollincrement=2
        )

        self.text.grid(column=0, row=1)
        self.canvas.grid(column=0, row=1)

        self.text.grid_forget()



        self.combo = ttk.Combobox(self, values = list(self.model.layout_algos.keys()), state='readonly' )
        self.combo.current(2)

        self.combo.grid(column=0, row=3, sticky=tk.N)

        # TODO Dynamisch statt hardcoded
        self.original_canvas_width = 1414

        self.xscrollbar.config(command=self.canvas.xview)
        self.yscrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Button-4>',lambda event:
                         self.canvas.yview_scroll(-1*event.num, "units"))
        self.canvas.bind('<Button-5>',lambda event:
                         self.canvas.yview_scroll(event.num, "units"))


        self.root.bind("<n>", self.toggle_text)
        self.canvas.bind("<Button>", self.touchpad_events)

         #Frame der die Label und TextInputs h�lt
        self.algorithm_options_frame = tk.Frame(self.root )
        self.algorithm_options_frame.grid(column=0, row=2)

        v = tk.Label(self.algorithm_options_frame, text="Hello Frame")
        v.pack()
        w = tk.Label(self.algorithm_options_frame, text="Hello Frame")
        w.pack()

        self.zoom = 1


    def toggle_text(self, event):
        if self.toggle == 0:
            self.toggle = 1
            self.text.grid(column=0, row=1)
        else:
            self.toggle = 0
            self.text.grid_forget()



    def touchpad_events(self, event):
        if event.num==6:
            self.canvas.xview_scroll(-1*event.num, "units")
            return "break"
        elif event.num==7:
            self.canvas.xview_scroll(event.num, "units")
            return "break"

    def change_graph(self, graph):
        ga = gv.GraphVisual(
            self.root,
            canvas=self.canvas,
            width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT,
            graph=graph)
        self.set_graph_vis(ga)


    def set_graph(self, graph):
        self.graph = graph

    def set_graph_vis(self, graph_vis):
        self.graph_vis = graph_vis


    def zoom_in(self, event=None):
        # pylint: disable=W0613
        amount = 1.1
        self.zoom *= amount
        self.canvas.scale(tk.ALL, self.graph_vis.width / 2, self.graph_vis.height / 2, amount, amount)

    def zoom_out(self, event=None):
        # pylint: disable=W0613
        amount = 0.9
        self.zoom *= amount
        self.canvas.scale(tk.ALL, self.graph_vis.width / 2, self.graph_vis.height / 2, amount, amount)

    def redraw_graph(self):
        self.graph_vis.translate_to_mid()
        self.canvas.scale(tk.ALL, self.graph_vis.width / 2, self.graph_vis.height / 2, self.zoom, self.zoom)



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
    def __init__(self, root, node, adjacent_nodes) -> None:
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
