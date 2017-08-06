from Eades import Eades
import unittest
from graph import GraphNode
import tkinter as tk
import math


class EadesTest(unittest.TestCase):

    def test_distance(self):
        node1 = GraphNode(canvas=tk.Canvas(), x=0,y=0, id=1, drawIds=False, text="")
        node2 = GraphNode(canvas=tk.Canvas(), x=0,y=200, id=2, drawIds=False, text="")
        self.assertEqual(Eades.distance(node1=node1, node2=node2), 200)

        node1 = GraphNode(canvas=tk.Canvas(), x=0, y=0, id=1, drawIds=False, text="")
        node2 = GraphNode(canvas=tk.Canvas(), x=200, y=0, id=2, drawIds=False, text="")
        self.assertEqual(Eades.distance(node1=node1, node2=node2), 200)

        node1 = GraphNode(canvas=tk.Canvas(), x=0, y=0, id=1, drawIds=False, text="")
        node2 = GraphNode(canvas=tk.Canvas(), x=100, y=100, id=2, drawIds=False, text="")
        self.assertTrue(math.isclose(Eades.distance(node1=node1, node2=node2), 141.4, abs_tol=0.1))

    def test_unit_vector(self):
        node1 = GraphNode(canvas=tk.Canvas(), x=0, y=0, id=1, drawIds=False, text="")
        node2 = GraphNode(canvas=tk.Canvas(), x=0, y=200, id=2, drawIds=False, text="")
        unit = Eades.unit_vector(node1, node2)
        # distance = 0-0 = 0, node1.x - node2.x = 0-0 = 0
        self.assertEqual(unit.x, 0)
        self.assertEqual(unit.y, -1)


if __name__ == '__main__':
    unittest.main()
