import graph
import Vector
import math


# TODO Eine minimal Distanz benutzen um dafür zu sorgen dass die nodes nicht "verschmelzen"

class Eades:
    graph_visuals = None

    # Graph konv. langsamer gegen gleichgewicht besonderns bei hoher Anzahl an Iterationen
    c1 = 2
    c2 = 25
    c3 = 1
    c4 = 0.1


    # c1 = 2
    # c2 = 1
    # # c3 = 10000
    # c3 = 1
    # c4 = 0.1

    c1 = 2
    c2 = 1
    # c3 = 10000
    c3 = 1
    c4 = 0.1


    @staticmethod
    # TODO UNITTESSSSTTSSSSSSS
    def distance(node1: graph.GraphNode = None, node2: graph.GraphNode = None):
        #Pythagorean theorem in R^2(euclidean distance in R^2)
        distance = math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)
        return distance

    @staticmethod
    def unit_vector(node1: graph.GraphNode = None, node2: graph.GraphNode = None):
        # Calculate x and y distance separate
        v = Vector.Vector(node1.x - node2.x, node1.y - node2.y)
        # Divide vector by its length to obtain a unit vector
        v = Vector.Vector(v.x / Eades.distance(node1, node2), v.y / Eades.distance(node1, node2))
        return v

    # TODO Bessere Konstanten errechnen

    # TODO  Unit Vector gibt halt 2 ergebniss(vorzeichen) haengt von der richtung ab
    @staticmethod
    def calculate_attractive_force_for_all_nodes_and_move_accordingly(event = None):
        # TODO Exception falls Eades.graph == None
        for node in Eades.graph_visuals.graphNodes:
            for nodes in Eades.graph_visuals.node_adjacency_list[node.id]:
                # If if would calc. the distance between two node which have the same id, the distance would be 0
                # and that would mean that I would divide by 0 in the attractive_force calculation
                if node.id != nodes.id:
                    distance = Eades.distance(node, nodes)
                    attractive_force = Eades.c1 * math.log( distance/Eades.c2)
                    # TODO Vorzeichen des unit vec.(sollte so stimmen)
                    direction = Eades.unit_vector(nodes, node)
                    node.move(direction.x * attractive_force* Eades.c4, direction.y * attractive_force* Eades.c4)

    @staticmethod
    def calculate_repelling_force_for_all_nodes_and_move_accordingly(event = None):
        for node in Eades.graph_visuals.graphNodes:
            for nodes in Eades.graph_visuals.graphNodes:
                if node.id != nodes.id:
                    distance = Eades.distance(node, nodes)
                    attractive_force = (Eades.c3 / (distance**2))
                    # TODO Vorzeichen des unit vec.
                    direction = Eades.unit_vector(node, nodes)
                    node.move(direction.x * attractive_force * Eades.c4, direction.y * attractive_force * Eades.c4)



