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
    def __init__(self, graph_visuals, canvas_width, canvas_height, k, t):
        self.graph_visuals = graph_visuals
        self.canvas_width = canvas_width
        self.canvas_length = canvas_height
        self.displacement_list = []

        self.area = canvas_width * canvas_height
        self.k = k
        self.t = t

    # In dem Paper hat jede Node ein displacement attribut welchens bei meiner Implementierung
    # nicht vorhanden ist dieses Attribut simuliere ich dadurch das ich fuer jede node die verschiebung
    # berechne und in der Liste speichere. an [0] steht also der Wert um den die Node mit der Id 0
    # verschoben werden soll etc.
    def do_fr(self, how_often: int):
        """
        "EXECUTes the algorithm
        :param how_often: How often the fr algorithm should be executed 
        :return: 
        """
        for x in range(0, how_often):
            # Das hier in Funk. do_fr_one_iter
            self.displacement_list = [Vector(0, 0)] * self.graph_visuals.node_counter
            self.calc_attractive_forces()

            self.calc_repelling_forces()
            i = 0
            for disp in self.displacement_list:
                v = min(disp.abs(), self.t)
                direction = Vector(disp.to_unit().x * v, disp.to_unit().y * v)
                self.graph_visuals.graph_nodes[i].move(direction.x, direction.y)
                i = i + 1
            self.cool()


    def fr(self, distance: float) -> float:
        """
        Calculates the repulsive force for a given distance
        :param distance:  
        :return: The repulsive force for the distance
        """
        if self.k is None:
            # TODO Hier formel hinschreiben die im paper verwendet werden
            raise ValueError("Area and k must be precalculated(see paper)")
        else:
            return (self.k ** 2) / distance

    def fa(self, distance: float) -> float:
        """
        Calculates the attractive force for the distance
        :param distance:  
        :return: The attractive force for the distance
        """
        if self.k is None:
            raise ValueError("Area and k must be precalculated(see paper)")
        else:
            return (distance ** 2) / self.k

    def calc_repelling_forces(self):
        """
        Calculates and "anwenden" the attractive forces 
        """
        # TODO WIe sorgge ich dafuer das die dispalcement lsite hier garantiert lange genug ist
        # Diese MEthode berechnet die abstossenden Kraefte
        # BUG  Ist diese(displacement list) Liste hier moeglicherweise
        # mit nicht nullwerete gefuellt was den algo. kaputmacht
        for node in self.graph_visuals.graph_nodes:
            for nodes in self.graph_visuals.graph_nodes:
                if node.id != nodes.id:
                    diff = node.position - nodes.position
                    diff_length = diff.abs()
                    scaled_x = diff.to_unit().x * self.fr(diff_length)
                    scaled_y = diff.to_unit().y * self.fr(diff_length)
                    scaled_unit = Vector(scaled_x, scaled_y)
                    new_force = self.displacement_list[node.id] + scaled_unit
                    self.displacement_list[node.id] = new_force

    def calc_attractive_forces(self):
        """
        Calculates and "anwenden" the attractive forces 
        """
        for edge in self.graph_visuals.graph_edges:
            diff = edge.start_node.position - edge.end_node.position
            diff_length = diff.abs()
            scaled_x_comp = diff.to_unit().x * self.fa(diff_length)
            scaled_y_comp = diff.to_unit().y * self.fa(diff_length)
            scaled_unit = Vector(scaled_x_comp, scaled_y_comp)
            # Nomma ins paper schauen
            start_force = self.displacement_list[edge.start_node.id] - scaled_unit
            end_force = self.displacement_list[edge.end_node.id] + scaled_unit
            self.displacement_list[edge.start_node.id] = start_force
            self.displacement_list[edge.end_node.id] = end_force

    def cool(self):
        """
        Implements the cooling from the paper
        :return: Nothing 
        """
        self.t = self.t - 1
