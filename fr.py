#Dises Modul implementiert den Layouting-Algorithmus von T. Fruchterman und E. Reingold
#aus dem Paper Graph Drawing by Force-directed Placement [FR91]
class Fruchterman_Reingold:
    graph_visuals = None
    canvas_width = None
    canvas_length = None

    area = None
    k = None
    # In dem Paper hat jede Node ein displacement attribut welchens bei meiner Implementierung nicht vorhanden ist
    # dieses Attribut simuliere ich dadurch das ich fuer jede node die verschiebung berechne und in der Liste
    # speichere. an [0] steht also der Wert um den die Node mit der Id 0 verschoben werden soll etc.
    dispalcement_list = []
    @staticmethod
    # TODO UNITTESSSSTTSSSSSSS
    def distance(node1: graph.GraphNode = None, node2: graph.GraphNode = None):
        # Pythagorean theorem in R^2(euclidean distance in R^2)
        distance = math.sqrt((node1.position.x - node2.position.x) ** 2 + (node1.position.y - node2.position.y) ** 2)
        return distance


    @staticmethod
    def unit_vector(node1: graph.GraphNode = None, node2: graph.GraphNode = None):
        # Calculate x and y distance separate
        v = Vector(node1.position.x - node2.position.x, node1.position.y - node2.position.y)
        # Divide vector by its length to obtain a unit vector
        v = Vector(v.x / Eades.distance(node1, node2), v.y / Eades.distance(node1, node2))
        return v


    def fr(z):
        if k == None:
           raise ValueError("Area and k must be precalculated")
        else:
            return (z ** 2)/ k
    def fa(z):
        if k == None:
           raise ValueError("Area and k must be precalculated")
        else:
            return (k ** 2)/z




    def calc_attractive_forces:

        #TODO WIe sorgge ich dafuer das die dispalcement lsite hier garantiert lange genug ist
        # Diese MEthode berechnet die abstossenden Kraefte
        #BUG  Ist diese Liste hier moeglicherweise mit nicht nullwerete gefuellt was den algo. kaputmacht
        for node in Fruchterman_Reingold.graph_visuals.graphNodes:
            for nodes in Fruchterman_Reingold.graph_visuals.graphNodes:
                if node.id != nodes.id:
                    diff = node - nodes
                    diff_length = math.sqrt(diff.x ** 2 + diff.y ** 2)
                    dispalcement_list[node.id] = dispalcement_list[node.id] + diff.to_unit() * fr(diff_length)





