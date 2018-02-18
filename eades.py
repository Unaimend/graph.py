import graph
from vector import Vector
import math

# TODO Bessere Konstanten errechnen
# TODO Der Benutzer kann fuer die Eades KOsntanten Null eingeben, dies muss verhindert werden da Null in einigen Berechnungen ein nicht
# zulaessiger Wert ist


class Eades:
    graph_visuals = None

    # Graph konv. langsamer gegen gleichgewicht besonderns bei hoher Anzahl an Iterationen
    c1 = 2
    # Beeinflust min. distance
    c2 = 200
    c3 = 300
    # Beeinflusstt die konv. Gesch.
    c4 = 0.1

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

    @staticmethod
    def calculate_attractive_force_for_all_nodes_and_move_accordingly_new(event=None):
        # TODO Exception falls Eades.graph == None
        for node in Eades.graph_visuals.graphNodes:
            displacement = Vector(0, 0)
            for nodes in Eades.graph_visuals.node_adjacency_list[node.id]:
                # If if would calc. the distance between two node which have the same id, the distance would be 0
                # and log(0) is undefined
                if node.id != nodes.id:
                    distance = Eades.distance(node, nodes)
                    attractive_force = Eades.c1 * math.log(distance / Eades.c2)
                    direction = Eades.unit_vector(nodes, node)
                    displacement.x += direction.x  * attractive_force * Eades.c4
                    displacement.y += direction.y  * attractive_force * Eades.c4
            node.move(displacement.x, displacement.y )

    @staticmethod
    def calculate_repelling_force_for_all_nodes_and_move_accordingly_new():
        for node in Eades.graph_visuals.graphNodes:
            displacement = Vector(0, 0)
            for nodes in Eades.graph_visuals.graphNodes:
                repelling_force = 0
                # If if would calc. the distance between two node which have the same id, the distance would be 0
                # and that would mean that I would divide by 0 in the attractive_force calculation
                if node.id != nodes.id:
                    distance = Eades.distance(node, nodes)
                    repelling_force = (Eades.c3 / (distance ** 2))
                    direction = Eades.unit_vector(node, nodes)
                    displacement.x += direction.x * repelling_force * Eades.c4
                    displacement.y += direction.y * repelling_force * Eades.c4
            node.move(displacement.x, displacement.y )
















