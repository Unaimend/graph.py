# pylint: skip-file
import math
import tkinter as tk
import unittest

from algorithms.layouting.eades import Eades
from utils import distance, unit_vector
from graph import GraphNode


class EadesTest(unittest.TestCase):

    def test_distance(self):
        node1 = GraphNode(canvas=None, x=0, y=0, id=1, draw_ids=False)
        node2 = GraphNode(canvas=None, x=0, y=200, id=2, draw_ids=False)
        self.assertEqual(distance(node1=node1, node2=node2), 200)

        node1 = GraphNode(canvas=None, x=0, y=0, id=1, draw_ids=False)
        node2 = GraphNode(canvas=None, x=200, y=0, id=2, draw_ids=False)
        self.assertEqual(distance(node1=node1, node2=node2), 200)

        node1 = GraphNode(canvas=None, x=0, y=0, id=1, draw_ids=False)
        node2 = GraphNode(canvas=None, x=100, y=100, id=2, draw_ids=False)
        self.assertTrue(math.isclose(distance(node1=node1, node2=node2), 141.4, abs_tol=0.1))

    def test_unit_vector(self):
        node1 = GraphNode(canvas=None, x=0, y=0, id=1, draw_ids=False)
        node2 = GraphNode(canvas=None, x=0, y=200, id=2, draw_ids=False)
        unit = unit_vector(node1, node2)
        # distance = 0-0 = 0, node1.x - node2.x = 0-0 = 0
        self.assertEqual(unit.x, 0)
        self.assertEqual(unit.y, -1)


if __name__ == '__main__':
    unittest.main()
