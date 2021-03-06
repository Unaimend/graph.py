"""
This module contains different useful functions
"""
import time
import math

import graphvisual as gv
from vector import Vector


def timeit(func, *args) -> None:
    """
    :param func: The function which should be executed
    """
    start = time.time()
    func(*args)
    end = time.time()
    print("Elapsed Time of", func.__name__, ":", end - start)


def distance(node1: gv.GraphNode, node2: gv.GraphNode) -> float:
    """
    Calculates the distance between two nodes
    :param node1: The "start" node 
    :param node2: The "end" node
    :return: The distance between the two nodes
    """
    # Pythagorean theorem in R^2(euclidean distance in R^2)
    distance = math.sqrt((node1.position.x - node2.position.x) ** 2 + (node1.position.y - node2.position.y) ** 2)
    return distance


def unit_vector(node1: gv.GraphNode, node2: gv.GraphNode) -> Vector:
    """
    Calculates the unit vector between two given nodes
    :param node1: The "start" node
    :param node2: The "end" node
    :return: The unit vector between two given nodes
    """
    # Calculate x and y distance separate
    unit_vec = Vector(node1.position.x - node2.position.x, node1.position.y - node2.position.y)
    # Divide vector by its length to obtain a unit vector
    unit_vec = Vector(unit_vec.x / distance(node1, node2), unit_vec.y / distance(node1, node2))
    return unit_vec
