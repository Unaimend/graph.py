""" Module which implements the layouting-algorithm from EAD[84]
"""
import math
import graph
from vector import Vector


# TODO Bessere Konstanten errechnen
# TODO Der Benutzer kann fuer die self KOsntanten Null eingeben,
# dies muss verhindert werden da Null in einigen Berechnungen ein nicht
# zulaessiger Wert ist


class Eades:
    """ Class which implements the layouting-algorithm from EAD[84]
    """
    def __init__(self, graph_visuals):
        self.graph_visuals = graph_visuals

        # Graph konv. langsamer gegen gleichgewicht besonderns bei hoher Anzahl an Iterationen
        self.constant_1 = 2
        # Beeinflust min. distance
        self.constant_2 = 200
        self.constant_3 = 300
        # Beeinflusstt die konv. Gesch.
        self.constant_4 = 0.1


    @staticmethod
    def distance(node1: graph.GraphNode, node2: graph.GraphNode) -> float:
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

    @staticmethod
    # TODO Die funktion gehoert hier nicht hin.
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
        unit_vec = Vector(unit_vec.x / Eades.distance(node1, node2), unit_vec.y / Eades.distance(node1, node2))
        return unit_vec

    def calculate_attractive_force_for_all_nodes_and_move_accordingly_new(self, event=None):
        """
        :param event: Only there because the tkinter bind functions expects the function to have one parameter
        :return Nothing
        """
        # pylint: disable= W0613
        # TODO Exception falls self.graph == None
        for node in self.graph_visuals.graphNodes:
            displacement = Vector(0, 0)
            for nodes in self.graph_visuals.node_adjacency_list[node.id]:
                # If if would calc. the distance between two node which have the same id,
                # the distance would be 0 and log(0) is undefined
                if node.id != nodes.id:
                    distance = Eades.distance(node, nodes)
                    attractive_force = self.constant_1 * math.log(distance / self.constant_2)
                    direction = Eades.unit_vector(nodes, node)
                    displacement.x += direction.x * attractive_force * self.constant_4
                    displacement.y += direction.y * attractive_force * self.constant_4
            node.move(displacement.x, displacement.y)

    def calculate_repelling_force_for_all_nodes_and_move_accordingly_new(self, event=None):
        """
        :param event: Only there because the tkinter bind functions expects the function to have one parameter
        """
        # pylint: disable= W0613
        for node in self.graph_visuals.graphNodes:
            displacement = Vector(0, 0)
            for nodes in self.graph_visuals.graphNodes:
                # If if would calc. the distance between two node which have the same id,
                # the distance would be 0  and that would mean that I would divide by 0 in the
                # attractive_force calculation
                if node.id != nodes.id:
                    distance = self.distance(node, nodes)
                    repelling_force = (self.constant_3 / (distance ** 2))
                    direction = self.unit_vector(node, nodes)
                    displacement.x += direction.x * repelling_force * self.constant_4
                    displacement.y += direction.y * repelling_force * self.constant_4
            node.move(displacement.x, displacement.y)
















