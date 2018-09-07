""" Module which implements the layouting-algorithm from EAD[84]
"""
import math
from vector import Vector
from utils import distance as util_distance, unit_vector

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


    def calculate_attractive_force_for_all_nodes_and_move_accordingly_new(self, event=None):
        """
        :param event: Only there because the tkinter bind functions expects the function to have one parameter
        :return Nothing
        """
        # pylint: disable= W0613
        # TODO Exception falls self.graph == None
        for node in self.graph_visuals.graph_nodes:
            displacement = Vector(0, 0)
            for nodes in self.graph_visuals.node_adjacency_list[node.id]:
                # If if would calc. the distance between two node which have the same id,
                # the distance would be 0 and log(0) is undefined
                if node.id != nodes.id:
                    distance = util_distance(node, nodes)
                    attractive_force = self.constant_1 * math.log(distance / self.constant_2)
                    direction = unit_vector(nodes, node)
                    displacement.x += direction.x * attractive_force * self.constant_4
                    displacement.y += direction.y * attractive_force * self.constant_4
            node.move(displacement.x, displacement.y)

    def calculate_repelling_force_for_all_nodes_and_move_accordingly_new(self, event=None):
        """
        :param event: Only there because the tkinter bind functions expects the function to have one parameter
        """
        # pylint: disable= W0613
        for node in self.graph_visuals.graph_nodes:
            displacement = Vector(0, 0)
            for nodes in self.graph_visuals.graph_nodes:
                # If if would calc. the distance between two node which have the same id,
                # the distance would be 0  and that would mean that I would divide by 0 in the
                # attractive_force calculation
                if node.id != nodes.id:
                    distance = util_distance(node, nodes)
                    repelling_force = (self.constant_3 / (distance ** 2))
                    direction = unit_vector(node, nodes)
                    displacement.x += direction.x * repelling_force * self.constant_4
                    displacement.y += direction.y * repelling_force * self.constant_4
            node.move(displacement.x, displacement.y)
