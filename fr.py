""" Module which implements the layouting-algorithm from FR[91]
"""
import math
import graph
from vector import Vector


# Dises Modul implementiert den Layouting-Algorithmus von T. Fruchterman und E. Reingold
# aus dem Paper Graph Drawing by Force-directed Placement [FR91]


class FruchtermanReingold:
    """ Class which implements the layouting-algorithm from EAD[84]
    """
    graph_visuals = None
    canvas_width = None
    canvas_length = None
    displacement_list = []

    area = None
    k = None
    t = 0
    # In dem Paper hat jede Node ein displacement attribut welchens bei meiner Implementierung
    # nicht vorhanden ist dieses Attribut simuliere ich dadurch das ich fuer jede node die verschiebung
    # berechne und in der Liste speichere. an [0] steht also der Wert um den die Node mit der Id 0
    # verschoben werden soll etc.
    # TODO UNITTESSSSTTSSSSSSS

    @staticmethod
    def distance(node1: graph.GraphNode, node2: graph.GraphNode) -> float:
        # TODO Die funktion gehoert hier nicht hin(doppelt) siehe ead.
        """
        Calculates the distance between two nodes
        :param node1: The "start" node
        :param node2: The "end" node
        :return: The distance between the two nodes
        """
        # Pythagorean theorem in R^2(euclidean distance in R^2)
        x_diff = node1.position.x - node2.position.x
        y_diff = node1.position.y - node2.position.y
        distance = math.sqrt(x_diff ** 2 + y_diff ** 2)
        return distance

    @staticmethod
    def unit_vector(node1: graph.GraphNode, node2: graph.GraphNode) -> Vector:
        """
        Calculates the unit vector between two given nodes
        :param node1: The "start" node
        :param node2: The "end" node
        :return: The unit vector between two given nodes
        """
        # Calculate x and y distance separate
        unit_vec = Vector(node1.position.x - node2.position.x, node1.position.y - node2.position.y)
        # Divide vector by its length to obtain a unit vector
        x_comp = unit_vec.x / FruchtermanReingold.distance(node1, node2)
        y_comp = unit_vec.y / FruchtermanReingold.distance(node1, node2)
        unit_vec = Vector(x_comp, y_comp)
        return unit_vec

    @staticmethod
    def fr(distance: float) -> float:
        """
        Calculates the repulsive force for a given distance
        :param distance:  
        :return: The repulsive force for the distance
        """
        if FruchtermanReingold.k is None:
            # TODO Hier formel hinschreiben die im paper verwendet werden
            raise ValueError("Area and k must be precalculated(see paper)")
        else:
            return (FruchtermanReingold.k ** 2) / distance

    @staticmethod
    def fa(distance: float) -> float:
        """
        Calculates the attractive force for the distance
        :param distance:  
        :return: The attractive force for the distance
        """
        if FruchtermanReingold.k is None:
            raise ValueError("Area and k must be precalculated(see paper)")
        else:
            return (distance ** 2) / FruchtermanReingold.k

    @staticmethod
    def calc_repelling_forces():
        """
        Calculates and "anwenden" the attractive forces 
        """
        # TODO WIe sorgge ich dafuer das die dispalcement lsite hier garantiert lange genug ist
        # Diese MEthode berechnet die abstossenden Kraefte
        # BUG  Ist diese(displacement list) Liste hier moeglicherweise
        # mit nicht nullwerete gefuellt was den algo. kaputmacht
        for node in FruchtermanReingold.graph_visuals.graphNodes:
            for nodes in FruchtermanReingold.graph_visuals.graphNodes:
                if node.id != nodes.id:
                    diff = node.position - nodes.position
                    diff_length = diff.abs()
                    scaled_x = diff.to_unit().x * FruchtermanReingold.fr(diff_length)
                    scaled_y = diff.to_unit().y * FruchtermanReingold.fr(diff_length)
                    scaled_unit = Vector(scaled_x, scaled_y)
                    new_force = FruchtermanReingold.displacement_list[node.id] + scaled_unit
                    FruchtermanReingold.displacement_list[node.id] = new_force

    @staticmethod
    def calc_attractive_forces():
        """
        Calculates and "anwenden" the attractive forces 
        """
        for edge in FruchtermanReingold.graph_visuals.graphEdges:
            diff = edge.start_node.position - edge.end_node.position
            diff_length = diff.abs()
            scaled_x_comp = diff.to_unit().x * FruchtermanReingold.fa(diff_length)
            scaled_y_comp = diff.to_unit().y * FruchtermanReingold.fa(diff_length)
            scaled_unit = Vector(scaled_x_comp, scaled_y_comp)
            # Nomma ins paper schauen
            start_force = FruchtermanReingold.displacement_list[edge.start_node.id] - scaled_unit
            end_force = FruchtermanReingold.displacement_list[edge.end_node.id] + scaled_unit
            FruchtermanReingold.displacement_list[edge.start_node.id] = start_force
            FruchtermanReingold.displacement_list[edge.end_node.id] = end_force

    @staticmethod
    def cool():
        """
        Implements the cooling from the paper
        :return: Nothing 
        """
        FruchtermanReingold.t = FruchtermanReingold.t - 1




