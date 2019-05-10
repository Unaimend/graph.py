import os
from typing import Dict
from enum import Enum
from time import sleep

from logger import logger
from graph import Graph, LoadingError, DecodingError, EmptyGraphError
from algorithms.depth_first_search import DepthFirstSearch
from algorithms.layouting.layout_algorithm import LayoutAlgorithm
from observer import Subject


class MainModel(Subject):
    """
    Class which implements the model from MVC
    Loads all the algorithms:
    """

    class State(Enum):
        GRAPH_CHANGED = 0

    def __init__(self) -> None:
        """
        Checks if all needed paths exists and starts to load data which
        is needed by the application
        """
        Subject.__init__(self)
        if not os.path.exists("graphs"):
            logger.debug("Making graphs directory")
            os.makedirs("graphs")

        if not os.path.exists("algorithms"):
            logger.debug("Making algorithms directory")
            os.makedirs("algorithms")

        self.is_connected = False
        self.acyclic = False
        self.is_undirected_tree = False
        self.loaded_graphs: Dict[str, Graph] = dict()
        self.layout_algos: Dict[str, LayoutAlgorithm] = dict()

        self.load_layouting_algos()
        self.view = None


    def attach(self, observer):
        Subject.attach(self, observer)

    def load_layouting_algos(self):

        excluded_files = frozenset({"layout_algorithm.py", "__pycache__"})

        logger.info("CWD: %s" % os.getcwd())
        path = "algorithms/layouting/"

        if not os.path.exists(path):
            logger.debug("Making %s directory" % path)
            os.makedirs(path)

        # TODO GIBTS KEIN LIST MINUS/REMOVE
        entries = set(os.listdir(path)) - excluded_files


        # TODO Teil der For-Schleife eigene (pure?)Fkt. auslagern
        for file in entries:
            module = file[0:-3]
            logger.info("Loading %s" % module)
            name = "default"
            try:
                mod = __import__((path+file).replace("/", ".")[0:-3], fromlist=[name])
                name= getattr(mod, "class_name")
                logger.info("Trying to import %s from %s"% (name, file))
                try:
                    klass = getattr(mod, name)
                    self.layout_algos[name] = klass
                except AttributeError as error:
                    logger.error(error)
                    logger.error("The module %s does not have a class with the name %s", module, name)
            except AttributeError as e:
                logger.error(e)
                logger.error("Could not load %s" % module)
                logger.error("Each module must have the .class_name attribute")


    def load_graph_from_file(self, name: str, filepath: str, tab) -> None:
        """
        Load a graph from the specified file
        Mutates: self.loaded_graphs, self.is_undirected_tree
        :param name: The name under which the graph will ne accessible through the whole
        apllication
        :param filepath: The path from which the graph should be loaded
        """
        try:
            temp = Graph(filepath)
        except LoadingError:
            # Sth. is wrong with the file path
            raise LoadingError
        except DecodingError:
            # Sth. is wrong with the syntax of the file
            raise DecodingError
        # TODO Think about what should happen when name is alredy present in the dict
        self.loaded_graphs[name] = temp

        self.is_undirected_tree = self.check_undirected_tree(name)
        self.subject_state = self.State.GRAPH_CHANGED, name, tab

    def check_undirected_tree(self, name: str) -> bool:
        """
        Checks if a graph is a undirected tree(connceted, acyclic)
        Mutates: self.is_connected, self.acyclic
        """
        graph = self.loaded_graphs[name]
        try:
            dfs = DepthFirstSearch(graph, 0)
            # Check if all nodes have been visited
            if all(dfs.marked):
                self.is_connected = True
            if not dfs.contains_cycle:
                self.acyclic = True
            return self.is_connected and self.acyclic
        except EmptyGraphError:
            logger.error("Graph is empty")
            return False















