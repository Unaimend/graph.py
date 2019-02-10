# pylint: disable=C0303, W0511
"""Module which handles most of the ui-stuff aka top level window stuff"""
import time
# -*- coding: latin-1 -*-
import tkinter as tk
from tkinter import ttk

from algorithms.depth_first_search import DepthFirstSearch, DfsVisual
from algorithms.layouting.eades import Eades
from algorithms.layouting.fr import FruchtermanReingold
from algorithms.layouting.lefty import Lefty
from graph import Graph, EmptyGraphError
from graphvisual import GraphVisual
from logger import logger
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
    """Class which handles everything which das to do wit hthe window, user input, algorithm output, ui stuff"""
    # Dynamisch ans Canvas anpassen(Soll so gross wie das Fenster - InfoMenue groesse sein)

    # TODO In graph_visuals auslagern da dies jetzt pro tab also pro graph_visuals gespeichert werden muss
    # TODO Jeder Tab hat ja die moeglichkeit einen anderen Algorithmus zu verwenden
    EADES = False
    FRUCHTERMAN_REINGOLD = False
    LEFTY = False

    def __init__(self, root):
        self.root = root
        # Four textboxes and labels for the eades constants
        self.info_menu = None
        self.alg = None
        self.root.geometry("1920x1080")
        # Init. canvas
        self.tabs = {}

        # TODO Current_algo solt eine
        self.current_algo = None

        self.nb = ttk.Notebook(self.root)
        self.index = 0


        # self.menubar = tk.Menu(self.root)
        # self.root.config(menu=self.menubar)
        #
        # # File menu
        # self.filemenu = tk.Menu(self.menubar, tearoff=0)
        # # self.viewmenu.add_separator()
        # # self.filemenu.add_command(label="Open...    (CMD+N)", command=self.open_new_graph)
        # self.filemenu.add_command(label="Exit", command=root.quit)
        # self.menubar.add_cascade(label="File", menu=self.filemenu)
        # #
        # # Edit menu
        # self.editmenu = tk.Menu(self.menubar, tearoff=0)
        # self.menubar.add_cascade(label="Edit", menu=self.editmenu)
        #
        # # View menu
        # self.viewmenu = tk.Menu(self.menubar, tearoff=0)
        # self.viewmenu.add_command(label="Toggle ids")
        # self.viewmenu.add_command(label="Clear canvas       (Strg+c)")
        # self.viewmenu.add_command(label="Toggle Info Menue  (Strg+b)", command=self.toggle_info_menu)
        # self.menubar.add_cascade(label="View", menu=self.viewmenu, command=self.run_dfs)

        self.nb.grid(column=0, row=0, sticky=tk.N)
        # self.nb.pack()
        # Add shortcuts
        # self.root.bind("<Control-n>", self.open_new_graph)
        self.root.bind("<Control-t>", self.open_new_graph)
        # self.root.bind("<Control-b>", self.toggle_info_menu)
        self.root.bind("<Control-w>", self.delete_tab)

        # self.nb.bind("<<NotebookTabChanged>>", self.get_current_notebook_tab)

        # self.root.bind_all('<MouseWheel>', lambda x: print("oben") )
        # self.root.bind_all('<Shift-MouseWheel>', lambda x: print("links"))

    def get_current_notebook_tab(self, event=None):
        # pylint: disable=W0613
        """Method get the index of the current notebook tabbb"""
        logger.debug(self.nb.tab(self.nb.select(), "text"))
        index = self.nb.tab(self.nb.select(), "text")[-1]
        return {"id": self.nb.index("current"), "index": int(index)}

    def load_graph(self, filepath):
        """
        Loads a graph from the specified filepath, also initializes the tab and the graph visuals
        in which the graph will be displayed
        :param filepath: Filepath from which the graph should be loaded
        """
        print("Loading graph...")
        # Herausfinden in welchem Tab man sich befindet
        print(self.tabs)
        current_index = self.get_current_notebook_tab()["index"]
        current_tab = self.tabs[current_index]
        # Aktuellem Tab den Graphen zuweisen
        current_tab.set_graph((Graph.from_file(filepath=filepath)))
        # Aktuellem Tab die GraphVisuals zuweisen
        current_tab.set_graph_vis(GraphVisual(
            window=self.root,
            canvas=current_tab.canvas,
            width=current_tab.CANVAS_WIDTH, height=current_tab.CANVAS_HEIGHT,
            graph=current_tab.graph))
        # Zueweisen welcher Algo. verwendet wird um mit Hilfe dieser Information
        # zu bestimmen welche Gui Widgets gezeichnet werden sollen.


    # def load_graph(self, filepath) -> None:
    #     """
    #     Loads a graph from the specified filepath, also initializes the tab and the graph visuals
    #     in which the graph will be displayed
    #     :param filepath: Filepath from which the graph should be loaded
    #     """
    #     print("Loading graph...")
    #     # Herausfinden in welchem Tab man sich befindet
    #     current_tab = self.tabs[self.get_current_notebook_tab_index()]
    #     # Aktuellem Tab den Graphen zuweisen
    #     current_tab.set_graph((Graph.from_file(filepath=filepath)))
    #     # Aktuellem Tab die GraphVisuals zuweisen
    #     current_tab.set_graph_vis(GraphVisual(
    #         window=self.root,
    #         canvas=self.tabs[self.get_current_notebook_tab_index()].canvas,
    #         width=Window.CANVAS_WIDTH, height=Window.CANVAS_HEIGHT,
    #         graph=self.tabs[self.get_current_notebook_tab_index()].graph))
    #     # Zueweisen welcher Algo. verwendet wird um mit Hilfe dieser Information
    #     # zu bestimmen welche Gui Widgets gezeichnet werden sollen.
    #     if Window.EADES:
    #         current_tab.algorithm = "eades"
    #         self.alg = Eades()
    #     elif Window.FRUCHTERMAN_REINGOLD:
    #         current_tab.algorithm = "fr"
    #     elif Window.LEFTY:
    #         current_tab.algorithm = "lefty"
    #     else:
    #         current_tab.algorithm = "None"
    #
    #     self.info_menu.label_val[4]["text"] = current_tab.algorithm
    #
    #
    #     # ALGORITHM TEST AREA
    #     try:
    #         test = DepthFirstSearch(current_tab.graph, 0)
    #         for x in range(current_tab.graph.vertice_count):
    #             print("IS connected to", test.has_path_to(x))
    #     except EmptyGraphError:
    #         logger.info("Did not ran dfs because the graph was empty " + str(__file__))
    # #
    # #     # ALL ACTIONS WHICH ARE ON TAB LEVEL SHOULD BE ADDED HERE
    # #     # Bind actions to the last added graph_vis
    # #     # TODO Control-w to close tab
    #     current_tab.canvas.bind("<Control-g>", current_tab.graph_vis.change_node_look)
    #     current_tab.canvas.bind("<Control-c>", current_tab.graph_vis.redraw_graph)
    #     current_tab.canvas.bind("<Button-1>", current_tab.graph_vis.set_focus)
    #     # add="+" sorgt dafuer das die vorherige Funktion die auf der Tasten liegt nicht ueberschrieben wird
    #     current_tab.canvas.bind("<Control-p>", current_tab.zoom_in)
    #     current_tab.canvas.bind("<Control-p>", current_tab.graph_vis.inc_zoomlevel, add="+")
    #
    #     current_tab.canvas.bind("<Control-o>", current_tab.zoom_out)
    #     current_tab.canvas.bind("<Control-o>", current_tab.graph_vis.dec_zoomlevel, add="+")
    #     current_tab.canvas.bind("<Button-1>", current_tab.graph_vis.select_node, add="+")
    #
    #i
    #
    #     # ----------------------------------This is the the only part that should change when usign another algorithm--
    #     if Window.EADES:
    #         # Graphen auf dem gearbeitet wird zuweisenr
    #         self.current_algo = Eades(current_tab.graph_vis)
    #         # Show eades constant choices only if user selected eades as algorithm
    #         # Dem Algorithmus eine Zeichenflaeche zuweisen mit der er arbeiten soll
    #         current_tab.canvas.bind("<Control-s>", self.do_eades_new)
    #         self.init_eades_constant_widgets()
    #     elif Window.FRUCHTERMAN_REINGOLD:
    #         current_tab.canvas.bind("<Control-s>", self.do_fruchterman_reingold)
    #     elif Window.LEFTY:
    #         current_tab.canvas.bind("<Control-s>", self.do_sexy)
    #
    #
    #     # Next algorithm gui stuff
    #     current_tab.graph_vis.redraw_graph()
    #

    def add_tab(self, event=None, graph_name: str = ""):
        # pylint: disable=W0613
        # Anzahl der Tabs herausfinden

        # Neuen Tab und zugehoeriges Canvas erstellen
        tab =  (NoteBookTab(self.nb, None, None, self.root, self.index))
        # Erstellten Tab zum Canvas hizufuegen
        self.nb.add(tab, text=graph_name + " " + str(self.index))
        self.tabs[self.index] = tab
        # Damit die Daten aktualisiert werden
        self.index += 1


    def delete_tab(self, event=None) -> None:
        # pylint: disable=W0613
        """
        Functons which closes the current ttk Notebook Tab
        :param event: ---
        :return:
        """
        self.nb.forget(self.get_current_notebook_tab()["id"])

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
        # self.add_tab(graph_name="Peter")
        current_instance = OpenGraphDialog(self.root)
        Window.EADES = current_instance.eades.get()
        Window.FRUCHTERMAN_REINGOLD = current_instance.fruchterman_reingold.get()
        Window.LEFTY = current_instance.lefty.get()
        self.add_tab(graph_name=current_instance.filename)
        self.load_graph(current_instance.filename)
        # self.toggle_info_menu()
        # self.toggle_info_menu()
    #
    # def add_info_menu(self) -> None:
    #     """Creates the Info Sidebar and also adds the different menue entries"""
    #     self.info_menu = InfoMenu(self.root)
    #     self.info_menu.grid(column=0, row=0, sticky=tk.N)
    #
    #     self.info_menu.add_label("Anzahl der Knoten")
    #     self.info_menu.label_val[0]["text"] = ""
    #
    #     self.info_menu.add_label("Anzahl der Kanten")
    #     self.info_menu.label_val[1]["text"] = ""
    #
    #     self.info_menu.add_label("Azyklisch")
    #     self.info_menu.label_val[2]["text"] = ""
    #
    #     self.info_menu.add_label("Zusammenhaengend")
    #     self.info_menu.label_val[3]["text"] = ""
    #
    #     self.info_menu.add_label("Algorithmus")
    #     self.info_menu.label_val[4]["text"] = self.tabs[self.get_current_notebook_tab_index()].algorithm

    # def toggle_info_menu(self, event=None) -> None:
    #     # pylint: disable=W0613
    #     """
    #     Toggles the Info Menue
    #     :param event:
    #     """
    #     new_width = 0
    #     self.info_menu.toggle()
    #
    #     # Neue Breite berechnen(abhaengig davon ob das info_menu zu sehen ist oder nicht)
    #     if self.info_menu.visible:
    #         new_width = self.tabs[self.get_current_notebook_tab_index()].original_canvas_width
    #         try:
    #             # HIER KOMMEN DIE ZUWEISUNGEN FUER DATEN DES INFO MENUES HIN
    #             self.info_menu.label_val[0]["text"] = str(self.tabs[self.get_current_notebook_tab_index()].graph.vertice_count)
    #
    #         except AttributeError:
    #             self.info_menu.label_val[0]["text"] = ""
    #         try:
    #             pass
    #         except AttributeError:
    #             pass
    #     else:
    #         # Magic 28 sorgt dafuer das canvas nicht an Breite waechst
    #         # TODO: Gehts locker kaputt wenn ich die Aufloesung aendere
    #         new_width = self.info_menu.winfo_width() + self.tabs[self.get_current_notebook_tab_index()].canvas.winfo_width() - 28
    #
    #     self.tabs[self.get_current_notebook_tab_index()].canvas.configure(width=new_width)
    #
    # def renew_info_menu_data(self, event=None) -> None:
    #     # pylint: disable=W0613
    #     """
    #     Reloads the Info-Menue-Data when the Info Menue got toggled
    #     :param event:
    #     """
    #     # Beim toggeln werden die Daten aktualisiert deswegen toggeln wir hier 2x mal
    #     # um den Anzeigestatus beizubehalten aber die Daten zu aktualiseren
    #     self.toggle_info_menu()
    #     self.toggle_info_menu()
    #     # Check ob der in diesem Tab verwendete Algorithmus des von Eades ist oder nicht
    #     if self.tabs[self.get_current_notebook_tab_index()].algorithm == "eades":
    #         # Falls der Algorithmus von Eades verwenet wird muessen die Gui Widgets neu initialisert werden
    #         # self.init_eades_constant_widgets()
    #     else:
    #         # Falls nicht, sollen die Widgets geloescht werden damit sie nicht angezeigt werden
    #         # self.del_eades_constant_widgets()
    #

        # ---------------------------------------------------------------------------------------------
    #
    # def do_sexy(self, event=None)->None:
    #     # pylint: disable=W0613
    #     current_tab = self.tabs[self.get_current_notebook_tab_index()]
    #
    #     sexy = Lefty(graph_visuals=current_tab.graph_vis, graph=current_tab.graph, canvas_width=Window.CANVAS_WIDTH,
    #                  canvas_height=Window.CANVAS_HEIGHT)
    #
    #     timeit(sexy.do_lefty)
    #     current_tab.graph_vis.redraw_nodes()
    #     # Update adjacency list
    #     current_tab.graph_vis.generate_adj_list()
    #     # Update edges between nodes
    #     current_tab.graph_vis.generate_edges()

    # def do_fruchterman_reingold(self, event=None) -> None:
        # # pylint: disable=W0613
        # """Inititialisiert die FruchtermanReingold-Klasse um den Layouting-Algorithmus korrekt auszuf�hren"""
        # # Herausfinden in welchem Tab man sich befindet
        # current_tab = self.tabs[self.get_current_notebook_tab_index()]
        # # Graphen auf dem gearbeitet wird zuweisen
        # # FruchtermanReingold.k =  math.sqrt(FruchtermanReingold.area / FruchtermanReingold.graph_visuals.nodeCounter)
        # # TODO Warum ist das hardgecoded
        # fr = FruchtermanReingold(graph_visuals=current_tab.graph_vis, canvas_width=Window.CANVAS_WIDTH,
        #                          canvas_height=Window.CANVAS_HEIGHT, k=50, t=100)
        #
        # timeit(fr.do_fr, 100)
        #
        # current_tab.graph_vis.redraw_nodes()
        #
        # # Update adjacency list
        # current_tab.graph_vis.generate_adj_list()
        # # Update edges between nodes
        # current_tab.graph_vis.generate_edges()

    # # -----------------------------EADES SPECIFIC STUFF------------------------------------------------------------
    # def do_eades_new(self, event=None):
    #     # pylint: disable=W0613
    #     """Inititialisiert die Eades-Klasse um den Layouting-Algorithmus korrekt auszuf�hren"""
    #     # Herausfinden in welchem Tab man sich befindet
    #     current_tab = self.tabs[self.get_current_notebook_tab_index()]
    #
    #     text = str()
    #
    #     # Aktuelle Werte der Konstante laden
    #     text = self.tb_1.get("1.0", 'end-1c')
    #     self.current_algo.c1 = float(text)
    #
    #     text = self.tb_2.get("1.0", 'end-1c')
    #     self.current_algo.c2 = float(text)
    #
    #     text = self.tb_3.get("1.0", 'end-1c')
    #     self.current_algo.c3 = float(text)
    #
    #     text = self.tb_4.get("1.0", 'end-1c')
    #     self.current_algo.c4 = float(text)
    #
    #     start = time.time()
    #     # 100x den Algorithmus ausf�hren(siehe [EAD84] Paper)
    #     for _ in range(0, 100):
    #         self.current_algo.calculate_attractive_force_for_all_nodes_and_move_accordingly_new()
    #         self.current_algo.calculate_repelling_force_for_all_nodes_and_move_accordingly_new()
    #     end = time.time()
    #     print("Elapsed Time", end - start)
    #     # Update positions
    #     current_tab.graph_vis.redraw_nodes()
    #
    #     # Update adjacency list
    #     current_tab.graph_vis.generate_adj_list()
    #     # Update edges between nodes
    #     current_tab.graph_vis.generate_edges()


# ----------------------------EADES SPECIFIC STUFF END------------------------------------------------------------------

    def run_dfs(self, event=None):
        # pylint: disable=W0613
        a = DfsVisual(self.tabs[self.get_current_notebook_tab_index()].graph_vis, colour="black")
        a.run()
        print("IHI")
