from graph import Graph



class DepthFirstSearch:
    def __init__(self, graph: Graph, start_node):
        self.marked = [False] * graph.vertice_count
        self.edgeTo = [-1] * graph.vertice_count
        self.start = start_node

        self.dfs(graph, start_node)

    def dfs(self, graph: Graph, v):
        self.marked[v] = True
        for node in graph.adjacency_list[v]:
            if not self.marked[node]:
                self.edgeTo[node] = v
                self.dfs(graph, node)

    def has_path_to(self, node):
        return self.marked[node]

    def path_to(self, node):
        if not self.has_path_to(node):
            return None
        path = []
        x = node
        while x != self.start:
            path.append(x)
            x = self.edgeTo[x]
        path.append(self.start)
        return path
