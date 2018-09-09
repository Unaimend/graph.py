# pylint: skip-file
import unittest
from graph import Graph


class GraphTest(unittest.TestCase):
    # def __init__(self):
    #     self.graph = Graph("./graphs/simple_bin_tree.json")

    def setUp(self):
        self.graph = Graph("./graphs/simple_bin_tree.json")

    def test_fileloading(self):
        with self.assertRaises(FileNotFoundError):
            self.graph = Graph(".simple_bin_tree.json")

    def test_adjacecency_list(self):
        self.assertEqual(self.graph.adjacency_list, [[1, 2], [0], [0]])

    def test_vertice_counter(self):
        self.assertEqual(self.graph.vertice_count, 3)

    def test_parent(self):
        self.assertEqual(self.graph.parent(1), 0)
        self.assertEqual(self.graph.parent(2), 0)

    # def test_subtree(self):
    #     self.graph = Graph("./graphs/simple_bin_tree.json")
    #     self.assertEqual(self.graph.subtree_index(0), [1, 2])



if __name__ == '__main__':
    unittest.main()
