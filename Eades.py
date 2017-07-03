import Graph
import Vector
import math



class Eades:
    graph = None
    c1 = 2
    c2 = 1
    c3 = 3
    c4 = 0.1



    @staticmethod
    # TODO UNITTESSSSTTSSSSSSS
    def distance(node1: Graph.GraphNode = None, node2: Graph.GraphNode = None):
        #Pythagorean theorem in R^2(euclidean distance in R^2)
        distance = math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)
        return distance

    @staticmethod
    def unit_vector(node1: Graph.GraphNode = None, node2: Graph.GraphNode = None):
        # Calculate x and y distance separate
        v = Vector.Vector(node1.x - node2.x, node1.y - node2.y)
        # Divide vector by its length to obtain a unit vector
        v = Vector.Vector(v.x / Eades.distance(node1, node2), v.y / Eades.distance(node1, node2))
        return v

    @staticmethod
    def calculate_attractive_force_for_all_nodes_and_move_accordingly(event = None):
        # TODO Exception falls Eades.graph == None
        for node in Eades.graph.graphNodes:
            for nodes in Eades.graph.node_adjacency_list[node.id]:
                distance = Eades.distance(node, nodes)
                attractive_force = Eades.c1 * math.log(Eades.c2 / distance)
                direction = Eades.unit_vector(node, nodes)
                node.move(direction.x * attractive_force* Eades.c4, direction.y * attractive_force* Eades.c4)

    @staticmethod
    def calculate_repelling_force_for_all_nodes_and_move_accordingly(event = None):
        for node in Eades.graph.graphNodes:
            for nodes in Eades.graph.graphNodes:
                if node.id != nodes.id:
                    distance = Eades.distance(node, nodes)
                    attractive_force = Eades.c3 / (distance**2)
                    direction = Eades.unit_vector(node, nodes)
                    node.move(direction.x * attractive_force * Eades.c4, direction.y * attractive_force * Eades.c4)



