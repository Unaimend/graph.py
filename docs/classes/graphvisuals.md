
<style>
a.member_var   {color: #32ce25; font-size: 18px; font-weight: bold}
a.member_func   {color: #32ce25;  font-size: 18px; font-weight: bold}
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
1. a  
2. b  
3. c  

<a class="member_func">inc_zoomlevel</a><a>(self, event=None) -> None</a>     
Calculates the misplacement which comes from zooming(which is scaling) the canvas

**Parameters**  
1. event: Needed parameter so that the function can be used with tkinter events.
</br></br>


<a class="member_func">dec_zoomlevel</a><a>(self, event=None) -> None</a>  

**Parameters**  
1. event: Needed parameter so that the function can be used with tkinter events.
</br></br>


<a class="member_func">int_node_to_graph_node</a><a>(self) -> None</a>  
Converts the list of nodes which holds integers to a list which holds GraphNodes note that the here generated list doesn't hold information about how the notes are related.
</br></br>


<a class="member_func">generate_adj_list</a><a>(self) -> None</a>  
Converts the integer ajd. list to a GraphNode adj. list.
</br></br>


<a class="member_func">redraw_nodes</a><a>(self) -> None</a>  
Deletes all the nodes and their text from the canvas and redraws them again but with updated values.
</br></br>


<a class="member_func">generate_edges</a><a>(self) -> None</a>  
Generates edges between graph nodes, can also be used to redraw edges.
</br></br>


<a class="member_func">redraw_graph</a><a>(self, event=None) -> None</a>  
Combines methods to redraw all graphical items of the graphs.

**Parameters**  
1. event: Needed parameter so that the function can be used with tkinter events.
</br></br>


<a class="member_func">change_node_look</a><a>(self, event=None) -> None</a>  
Toggles the node look from black dots to white circles white text inside and the other way around.

**Parameters**  
1. event: Needed parameter so that the function can be used with tkinter events.
</br></br>


<a class="member_func">select_node</a><a>(self, event=None) -> None</a>  
Selects a node and opens a window with important informatoion about the selected node.

**Parameters**  
1. event: Needed parameter so that the function can be used with tkinter events.
</br></br>


##Static functions

<a class="member_func">set_focus</a><a>(event=None)</a>  
The tkinter text widget doesn't loose focus if another widget is clicked this function emulates this behaviour.  
**Parameters**  
1. event	

