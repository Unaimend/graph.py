"""
.. module:: graph
   :platform: Unix, Windows, Mac
   :synopsis: This module includes classes necessary for working with graphs
.. moduleauthor:: Thomas Dost(Unaimend@gmail.com)
"""
import json
from typing import List
from logger import logger
from vector import Vector

# typedefs
AdjacencyList = List[List[int]]
AdjacencyListEntry = List[int]
AdjacencyMatrix = List[List[int]]

# TODO representation of graphs
# TODO Siehe https://stackoverflow.com/questions/13212300/how-to-reconfigure-tkinter-canvas-items
# TODO Graphen als n-gon aufstellen und dann algorithmen anwenden einfach for the lullz
# TODO Natuerlich nur optional
# TODO mit with  verpacken
# TODO "Graphen-Mittelpunkt" berechen und den imer auf (0,0) setzen

# TODO DFS Visualisierung und ueberlegen wie ich mit Graphen umgehe die nicht integer vertices haben
# IDEE Als isomorphen graphen zu einem integer graphen betrachtemn


class GraphError(Exception):
    pass

class LoadingError(GraphError):
    pass

class DecodingError(GraphError):
    pass


class Graph:
    """
    Class for representing graphs
    """
    def __init__(self, filepath: str = None, adjacency_list: AdjacencyList = None,
                 adjacency_matrix: AdjacencyMatrix = None, version = 0) -> None:
        """
        Note: All the variables are exlusive, that means if on is supplied the others should not be used
        :param filepath: The path from which the graph should be loaded
        :param adjacency_list: The ajd. list from which the graph should be load
        :param adjacency_matrix:
        """
        # Filepath to the grad which should be loaded
        self.filepath = filepath
        # 2d list. which holds all adjacent nodes in the form of and adjacency list
        self.adjacency_list = adjacency_list
        # 2d list. which holds all adjacent nodes in the form of and adjacency matrix
        self.adjacency_matrix = adjacency_matrix
        # Total number of vertices
        self.vertice_count = None
        self.j = None
        self.version = 0

        self.values = list()

        # Load from a file
        # https://stackoverflow.com/questions/1369526/what-is-the-python-keyword-with-used-for
        if filepath:
            logger.info("Loading from" + filepath)
            # print("Loading from " + filepath)
            # Get file descriptor
            try:
                f = open(self.filepath, "r")
                try:
                    # Load data into the adjacency_list
                    self.j = json.load(f)
                    self.version = self.j["version"]
                    if self.version == 0:
                        self.adjacency_list = self.j["adj_list"]
                        logger.info("Adjacency list" + str(self.adjacency_list))
                    if self.version == 1:
                        self.adjacency_list = self.convert_from_adjacency_matrix(self.j["adj_matrix"])
                    # Load values for the nodes(Optional)
                    try:
                        self.values = self.j["values"]
                        logger.debug("Values are %s", self. values)
                    except KeyError:
                        logger.debug("Values list is not specified")
                except json.JSONDecodeError:
                    logger.error("Colud not decode " + filepath + "to Json")
                    raise DecodingError
            except FileNotFoundError:
                logger.error("Could not load" + filepath)
                raise LoadingError
            finally:
                # Close file
                f.close()
        else:
            if self.adjacency_matrix is not None:
                self.adjacency_list = self.convert_from_adjacency_matrix(self.adjacency_matrix)
            self.version = version
        # Get the vertice count
        self.vertice_count = len(self.adjacency_list)
        self.is_binary_tree = False
        self.node_id = 0

    @classmethod
    def from_file(cls, filepath: str) -> 'Graph':
        """
        :param filepath: The file from which the graph sould be loaded
        :return:  A new graph instance
        """
        return cls(filepath=filepath)

    @classmethod
    def from_adjacency_list(cls, adjacency_list: AdjacencyList, version) -> 'Graph':
        """
        :param adjacency_list: The adj. list from which the graph sould be loaded
        :return:  A new graph instance
        """
        return cls(adjacency_list=adjacency_list, version=version)

    @classmethod
    def from_adjacency_matrix(cls, adjacency_matrix: AdjacencyMatrix, version) -> 'Graph':
        """
        :param adjacency_matrix: The adj. matrix from which the graph sould be loaded
        :return: A new graph instance
        """
        return cls(adjacency_matrix=adjacency_matrix, version=version)

    def convert_from_adjacency_matrix(self, matrix):
        adj_list = list()
        row_count = len(matrix)
        column_count = len(matrix[0])

        for y, value in enumerate(matrix):
            #add new node per row
            #print(value)
            adj_list.append([])
            for x, value2 in enumerate(matrix[y]):
                if matrix[y][x]:
                    adj_list[y].append(x)
                #print("(%s,%s)" % (y,x))

        return adj_list


    def adjacent_to(self, node: int) -> AdjacencyListEntry:
        """
        :param node: The node from which you want the ajd. list
        :return: adjacency_list from the give node
        """
        return self.adjacency_list[node]

    def root_index(self):
        """Returns the  index of the root"""
        if self.is_binary_tree:
            return 0
        return -1

    def traverse_binary_tree(self, index):
        # pylint: disable=C1801
        """Traverse the whole binary tree"""
        if len(self.adjacency_list) > 0:
            if index == 0:
                for child_index in self.adjacency_list[0]:
                    self.traverse_binary_tree(child_index)
            else:
                # print("TRAV", index)
                # In current node has children(>1 because every node has its parent node as an adj. list entry)
                if len(self.adjacency_list[index]) > 1:
                    for counter in range(1, len(self.adjacency_list[index])):
                        self.traverse_binary_tree(self.adjacency_list[index][counter])
                else:
                    pass

        else:
            print("Cant traverse an emtpy graph")

    def subtree_index(self, index):
        # pylint: disable=C1801
        """
        Calculates all indices of of the subtree from node[index]
        :param index: The index to the node from which you want the subtree 
        :return: A List made of the indices to the nodes of the subtree 
        """
        indices = []
        if len(self.adjacency_list) > 0:
            if index == 0:
                indices.append(0)
                for child_index in self.adjacency_list[0]:
                    self.traverse_binary_tree(child_index)
            else:
                indices.append(index)
                # In current node has children(>1 because every node has its parent node as an adj. list entry)
                if len(self.adjacency_list[index]) > 1:
                    for counter in range(1, len(self.adjacency_list[index])):
                        self.traverse_binary_tree(self.adjacency_list[index][counter])
                else:
                    pass

        else:
            print("Cant traverse an emtpy graph")

        return indices

    def parent(self, index):
        """
        Calculates the index from to parent from node[index]
        :param index: The index of the node from which you want the parent
        :return: The parent of node[index] or -1 if you ask for the parent of the root
        """
        if index == 0:
            return -1
        return self.adjacency_list[index][0]

    def dist_from_root(self, index):
        """
        Calculates the distance from root to node[index], should be the number of edges
        :param index: The index of the node from which you want the distance
        :return: The distance from root to node[index]  
        """
        if index == 0:
            return 0
        return self.dist_from_root(self.parent(index)) + 1

    def left(self, index):
        """
        Get the index left child of index
        :param index: index of the node from which you wan't the left child index
        :return: The index oft the left child of index or -1 if node[index] doesnt exist
        """
        try:
            if index == self.root_index():
                index = self.adjacency_list[index][0]
            else:
                index = self.adjacency_list[index][1]
            return index
        except IndexError:
            return -1

    def right(self, index):
        """
        Get the index right child of index
        :param index: index of the node from which you wan't the right child index
        :return: The index of the right child of index or -1 if node[index] doesnt exist
        """
        try:
            if index == self.root_index():
                index = self.adjacency_list[index][1]
            else:
                index = self.adjacency_list[index][2]
            return index
        except IndexError:
            return -1



class EmptyGraphError(Exception):
    pass
