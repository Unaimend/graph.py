
<style>
a.member_var   {color: #32ce25;}
a.member_func   {color: #32ce25;}
</style>

# Class: GraphVisual

##Description:
This class encapsulates variables and functions for drawing graphs

##Member variables:

<a class="member_var">canvas:</a> tk.Canvas

<a class="member_var">window:</a> [Window](classes/window.md)

<a class="member_var">graph_nodes_min_distance:</a> int

<a class="member_var">graph_nodes:</a> List[GraphNode]

<a class="member_var">graph_edges:</a> List[GraphEge]

<a class="member_var">node_adjacency_list:</a> List[GraphNode]

<a class="member_var">width:</a> float

<a class="member_var">height:</a> float

<a class="member_var">graph:</a> Graph

<a class="member_var">clicked_nodes:</a> List[GraphNode]

<a class="member_var">draw_node_ids:</a> bool

<a class="member_var">node_counter:</a> int

<a class="member_var">current_selected_node:</a>

<a class="member_var">current_info:</a> NodeInfo

##Member functions

<a class="member_func">from_graph</a>

<a class="member_func">inc_zoomlevel</a>

<a class="member_func">dec_zoomlevel</a>

<a class="member_func">int_node_to_graph_node</a>

<a class="member_func">generate_adj_list</a>

<a class="member_func">redraw_nodes</a>

<a class="member_func">generate_edges</a>

<a class="member_func">redraw_graph</a>

<a class="member_func">select_node</a>


##Static functions

<a class="member_func">set_focus</a>
