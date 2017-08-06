import Eades
import unittest
import Graph
import tkinter as tk
import math


class EadesTest(unittest.TestCase):

    def test_distance(self):
        node1 = Graph.GraphNode(canvas=tk.Canvas(), x=0,y=0, id=1, drawIds=False, text="")
        node2 = Graph.GraphNode(canvas=tk.Canvas(), x=0,y=200, id=2, drawIds=False, text="")
        self.assertEqual(Eades.Eades.distance(node1=node1, node2=node2), 200)

        node1 = Graph.GraphNode(canvas=tk.Canvas(), x=0, y=0, id=1, drawIds=False, text="")
        node2 = Graph.GraphNode(canvas=tk.Canvas(), x=200, y=0, id=2, drawIds=False, text="")
        self.assertEqual(Eades.Eades.distance(node1=node1, node2=node2), 200)

        node1 = Graph.GraphNode(canvas=tk.Canvas(), x=0, y=0, id=1, drawIds=False, text="")
        node2 = Graph.GraphNode(canvas=tk.Canvas(), x=100, y=100, id=2, drawIds=False, text="")
        self.assertTrue(math.isclose(Eades.Eades.distance(node1=node1, node2=node2), 141.421, abs_tol=0.001))
        # TODO 3 oder 4 weitere unit test schreiben damit alles funktioniert

    def test_unit_vector(self):
        node1 = Graph.GraphNode(canvas=tk.Canvas(), x=0, y=0, id=1, drawIds=False, text="")
        node2 = Graph.GraphNode(canvas=tk.Canvas(), x=0, y=200, id=2, drawIds=False, text="")
        unit = Eades.Eades.unit_vector(node1, node2)
        # distance = 0-0 = 0, node1.x - node2.x = 0-0 = 0
        self.assertEqual(unit.x, 0)
        self.assertEqual(unit.y, -1)

        # TODO 5 oder 6 weitere unit tests schreiben

if __name__ == '__main__':
    unittest.main()
