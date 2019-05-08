# pylint: disable=C0303, W0511
"""Module which handles most of the ui-stuff aka top level window stuff"""
import time
# -*- coding: latin-1 -*-
import tkinter as tk
from tkinter import ttk
from enum import Enum
from utils import timeit
import threading
import math

from graph import Graph, EmptyGraphError
from graphvisual import GraphVisual
from logger import logger
from observer import Observer, Subject

from widgets import OpenGraphDialog, NoteBookTab, InfoMenu

from graphs.ncircle import n_circle

# TODO RESIZABLE

class Window(tk.Tk, Subject, Observer):
    """Class which handles everything which das to do wit hthe window, user input, algorithm output, ui stuff"""
    # Dynamisch ans Canvas anpassen(Soll so gross wie das Fenster - InfoMenue groesse sein)

    class State(Enum):
        """
        Private class to capture the state of te program,
        can be used from an observer to implement actions
        when the state changes
        """
        LOAD_GRAPH = 0


    def __init__(self, model):
        tk.Tk.__init__(self)
        Subject.__init__(self)
        # VIEW OBSERVES THE MODEL FOR STATE CHANGES
        Observer.__init__(self)

        self.model = model
        self.model.attach(self)

        for x in self.model.layout_algos:
            print(x, self.model.layout_algos[x])

        self.info_menu = None
        self.geometry("1920x1080")
        # Init. canvas
        self.tabs = {}
        self.nb = ttk.Notebook(self, name="nb")
        self.index = 0

        self.nb.grid(column=0, row=0, sticky=tk.N)

        self.bind("<Control-t>", self.open_new_graph)
        self.bind("<Control-w>", self.delete_tab)
        self.bind("<Control-s>", self.do_algo)
        self.bind("<Control-r>", self.zoom_out)
        self.bind("<Control-f>", self.zoom_in)


    def zoom_out(self, event=None):
        self.get_current_tab().zoom_out()

    def zoom_in(self, event=None):
        self.get_current_tab().zoom_in()

    def attach(self, observer) -> None:
        Subject.attach(self, observer)

    def update(self, arg):
        # pylint: disable=R0201
        """
        Function which gets called from observed objects
        :param arg: Arguments which the observed class wants to be transmitted
        """
        state = arg[0]

        logger.info("mw: State: %s", str(state))

        if state == self.model.State.GRAPH_CHANGED:
            current_tab = self.tabs[arg[2]]
            graph = self.model.loaded_graphs[arg[1]]
            logger.info("setting the graph of %s to %s", arg[2], arg[1])
            current_tab.change_graph(graph)
            current_tab.graph_vis.redraw_graph()

        return filepath.split("/")[-1]

    def load_graph(self, filepath):
        """
        Loads a graph from the specified filepath, also initializes the tab and the graph visuals
        in which the graph will be displayed
        :param filepath: Filepath from which the graph should be loaded
        """
        logger.debug("Loading graph...")
        # Herausfinden in welchem Tab man sich befindet
        #logger.debug("TABS", self.nb.tabs())
        newest_tab = list(self.nb.tabs())[-1].split(".")[1]
        current_tab = self.tabs[newest_tab]

        self.subject_state = self.State.LOAD_GRAPH, filepath
        # Aktuellem Tab den Graphen zuweisen
        current_tab.set_graph(Graph.from_adjacency_list([], 0))
        # Aktuellem Tab die GraphVisuals zuweisen
        # TODO Das sollte nicht in der view passieren, generell sollte das load im controller sein
        current_tab.set_graph_vis(GraphVisual(
            window=self,
            canvas=current_tab.canvas,
            width=current_tab.CANVAS_WIDTH, height=current_tab.CANVAS_HEIGHT,
            graph=current_tab.graph,
            draw_node_ids = False,
            draw_values = True
        ))
        self.model.load_graph_from_file(self.get_graph_name(filepath), filepath, newest_tab)

    # TODO Sollte das auch ins model?
    def add_tab(self, event=None, graph_name: str = ""):
        # pylint: disable=W0613
        # Neuen Tab und zugehoeriges Canvas erstellen
        tab =  (NoteBookTab(self.nb,self, "tab"+str(self.index), self.model))
        tab.grid(column=0, row=1)
        # Erstellten Tab zum Canvas hizufuegen
        self.nb.add(tab, text=graph_name + " " + str(self.index))
        self.tabs["tab"+str(self.index)] = tab
        # Damit die Daten aktualisiert werden
        self.index += 1

    def delete_tab(self, event=None) -> None:
        # pylint: disable=W0613
        """
        Functons which closes the current ttk Notebook Tab
        :param event: ---
        :return:
        """
        # TODO self.tabs des zu loeschenden = None damit alle referenzen geloescht sind
        # TODO und garbage collected werden kann
        self.nb.forget(self.nb.select())

    def run(self):
        """Starts the application"""
        self.mainloop()

    def open_new_graph(self, event="nothing"):
        # pylint: disable=W0613
        """
        Funktion welche das Oeffnen eines neuen Graphen regelt, also das Auswehlen
        des json datei
        ueber den Graphen
        :param event:
        :return:
        """
        # self.add_tab(graph_name="Peter")
        current_instance = OpenGraphDialog(self)
        #a = "/home/td/dev/projects/graph.py/graphs/k20.json"
        #self.add_tab(a)
        #self.load_graph(a)
        # TODO Sollte das hier ein call an den Controller sein
        self.add_tab(current_instance.filename)
        self.load_graph(current_instance.filename)

        # TODO WENN ICH MIT NICH IRRE SCHUETZT NICHTS DIESES OBJECT DAS DUMM
        #threading.Thread(target=self.load_graph, args=(current_instance.filename,)).start()


    def get_current_tab(self):
        newest_tab = self.nb.select().split(".")[1]
        return self.tabs[newest_tab]


    # TODO Auch das sollte in controller
    def do_algo(self, event=None) -> None:
        # pylint: disable=W0613
        """Inititialisiert die FruchtermanReingold-Klasse um den Layouting-Algorithmus korrekt auszuf�hren"""
        # Herausfinden in welchem Tab man sich befindet
        current_tab = self.get_current_tab()
        # TODO Warum ist das hardgecoded
        klass = self.model.layout_algos[self.get_current_tab().combo.get()]
        algo = klass(graph_visuals=current_tab.graph_vis)

        algo.run()
        current_tab.redraw_graph()
        #threading.Thread(target=algo.run).start()

