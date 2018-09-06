"""
This module cotains different useful functions
"""
import time
import math
from graph import GraphNode, GraphEdge
from vector import Vector

"""
param func: The function which should be executed
"""
def timeit(func, *args) -> None:
    start = time.time()
    func(*args)
    end = time.time()
    print("Elapsed Time of", func.__name__, ":", end - start)

def distance(node1: GraphNode, node2: GraphNode) -> float:
    # TODO Die funktion gehoert hier nicht hin.
    """
    Calculates the distance between two nodes
    :param node1: The "start" node 
    :param node2: The "end" node
    :return: The distance between the two nodes
    """
    # Pythagorean theorem in R^2(euclidean distance in R^2)
    distance = math.sqrt((node1.position.x - node2.position.x) ** 2 + (node1.position.y - node2.position.y) ** 2)
    return distance

def unit_vector(node1: GraphNode, node2: GraphNode) -> Vector:
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
