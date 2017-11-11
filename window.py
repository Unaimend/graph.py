from graph import Graph
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

from graphvisual import GraphVisual
from eades import Eades
import time

# TODO Enter druecken in den Eades Kosntantenboxen geht gar nicht gut
# TODO Bind mac touchbad to scrollbars
# TODO Siehe Shift-MouseWheel MouseWheel
# TODO Wenn graph gezeichnet wird sollten scrollsbars auf anfang gesetzt werden damit man den graphen sieht

# TODO Pypy3 is kranker shit mal auseinandersettzen KRANK
# TODO RESIZABLE
# TODO Slices um das \n oder so loszuwerden beim den textfeldern(anber erst string.rstrip anschauen
# TODO Ueberlegen ob ich die Alg. async mache
# TODO Duck  Typing vs type hinting in python (Does type hinting eng(verhindern) duck typing)
# TODO GUI option to start the algorithms and at leas tfor the eades a text entry(pop up) how opfen they want to start
# TODO the algo
# MUltishredding fuer die Algorithmen

# Frozen binarie am Besten mit pypy3
# Control statt Cmd verwenden


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
        button.wait_variable(var)
        self.window.destroy()


class NoteBookTab:
    def __init__(self, canvas, graph, graph_vis):
        self.canvas = canvas
        self.graph = graph
        self.graph_vis = graph_vis
        # TODO Dynamisch statt hardcoded
        self.original_canvas_width = 1414

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


class Window:
    # Dynamisch ans Canvas anpassen(Soll so gross wie das Fenster - InfoMenue groesse sein)
    CANVAS_WIDTH = 1400
    CANVAS_HEIGHT = 700
    # TODO In graph_visuals auslagern da dies jetzt pro tab also pro graph_visuals gespeichert werden muss
    # TODO Jeder Tab hat ja die moeglichkeit einen anderen Algorithmus zu verwenden
    EADES = False
    def __init__(self, root):
        self.root = root
        # Four textboxes and labels for the eades constants
        self.eades_options_frame = None
        self.t1 = None
        self.t2 = None
        self.t3 = None
        self.t4 = None
        self.l1 = None
        self.l2 = None
        self.l3 = None
        self.l4 = None
        self.info_menu = None
        self.root.geometry("1920x1080")
        # Init. canvas
        self.tabs = {}



        self.nb = ttk.Notebook(self.root)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.xscrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(column=1, row=2, sticky=tk.E + tk.W)

        self.yscrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.yscrollbar.grid(column=2, row=0, sticky=tk.S + tk.N, rowspan=1)

        self.add_info_menu()
        self.add_canvas()

        self.xscrollbar.config(command=self.tabs[0].canvas.xview)
        self.yscrollbar.config(command=self.tabs[0].canvas.yview)
        # File menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        # self.viewmenu.add_separator()
        self.filemenu.add_command(label="Open...    (CMD+N)", command=self.open_new_graph )
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Edit menu
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # View menu
        self.viewmenu = tk.Menu(self.menubar, tearoff=0)
        self.viewmenu.add_command(label="Toggle ids         (g)")
        self.viewmenu.add_command(label="Clear canvas       (c)")
        self.viewmenu.add_command(label="Toggle Info Menue  (CMD+B)", command=self.toggle_info_menu)
        self.menubar.add_cascade(label="View", menu=self.viewmenu)

        self.nb.grid(column=1, row=0, sticky=tk.E)
        # Add shortcuts
        self.root.bind("<Command-n>", self.open_new_graph)
        self.root.bind("<Command-t>", self.add_canvas)
        self.root.bind("<Command-b>", self.toggle_info_menu)

        # self.root.bind_all('<MouseWheel>', lambda x: print("oben") )
        # self.root.bind_all('<Shift-MouseWheel>', lambda x: print("links"))

    def get_current_notebook_tab(self, event=None):
        return self.nb.index("current")

    def add_canvas(self, event=None):
        # Anzahl der Tabs herausfinden
        index = len(self.nb.tabs())
        # Neuen Tab und zugehoeriges Canvas erstellen
        self.tabs[index] = (NoteBookTab(tk.Canvas(self.nb, relief=tk.SUNKEN, bd=4,
                                                  width=Window.CANVAS_WIDTH, height=Window.CANVAS_HEIGHT,
                                                  background='white', scrollregion=(-2000, -2000, 2000, 2000),
                                                  xscrollcommand=self.xscrollbar.set,
                                                  yscrollcommand=self.yscrollbar.set), None, None))
        # Erstellten Tab zum Canvas hizufuegen
        self.nb.add(self.tabs[index].canvas,  text="Canvas " + str(index))

    def run(self):
        self.root.mainloop()

    def open_new_graph(self, event="nothing"):
        current_instance = OpenGraphDialog(self.root)
        Window.EADES = current_instance.eades.get()
        self.load_graph(current_instance.filename)

    def add_info_menu(self):
        """In dieser Methoden koennen dem Info Menu widgets hinzugefuegt werden"""
        self.info_menu = InfoMenu(self.root)
        self.info_menu.grid(column=0, row=0, sticky=tk.N)

        self.info_menu.add_label("Zusammenhängend")
        self.info_menu.label_val[0]["text"] = "----"
        self.info_menu.add_label("Länge")
        self.info_menu.label_val[1]["text"] = "0"

    def toggle_info_menu(self, event=None):
        new_width = 0
        self.info_menu.toggle()
        # Neue Breite berechnen(abhaengig davon ob das info_menu zu sehen ist oder nicht)
        if self.info_menu.visible:
            new_width = self.tabs[self.get_current_notebook_tab()].original_canvas_width
        else:
            # Magic 28 sorgt dafuer das canvas nicht an Breite waechst
            new_width = self.info_menu.winfo_width() + self.tabs[self.get_current_notebook_tab()].canvas.winfo_width() - 28

        self.tabs[self.get_current_notebook_tab()].canvas.configure(width=new_width)

    def load_graph(self, filepath):
        print("Loading graph...")
        # Herausfinden in welchem Tab man sich befindet
        current_tab = self.tabs[self.get_current_notebook_tab()]
        # Aktuellem Tab den Graphen zuweisen
        current_tab.set_graph((Graph.from_file(filepath=filepath)))
        # Aktuellem Tab die GraphVisuals zuweisen
        current_tab.set_graph_vis(GraphVisual.from_graph(
                                                     canvas=self.tabs[self.get_current_notebook_tab()].canvas,
                                                     width=Window.CANVAS_WIDTH, height=Window.CANVAS_HEIGHT,
                                                     graph=self.tabs[self.get_current_notebook_tab()].graph))

        # Bind actions to the last added graph_vis
        # TODO Control-w to close tab
        current_tab.canvas.bind("<Command-g>", current_tab.graph_vis.change_node_look)
        current_tab.canvas.bind("<Command-c>", current_tab.graph_vis.redraw_graph)
        current_tab.canvas.bind("<Button-1>", current_tab.graph_vis.set_focus)

        self.del_eades_constant_widgets()
        # Show eades constant choices only if user selected eades as algorithm
        if Window.EADES:
            # Dem Algorithmus eine Zeichenflaeche zuweisen mit der er arbeiten soll
            current_tab.canvas.bind("<Control-s>", self.do_eades_new)
            self.init_eades_constant_widgets()
        # Next algorithm gui stuff
        current_tab.graph_vis.redraw_graph()

    def do_eades_new(self, event="nothing"):
        # Herausfinden in welchem Tab man sich befindet
        current_tab = self.tabs[self.get_current_notebook_tab()]
        # Graphen auf dem gearbeitet wird zuweisen
        Eades.graph_visuals = current_tab.graph_vis

        text = str()

        # Aktuelle Werte der Konstante laden
        text = self.t1.get("1.0", 'end-1c')
        Eades.c1 = float(text)

        text = self.t2.get("1.0", 'end-1c')
        Eades.c2 = float(text)

        text = self.t3.get("1.0", 'end-1c')
        Eades.c3 = float(text)

        text = self.t4.get("1.0", 'end-1c')
        Eades.c4 = float(text)

        start = time.time()
        # 100x den Algorithmus ausführen(siehe [EAD84] Paper)
        for x in range(0, 100):
            Eades.calculate_attractive_force_for_all_nodes_and_move_accordingly_new()
            Eades.calculate_repelling_force_for_all_nodes_and_move_accordingly_new()
        end = time.time()

        # Update positions
        current_tab.graph_vis.redraw_nodes()
        print("Elapsed Time", end - start)
        # Update adjacency list
        current_tab.graph_vis.generate_adj_list()
        # Update edges between nodes
        current_tab.graph_vis.generate_edges()

    def del_eades_constant_widgets(self):
        # Wenn self.eades_options_frame exisitiert, exisitieren die anderen Variablen auch
        # und es is sicher .destroy zu callen
        if self.eades_options_frame is not None:
            self.eades_options_frame.destroy()
            self.t1.destroy()
            self.t2.destroy()
            self.t3.destroy()
            self.t4.destroy()
            self.l1.destroy()
            self.l2.destroy()
            self.l3.destroy()
            self.l4.destroy()

    def init_eades_constant_widgets(self):
        # Frame der die Label und TextInputs hält
        self.eades_options_frame = tk.Frame(self.root)
        # Position des Frames in der GUI setzen
        self.eades_options_frame.grid(column=1, row=3)

        self.l1 = tk.Label(self.eades_options_frame, text="c1")
        self.l1.pack(side=tk.LEFT)
        # Textfield for c1 Eades constant
        self.t1 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
        self.t1.pack(side=tk.LEFT)
        self.t1.insert(tk.END, Eades.c1)
        self.l2 = tk.Label(self.eades_options_frame, text="c2")
        self.l2.pack(side=tk.LEFT)
        # Textfield for c2 Eades constant
        self.t2 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
        self.t2.pack(side=tk.LEFT)
        self.t2.insert(tk.END, Eades.c2)
        self.l3 = tk.Label(self.eades_options_frame, text="c3")
        self.l3.pack(side=tk.LEFT)
        # Textfield for c3 Eades constant
        self.t3 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
        self.t3.pack(side=tk.LEFT)
        self.t3.insert(tk.END, Eades.c3)
        self.l4 = tk.Label(self.eades_options_frame, text="c4")
        self.l4.pack(side=tk.LEFT)
        # Textfield for c4 Eades constant
        self.t4 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2, takefocus = 0)
        self.t4.pack(side=tk.LEFT)
        self.t4.insert(tk.END, Eades.c4)




  # style = ttk.Style()
        # style.theme_create("MyStyle", parent="alt", settings={
        #     "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        #     "TNotebook.Tab": {"configure": {"padding": [0, 0]}, }})
        #
        # style.theme_use("MyStyle")
