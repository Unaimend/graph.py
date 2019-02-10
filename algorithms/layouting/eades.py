""" Module which implements the layouting-algorithm from EAD[84]
"""
import math
from vector import Vector
from utils import distance as util_distance, unit_vector
from algorithms.layouting.layout_algorithm import LayoutAlgorithm
import tkinter as tk

class Eades(LayoutAlgorithm):
    """ Class which implements the layouting-algorithm from EAD[84]
    """
    def __init__(self, graph_visuals, gui_area):
        LayoutAlgorithm.__init__(self, "Eades", graph_visuals, gui_area)

        # Graph konv. langsamer gegen gleichgewicht besonderns bei hoher Anzahl an Iterationen
        self.constant_1 = 2
        # Beeinflust min. distance
        self.constant_2 = 200
        self.constant_3 = 300
        # Beeinflusstt die konv. Gesch.
        self.constant_4 = 0.1
    
    def init_widgets(self):
        frame = self.algorithm_gui_area
        frame.pack()

        redbutton = tk.Button(frame, text="Red", fg="red")
        redbutton.pack(side=tk.LEFT)

        greenbutton = tk.Button(frame, text="Brown", fg="brown")
        greenbutton.pack(side=tk.LEFT)

        bluebutton = tk.Button(frame, text="Blue", fg="blue")
        bluebutton.pack(side=tk.LEFT)

        blackbutton = tk.Button(frame, text="Black", fg="black")
        blackbutton.pack(side=tk.BOTTOM)

    def calculate_attractive_force_for_all_nodes_and_move_accordingly_new(self, event=None):
        """
        :param event: Only there because the tkinter bind functions expects the function to have one parameter
        :return Nothing
        """
        # pylint: disable= W0613
        # TODO Exception falls self.graph == None
        for node in self.graph_visuals.graph_nodes:
            displacement = Vector(0, 0)
            for nodes in self.graph_visuals.node_adjacency_list[node.id]:
                # If if would calc. the distance between two node which have the same id,
                # the distance would be 0 and log(0) is undefined
                if node.id != nodes.id:
                    distance = util_distance(node, nodes)
                    attractive_force = self.constant_1 * math.log(distance / self.constant_2)
                    direction = unit_vector(nodes, node)
                    displacement.x += direction.x * attractive_force * self.constant_4
                    displacement.y += direction.y * attractive_force * self.constant_4
            node.move(displacement.x, displacement.y)

    def calculate_repelling_force_for_all_nodes_and_move_accordingly_new(self, event=None):
        """
        :param event: Only there because the tkinter bind functions expects the function to have one parameter
        """
        # pylint: disable= W0613
        for node in self.graph_visuals.graph_nodes:
            displacement = Vector(0, 0)
            for nodes in self.graph_visuals.graph_nodes:
                # If if would calc. the distance between two node which have the same id,
                # the distance would be 0  and that would mean that I would divide by 0 in the
                # attractive_force calculation
                if node.id != nodes.id:
                    distance = util_distance(node, nodes)
                    repelling_force = (self.constant_3 / (distance ** 2))
                    direction = unit_vector(node, nodes)
                    displacement.x += direction.x * repelling_force * self.constant_4
                    displacement.y += direction.y * repelling_force * self.constant_4
            node.move(displacement.x, displacement.y)




    # def del_eades_constant_widgets(self):
    #     """
    #     FUNctions which handles the deletetion of the eades labels and text boxes
    #     :return: 
    #     """
    #     # Wenn self.eades_options_frame exisitiert, exisitieren die anderen Variablen auch
    #     # und es is sicher .destroy zu callen
    #     if self.eades_options_frame is not None:
    #         self.eades_options_frame.destroy()
    #         self.tb_1.destroy()
    #         self.tb_2.destroy()
    #         self.tb_3.destroy()
    #         self.tb_4.destroy()
    #         self.label_1.destroy()
    #         self.label_2.destroy()
    #         self.label_3.destroy()
    #         self.label_4.destroy()
    # 
    # def init_eades_constant_widgets(self):
    #     """Initializes all the eades constant"""
    #     # Frame der die Label und TextInputs h�lt
    #     self.eades_options_frame = tk.Frame(self.root)
    #     # Position des Frames in der GUI setzen
    #     self.eades_options_frame.grid(column=1, row=3)
    # 
    #     self.label_1 = tk.Label(self.eades_options_frame, text="c1")
    #     self.label_1.pack(side=tk.LEFT)
    #     # Textfield for c1 Eades constant
    #     self.tb_1 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
    #     self.tb_1.pack(side=tk.LEFT)
    #     self.tb_1.insert(tk.END, self.current_algo.constant_1)
    #     self.label_2 = tk.Label(self.eades_options_frame, text="c2")
    #     self.label_2.pack(side=tk.LEFT)
    #     # Textfield for c2 Eades constant
    #     self.tb_2 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
    #     self.tb_2.pack(side=tk.LEFT)
    #     self.tb_2.insert(tk.END, self.current_algo.constant_2)
    #     self.label_3 = tk.Label(self.eades_options_frame, text="c3")
    #     self.label_3.pack(side=tk.LEFT)
    #     # Textfield for c3 Eades constant
    #     self.tb_3 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2)
    #     self.tb_3.pack(side=tk.LEFT)
    #     self.tb_3.insert(tk.END, self.current_algo.constant_3)
    #     self.label_4 = tk.Label(self.eades_options_frame, text="c4")
    #     self.label_4.pack(side=tk.LEFT)
    #     # Textfield for c4 Eades constant
    #     self.tb_4 = tk.Text(self.eades_options_frame, height=1, width=5, relief="sunken", borderwidth=2, takefocus=0)
    #     self.tb_4.pack(side=tk.LEFT)
    #     self.tb_4.insert(tk.END, self.current_algo.constant_4)
