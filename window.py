# pylint: disable=C0303, W0511
"""Module which handles most of the ui-stuff aka top level window stuff"""
import time
# -*- coding: latin-1 -*-
import tkinter as tk
from tkinter import ttk

from algorithms.layouting.fr import FruchtermanReingold
from algorithms.layouting.lefty import Lefty
from algorithms.layouting.eades import Eades
from algorithms.depth_first_search import DepthFirstSearch, DfsVisual
from graph import Graph
from graphvisual import GraphVisual
from utils import timeit
from widgets import OpenGraphDialog, NoteBookTab, InfoMenu


# TODO Enter druecken in den Eades Kosntantenboxen geht gar nicht gut
# TODO Siehe Shift-MouseWheel MouseWheel
# TODO Wenn graph gezeichnet wird sollten scrollsbars auf anfang gesetzt werden damit man den graphen sieht

# TODO RESIZABLE
# TODO Slices um das \n oder so loszuwerden beim den textfeldern(anber erst string.rstrip anschauen
# Passiert falls man mit Enter versucht die Textfield eingabe zu bestaetigen,
# Das Emter drucken in einem Label sollte dafuer sorgen dass das Canvas ausgewaehlt wird
# TODO Eigentlich war es vollieg retarded die Layoutingklassen static zu machen denn
# TODo jetzt kann man  nichtmal in zwei Tabs den gleichen Algorithmus mit versch. Parametern starten


class Window:
    """ClLass which handles everything which das to do wit hthe window, user input, algorithm output, ui stuff"""
    # Dynamisch ans Canvas anpassen(Soll so gross wie das Fenster - InfoMenue groesse sein)
    CANVAS_WIDTH = 1400
    CANVAS_HEIGHT = 700
    # TODO In graph_visuals auslagern da dies jetzt pro tab also pro graph_visuals gespeichert werden muss
    # TODO Jeder Tab hat ja die moeglichkeit einen anderen Algorithmus zu verwenden
    EADES = False
    FRUCHTERMAN_REINGOLD = False
    LEFTY = False

    def __init__(self, root):
        self.root = root
        # Four textboxes and labels for the eades constants
        self.eades_options_frame = None
        self.tb_1 = None
        self.tb_2 = None
        self.tb_3 = None
        self.tb_4 = None
        self.label_1 = None
        self.label_2 = None
        self.label_3 = None
        self.label_4 = None
        self.info_menu = None
        self.root.geometry("1920x1080")
        # Init. canvas
        self.tabs = {}

        # TODO Current_algo solt eine
        self.current_algo = None

        self.nb = ttk.Notebook(self.root)

        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        self.xscrollbar = tk.Scrollbar(self.root, orient=tk.HORIZONTAL)
        self.xscrollbar.grid(column=1, row=2, sticky=tk.E + tk.W)

        self.yscrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.yscrollbar.grid(column=2, row=0, sticky=tk.S + tk.N, rowspan=1)

        self.add_canvas()
        self.add_info_menu()
        self.xscrollbar.config(command=self.tabs[0].canvas.xview)
        self.yscrollbar.config(command=self.tabs[0].canvas.yview)
        # File menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        # self.viewmenu.add_separator()
        self.filemenu.add_command(label="Open...    (CMD+N)", command=self.open_new_graph)
        self.filemenu.add_command(label="Exit", command=root.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Edit menu
        self.editmenu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Edit", menu=self.editmenu)

        # View menu
        self.viewmenu = tk.Menu(self.menubar, tearoff=0)
        self.viewmenu.add_command(label="Toggle ids")
        self.viewmenu.add_command(label="Clear canvas       (Strg+c)")
        self.viewmenu.add_command(label="Toggle Info Menue  (Strg+b)", command=self.toggle_info_menu)
        # self.menubar.add_cascade(label="View", menu=self.viewmenu, command=self.run_dfs)

        # View menu
        self.algorithms_menu = tk.Menu(self.menubar, tearoff=0)
        self.algorithms_menu.add_command(label="Run dfs", command=self.run_dfs)
        self.menubar.add_cascade(label="Algos", menu=self.algorithms_menu)

        self.nb.grid(column=1, row=0, sticky=tk.E)
        # Add shortcuts
        self.root.bind("<Control-n>", self.open_new_graph)
        self.root.bind("<Control-t>", self.add_canvas)
        self.root.bind("<Control-b>", self.toggle_info_menu)
        self.root.bind("<Control-w>", self.delete_tab)

        self.nb.bind("<<NotebookTabChanged>>", self.renew_info_menu_data)

        # self.root.bind_all('<MouseWheel>', lambda x: print("oben") )
        # self.root.bind_all('<Shift-MouseWheel>', lambda x: print("links"))

    def get_current_notebook_tab_index(self, event=None):
        # pylint: disable=W0613
        """Method get the index of the current notebook tabbb"""
        """
        :param event: 
        :return: Return the index of the current Notebook Tab
        """
        return self.nb.index("current")

    def add_canvas(self, event=None):
        # pylint: disable=W0613
        # Anzahl der Tabs herausfinden
        index = len(self.nb.tabs())
        # Neuen Tab und zugehoeriges Canvas erstellen
        self.tabs[index] = (NoteBookTab(tk.Canvas(self.nb, relief=tk.SUNKEN, bd=4,
                                                  width=Window.CANVAS_WIDTH, height=Window.CANVAS_HEIGHT,
                                                  background='white', scrollregion=(-2000, -2000, 2000, 2000),
                                                  xscrollcommand=self.xscrollbar.set,
                                                  yscrollcommand=self.yscrollbar.set), None, None))
        # Erstellten Tab zum Canvas hizufuegen
        self.nb.add(self.tabs[index].canvas, text="Canvas " + str(index))
        # Damit die Daten aktualisiert werden

    def delete_tab(self, event=None) -> None:
        # pylint: disable=W0613
        """
        Functons which closes the current ttk Notebook Tab
        :param event: --- 
        :return: 
        """
        self.nb.forget("current")

    def run(self):
        """Starts the application"""
        self.root.mainloop()

    def open_new_graph(self, event="nothing"):
        # pylint: disable=W0613
        """
        Funktion welche das Oeffnen eines neuen Graphen regelt, also das Auswehlen
        des json datei, das Auswaehlen des Algos und das setzen der Konstanten und Informationen 
        ueber den Graphen
        :param event: 
        :return: 
        """
        current_instance = OpenGraphDialog(self.root)
        Window.EADES = current_instance.eades.get()
        Window.FRUCHTERMAN_REINGOLD = current_instance.fruchterman_reingold.get()
        Window.LEFTY = current_instance.lefty.get()
        self.load_graph(current_instance.filename)
        self.toggle_info_menu()
        self.toggle_info_menu()

    def add_info_menu(self) -> None:
        """Creates the Info Sidebar and also adds the different menue entries"""
        self.info_menu = InfoMenu(self.root)
        self.info_menu.grid(column=0, row=0, sticky=tk.N)

        self.info_menu.add_label("Anzahl der Knoten")
        self.info_menu.label_val[0]["text"] = ""

        self.info_menu.add_label("Anzahl der Kanten")
        self.info_menu.label_val[1]["text"] = ""

        self.info_menu.add_label("Azyklisch")
        self.info_menu.label_val[2]["text"] = ""

        self.info_menu.add_label("Zusammenhaengend")
        self.info_menu.label_val[3]["text"] = ""

        self.info_menu.add_label("Algorithmus")
        self.info_menu.label_val[4]["text"] = self.tabs[self.get_current_notebook_tab_index()].algorithm

    def toggle_info_menu(self, event=None) -> None:
        # pylint: disable=W0613
        """
        Toggles the Info Menue
        :param event: 
        """
        new_width = 0
        self.info_menu.toggle()

        # Neue Breite berechnen(abhaengig davon ob das info_menu zu sehen ist oder nicht)
        if self.info_menu.visible:
            new_width = self.tabs[self.get_current_notebook_tab_index()].original_canvas_width
            try:
                # HIER KOMMEN DIE ZUWEISUNGEN FUER DATEN DES INFO MENUES HIN
                self.info_menu.label_val[0]["text"] = str(self.tabs[self.get_current_notebook_tab_index()].graph.vertice_count)

            except AttributeError:
                self.info_menu.label_val[0]["text"] = ""
            try:
                pass
            except AttributeError:
                pass
        else:
            # Magic 28 sorgt dafuer das canvas nicht an Breite waechst
            # TODO: Gehts locker kaputt wenn ich die Aufloesung aendere
            new_width = self.info_menu.winfo_width() + self.tabs[self.get_current_notebook_tab_index()].canvas.winfo_width() - 28

        self.tabs[self.get_current_notebook_tab_index()].canvas.configure(width=new_width)

    def renew_info_menu_data(self, event=None) -> None:
        # pylint: disable=W0613
        """
        Reloads the Info-Menue-Data when the Info Menue got toggled
        :param event: 
        """
        # Beim toggeln werden die Daten aktualisiert deswegen toggeln wir hier 2x mal
        # um den Anzeigestatus beizubehalten aber die Daten zu aktualiseren
        self.toggle_info_menu()
        self.toggle_info_menu()
        # Check ob der in diesem Tab verwendete Algorithmus des von Eades ist oder nicht
        if self.tabs[self.get_current_notebook_tab_index()].algorithm == "eades":
            # Falls der Algorithmus von Eades verwenet wird muessen die Gui Widgets neu initialisert werden
            self.init_eades_constant_widgets()
        else:
            # Falls nicht, sollen die Widgets geloescht werden damit sie nicht angezeigt werden
            self.del_eades_constant_widgets()

    def load_graph(self, filepath) -> None:
        """
        Loads a graph from the specified filepath, also initializes the tab and the graph visuals
        in which the graph will be displayed
        :param filepath: Filepath from which the graph should be loaded    
        """
        print("Loading graph...")
        # Herausfinden in welchem Tab man sich befindet
        current_tab = self.tabs[self.get_current_notebook_tab_index()]
        # Aktuellem Tab den Graphen zuweisen
        current_tab.set_graph((Graph.from_file(filepath=filepath)))
        # Aktuellem Tab die GraphVisuals zuweisen
        current_tab.set_graph_vis(GraphVisual.from_graph(
            window=self.root,
            canvas=self.tabs[self.get_current_notebook_tab_index()].canvas,
            width=Window.CANVAS_WIDTH, height=Window.CANVAS_HEIGHT,
            graph=self.tabs[self.get_current_notebook_tab_index()].graph))
        # Zueweisen welcher Algo. verwendet wird um mit Hilfe dieser Information
        # zu bestimmen welche Gui Widgets gezeichnet werden sollen.
        if Window.EADES:
            current_tab.algorithm = "eades"
        elif Window.FRUCHTERMAN_REINGOLD:
            current_tab.algorithm = "fr"
        elif Window.LEFTY:
            current_tab.algorithm = "lefty"
        else:
            current_tab.algorithm = "None"

        self.info_menu.label_val[4]["text"] = current_tab.algorithm


        #     ALGORITHM TEST AREA
        test = DepthFirstSearch(current_tab.graph, 0)

        for x in range(current_tab.graph.vertice_count):
            print("IS connected to", test.has_path_to(x))

        # ALL ACTIONS WHICH ARE ON TAB LEVEL SHOULD BE ADDED HERE
        # Bind actions to the last added graph_vis
        # TODO Control-w to close tab
        current_tab.canvas.bind("<Control-g>", current_tab.graph_vis.change_node_look)
        current_tab.canvas.bind("<Control-c>", current_tab.graph_vis.redraw_graph)
        current_tab.canvas.bind("<Button-1>", current_tab.graph_vis.set_focus)
        # add="+" sorgt dafuer das die vorherige Funktion die auf der Tasten liegt nicht ueberschrieben wird
        current_tab.canvas.bind("<Control-p>", current_tab.zoom_in)
        current_tab.canvas.bind("<Control-p>", current_tab.graph_vis.inc_zoomlevel, add="+")

        current_tab.canvas.bind("<Control-o>", current_tab.zoom_out)
        current_tab.canvas.bind("<Control-o>", current_tab.graph_vis.dec_zoomlevel, add="+")
        current_tab.canvas.bind("<Button-1>", current_tab.graph_vis.select_node, add="+")


        self.del_eades_constant_widgets()

        # ----------------------------------This is the the only part that should change when usign another algorithm--
        if Window.EADES:
            # Graphen auf dem gearbeitet wird zuweisenr
            self.current_algo = Eades(current_tab.graph_vis)
            # Show eades constant choices only if user selected eades as algorithm
            # Dem Algorithmus eine Zeichenflaeche zuweisen mit der er arbeiten soll
            current_tab.canvas.bind("<Control-s>", self.do_eades_new)
            self.init_eades_constant_widgets()
        elif Window.FRUCHTERMAN_REINGOLD:
            current_tab.canvas.bind("<Control-s>", self.do_fruchterman_reingold)
        elif Window.LEFTY:
            current_tab.canvas.bind("<Control-s>", self.do_sexy)


        # Next algorithm gui stuff
        current_tab.graph_vis.redraw_graph()
        # ---------------------------------------------------------------------------------------------

    def do_sexy(self, event=None)->None:
        # pylint: disable=W0613
        current_tab = self.tabs[self.get_current_notebook_tab_index()]

        sexy = Lefty(graph_visuals=current_tab.graph_vis, graph=current_tab.graph, canvas_width=Window.CANVAS_WIDTH,
                     canvas_height=Window.CANVAS_HEIGHT)

        timeit(sexy.do_lefty)
        current_tab.graph_vis.redraw_nodes()
        # Update adjacency list
        current_tab.graph_vis.generate_adj_list()
        # Update edges between nodes
        current_tab.graph_vis.generate_edges()

    def do_fruchterman_reingold(self, event=None) -> None:
        # pylint: disable=W0613
        """Inititialisiert die FruchtermanReingold-Klasse um den Layouting-Algorithmus korrekt auszuf�hren"""
        # Herausfinden in welchem Tab man sich befindet
        current_tab = self.tabs[self.get_current_notebook_tab_index()]
        # Graphen auf dem gearbeitet wird zuweisen
        # FruchtermanReingold.k =  math.sqrt(FruchtermanReingold.area / FruchtermanReingold.graph_visuals.nodeCounter)
        # TODO Warum ist das hardgecoded
        fr = FruchtermanReingold(graph_visuals=current_tab.graph_vis, canvas_width=Window.CANVAS_WIDTH,
                                 canvas_height=Window.CANVAS_HEIGHT, k=50, t=100)

        timeit(fr.do_fr, 100)

        current_tab.graph_vis.redraw_nodes()

        # Update adjacency list
        current_tab.graph_vis.generate_adj_list()
        # Update edges between nodes
        current_tab.graph_vis.generate_edges()

    # -----------------------------EADES SPECIFIC STUFF------------------------------------------------------------
    def do_eades_new(self, event=None):
        # pylint: disable=W0613
        """Inititialisiert die Eades-Klasse um den Layouting-Algorithmus korrekt auszuf�hren"""
        # Herausfinden in welchem Tab man sich befindet
        current_tab = self.tabs[self.get_current_notebook_tab_index()]

        text = str()

        # Aktuelle Werte der Konstante laden
        text = self.tb_1.get("1.0", 'end-1c')
        self.current_algo.c1 = float(text)

        text = self.tb_2.get("1.0", 'end-1c')
        self.current_algo.c2 = float(text)

        text = self.tb_3.get("1.0", 'end-1c')
        self.current_algo.c3 = float(text)

        text = self.tb_4.get("1.0", 'end-1c')
        self.current_algo.c4 = float(text)

        start = time.time()
        # 100x den Algorithmus ausf�hren(siehe [EAD84] Paper)
        for _ in range(0, 100):
            self.current_algo.calculate_attractive_force_for_all_nodes_and_move_accordingly_new()
            self.current_algo.calculate_repelling_force_for_all_nodes_and_move_accordingly_new()
        end = time.time()
        print("Elapsed Time", end - start)
        # Update positions
        current_tab.graph_vis.redraw_nodes()

        # Update adjacency list
        current_tab.graph_vis.generate_adj_list()
        # Update edges between nodes
        current_tab.graph_vis.generate_edges()

    def del_eades_constant_widgets(self):
        """
        FUNctions which handles the deletetion of the eades labels and text boxes
        :return: 
        """
        # Wenn self.eades_options_frame exisitiert, exisitieren die anderen Variablen auch
        # und es is sicher .destroy zu callen
        if self.eades_options_frame is not None:
            self.eades_options_frame.destroy()
            self.tb_1.destroy()
            self.tb_2.destroy()
            self.tb_3.destroy()
            self.tb_4.destroy()
            self.label_1.destroy()
            self.label_2.destroy()
            self.label_3.destroy()
            self.label_4.destroy()

    def init_eades_constant_widgets(self):
        """Initializes all the eades constant"""
        # Frame der die Label und TextInputs h�lt
        self.eades_options_frame = tk.Frame(self.root)
        # Position des Frames in der GUI setzen
        self.eades_options_frame.grid(column=1, row=3)

        self.label_1 = tk.Label(self.eades_options_frame, text="c1")
        self.label_1.pack(side=tk.LEFT)
        # Textfield for c1 Eades constant
        self.tb_1 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
        self.tb_1.pack(side=tk.LEFT)
        self.tb_1.insert(tk.END, self.current_algo.constant_1)
        self.label_2 = tk.Label(self.eades_options_frame, text="c2")
        self.label_2.pack(side=tk.LEFT)
        # Textfield for c2 Eades constant
        self.tb_2 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
        self.tb_2.pack(side=tk.LEFT)
        self.tb_2.insert(tk.END, self.current_algo.constant_2)
        self.label_3 = tk.Label(self.eades_options_frame, text="c3")
        self.label_3.pack(side=tk.LEFT)
        # Textfield for c3 Eades constant
        self.tb_3 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
        self.tb_3.pack(side=tk.LEFT)
        self.tb_3.insert(tk.END, self.current_algo.constant_3)
        self.label_4 = tk.Label(self.eades_options_frame, text="c4")
        self.label_4.pack(side=tk.LEFT)
        # Textfield for c4 Eades constant
        self.tb_4 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2, takefocus=0)
        self.tb_4.pack(side=tk.LEFT)
        self.tb_4.insert(tk.END, self.current_algo.constant_4)
# ----------------------------EADES SPECIFIC STUFF END------------------------------------------------------------------

    def run_dfs(self, event=None):
        # pylint: disable=W0613
        a = DfsVisual(self.tabs[self.get_current_notebook_tab_index()].graph_vis, colour="black")
        a.run()
        print("IHI")


