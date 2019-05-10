
from graph import Graph
def n_circle(n):
    l = list()
    for i in range(1, n):
        l.append([i])
    l.append([0])

    print(l)
    return Graph.from_adjacency_list(l,0)
