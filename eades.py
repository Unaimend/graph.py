import graph
from vector import Vector
import math

# TODO Bessere Konstanten errechnen
# TODO Der Benutzer kann fuer die self KOsntanten Null eingeben, dies muss verhindert werden da Null in einigen Berechnungen ein nicht
# zulaessiger Wert ist


class Eades:
    def __init__(self, graph_visuals):
        self.graph_visuals = graph_visuals

        # Graph konv. langsamer gegen gleichgewicht besonderns bei hoher Anzahl an Iterationen
        self.c1 = 2
        # Beeinflust min. distance
        self.c2 = 200
        self.c3 = 300
        # Beeinflusstt die konv. Gesch.
        self.c4 = 0.1

    # c1 = 2
    # c2 = 1
    # # c3 = 10000
    # c3 = 1
    # c4 = 0.1

    # c1 = 2
    # c2 = 1
    # # c3 = 10000
    # c3 = 1
    # c4 = 0.1

    # 2,200,5000,0.1
    @staticmethod
    def distance(node1: graph.GraphNode, node2: graph.GraphNode) -> float:
        # Pythagorean theorem in R^2(euclidean distance in R^2)
        distance = math.sqrt((node1.position.x - node2.position.x) ** 2 + (node1.position.y - node2.position.y) ** 2)
        return distance
    @staticmethod
    def unit_vector(node1: graph.GraphNode, node2: graph.GraphNode) -> float:
        # Calculate x and y distance separate
        v = Vector(node1.position.x - node2.position.x, node1.position.y - node2.position.y)
        # Divide vector by its length to obtain a unit vector
        v = Vector(v.x / Eades.distance(node1, node2), v.y / Eades.distance(node1, node2))
        return v

    def calculate_attractive_force_for_all_nodes_and_move_accordingly_new(self, event=None):
        # TODO Exception falls self.graph == None
        for node in self.graph_visuals.graphNodes:
            displacement = Vector(0, 0)
            for nodes in self.graph_visuals.node_adjacency_list[node.id]:
                # If if would calc. the distance between two node which have the same id, the distance would be 0
                # and log(0) is undefined
                if node.id != nodes.id:
                    distance = Eades.distance(node, nodes)
                    attractive_force = self.c1 * math.log(distance / self.c2)
                    direction = Eades.unit_vector(nodes, node)
                    displacement.x += direction.x  * attractive_force * self.c4
                    displacement.y += direction.y  * attractive_force * self.c4
            node.move(displacement.x, displacement.y )

    def calculate_repelling_force_for_all_nodes_and_move_accordingly_new(self, event=None):
        for node in self.graph_visuals.graphNodes:
            displacement = Vector(0, 0)
            for nodes in self.graph_visuals.graphNodes:
                repelling_force = 0
                # If if would calc. the distance between two node which have the same id, the distance would be 0
                # and that would mean that I would divide by 0 in the attractive_force calculation
                if node.id != nodes.id:
                    distance = self.distance(node, nodes)
                    repelling_force = (self.c3 / (distance ** 2))
                    direction = self.unit_vector(node, nodes)
                    displacement.x += direction.x * repelling_force * self.c4
                    displacement.y += direction.y * repelling_force * self.c4
            node.move(displacement.x, displacement.y )
















