from graphvisual import  GraphVisual
from graph import Graph

class SexyTree:

    def __init__(self, graph_visuals, graph, canvas_width, canvas_height):
        self.graph_visuals = graph_visuals
        self.canvas_width = canvas_width
        self.canvas_length = canvas_height
        self.graph = graph
        self.max_height = -1

        for x in range(0, len(self.graph.adjacency_list)):
            height = self.graph.dist_from_root(x)
            if height > self.max_height:
                self.max_height = height

        print("max height", self.max_height)



    def do_sexy(self):
        nexts = [100] * (self.max_height+2)
        depths = [0] * len(self.graph.adjacency_list)
        print("LEN", len(nexts))
        def pos(index, depth):
            curr_node = self.graph_visuals.graph_nodes[index]
            print("DEPTH", depth)
            posit = nexts[depth]
            # Wenn diese if zutrifft kann direkt links von mir kein Knoten sein
            # also koennen wir eine positon nach links gehen ohne wen zu treffen
            if nexts[depth] < depths[self.graph.parent(index)]:
                posit = depths[self.graph.parent(index)]-100
                nexts[depth] = posit
            curr_node.set_pos(posit, (depth*100)+50)
            depths[index] = nexts[depth]
            nexts[depth] = nexts[depth] + 100

            if index == 0:
                pos(self.graph_visuals.node_adjacency_list[curr_node.id][0].id, depth + 1)
            for x in range(1, len(self.graph_visuals.node_adjacency_list[curr_node.id])):
                pos(self.graph_visuals.node_adjacency_list[curr_node.id][x].id, depth + 1)

        pos(0, 0)

        def pos2(index, depth):
            curr_node = self.graph_visuals.graph_nodes[index]
            curr_node.move(-50*depth, 0)
            if index == 0:
                pos2(self.graph_visuals.node_adjacency_list[curr_node.id][0].id, depth + 1)
            for x in range(1, len(self.graph_visuals.node_adjacency_list[curr_node.id])):
                pos2(self.graph_visuals.node_adjacency_list[curr_node.id][x].id, depth + 1)

        # pos2(0,0)








            # for node in self.graph_visuals.graph_nodes:
            #     dist = self.graph.dist_from_root(node.id)
            #     node.set_pos(node.position.x, dist * 100 )
        print("DID SEXY")
# current = 0
#         next_x = [1]*self.max_height
#         status = [1]*len(self.graph.adjacency_list)
#         for x in range(1, len(status)):
#             status[x] = len(self.graph.adjacency_list[x])
#         status[0] = 0
#
#
#
#
#         while current != -1:
#             print("CUR", current)
#             if status[current] == 0:
#                 print("Interesting Step")
#                 dist = self.graph.dist_from_root(current)
#                 self.graph_visuals.graph_nodes[current].set_pos(next_x[dist], dist*100 )
#                 next_x[dist] = next_x[dist] + 2
#                 for son_index in range(1, len(self.graph.adjacency_list[current])):
#                     status[son_index] = 0
#                 status[current] = 1
#             elif 1 <=  status[current] and status[current] <= len(self.graph.adjacency_list[current]):
#                 print("2nd")
#                 status[current] = status[current] + 1
#                 print("Status[current]", status[current])
#                 try:
#                     current = self.graph.adjacency_list[current][status[current]-1]
#                 except IndexError:
#                     print("ERRCUr", current)
#                     print("ERRCHildINdex", status[current]-1)
#                     current = self.graph.parent(current)
#             else:
#                 print("3d")
#                 current = self.graph.parent(current)
