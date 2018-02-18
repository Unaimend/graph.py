import graph
from vector import Vector
import math

# Dises Modul implementiert den Layouting-Algorithmus von T. Fruchterman und E. Reingold
# aus dem Paper Graph Drawing by Force-directed Placement [FR91]


class FruchtermanReingold:
    graph_visuals = None
    canvas_width = None
    canvas_length = None
    displacement_list = []

    area = None
    k = None
    t = 0
    # In dem Paper hat jede Node ein displacement attribut welchens bei meiner Implementierung nicht vorhanden ist
    # dieses Attribut simuliere ich dadurch das ich fuer jede node die verschiebung berechne und in der Liste
    # speichere. an [0] steht also der Wert um den die Node mit der Id 0 verschoben werden soll etc.
    # TODO UNITTESSSSTTSSSSSSS
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
        v = Vector(v.x / FruchtermanReingold.distance(node1, node2), v.y / FruchtermanReingold.distance(node1, node2))
        return v

    @staticmethod
    def fr(z: float) -> float:
        if FruchtermanReingold.k is None:
            raise ValueError("Area and k must be precalculated")
        else:
            return (FruchtermanReingold.k ** 2) / z
    @staticmethod
    def fa(z : float) -> float:
        if FruchtermanReingold.k is None:
            raise ValueError("Area and k must be precalculated")
        else:
            return (z ** 2) / FruchtermanReingold.k

    @staticmethod
    def calc_repelling_forces():
        #print("LENGTH", len(FruchtermanReingold.displacement_list))
        #TODO WIe sorgge ich dafuer das die dispalcement lsite hier garantiert lange genug ist
        # Diese MEthode berechnet die abstossenden Kraefte
        #BUG  Ist diese Liste hier moeglicherweise mit nicht nullwerete gefuellt was den algo. kaputmacht
        for node in FruchtermanReingold.graph_visuals.graphNodes:
            for nodes in FruchtermanReingold.graph_visuals.graphNodes:
                if node.id != nodes.id:
                    diff = node.position - nodes.position
                    diff_length = diff.abs()
                    #print("FR", FruchtermanReingold.fr(diff_length))
                    scaled_x = diff.to_unit().x * FruchtermanReingold.fr(diff_length)
                    scaled_y = diff.to_unit().y * FruchtermanReingold.fr(diff_length)
                    scaled_unit = Vector(scaled_x, scaled_y)
                    FruchtermanReingold.displacement_list[node.id] = FruchtermanReingold.displacement_list[node.id] + scaled_unit

    @staticmethod
    def calc_attractive_forces():
        for edge in FruchtermanReingold.graph_visuals.graphEdges:

            #print("START", edge.start_node.position, "END", edge.end_node.position)
            diff = edge.start_node.position - edge.end_node.position

            #print("Difference", diff)
            diff_length = diff.abs()
            #print("FA", FruchtermanReingold.fa(diff_length))
            scaled_x = diff.to_unit().x * FruchtermanReingold.fa(diff_length)
            scaled_y = diff.to_unit().y * FruchtermanReingold.fa(diff_length)
            scaled_unit = Vector(scaled_x, scaled_y)
            #print("SCU", scaled_unit)
            FruchtermanReingold.displacement_list[edge.start_node.id] = FruchtermanReingold.displacement_list[edge.start_node.id] - scaled_unit

            FruchtermanReingold.displacement_list[edge.end_node.id] = FruchtermanReingold.displacement_list[edge.end_node.id] + scaled_unit
            # print(edge.start_node.id, edge.end_node.id)

    @staticmethod
    def cool():
        FruchtermanReingold.t = FruchtermanReingold.t - 1




