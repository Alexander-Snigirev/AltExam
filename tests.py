import unittest
from algorithm.edmonds_algorithm import LiuEdmondsAlgorithm


class TestLiuEdmondsAlgorithm(unittest.TestCase):
    def test_simple_graph_no_cycle(self):
        """Тест: Простой граф без циклов, 3 вершины, корень 1."""
        Vertexes = {1, 2, 3}
        edges_set = {(1, 2), (1, 3), (2, 3)}
        edges_dict = {(1, 2): 10, (1, 3): 20, (2, 3): 30}
        root = 1
        n = 3
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = {(1, 2), (1, 3)}
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)

    def test_graph_with_cycle(self):
        """Тест: Граф с циклом (2->3, 3->2), 4 вершины, корень 1."""
        Vertexes = {1, 2, 3, 4}
        edges_set = {(1, 2), (2, 3), (3, 2), (3, 4), (4, 1)}
        edges_dict = {(1, 2): 10, (2, 3): 20, (3, 2): 30, (3, 4): 40, (4, 1): 50}
        root = 1
        n = 4
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = {(1, 2), (2, 3), (3, 4)}
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)

    def test_single_vertex(self):
        """Тест: Граф с одной вершиной, без рёбер."""
        Vertexes = {1}
        edges_set = set()
        edges_dict = {}
        root = 1
        n = 1
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = set()
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)

    def test_two_vertices_one_edge(self):
        """Тест: Граф с двумя вершинами и одним ребром."""
        Vertexes = {1, 2}
        edges_set = {(1, 2)}
        edges_dict = {(1, 2): 10}
        root = 1
        n = 2
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = {(1, 2)}
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)


    def test_multiple_edges_to_vertex(self):
        """Тест: Граф с несколькими входящими рёбрами в одну вершину, корень 1."""
        Vertexes = {1, 2, 3}
        edges_set = {(1, 2), (3, 2), (2, 3)}
        edges_dict = {(1, 2): 10, (3, 2): 20, (2, 3): 30}
        root = 1
        n = 3
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = {(1, 2), (2, 3)}
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)

    def test_complete_graph(self):
        """Тест: Полный граф с 3 вершинами, корень 1."""
        Vertexes = {1, 2, 3}
        edges_set = {(1, 2), (1, 3), (2, 1), (2, 3), (3, 1), (3, 2)}
        edges_dict = {(1, 2): 10, (1, 3): 20, (2, 1): 30, (2, 3): 40, (3, 1): 50, (3, 2): 60}
        root = 1
        n = 3
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = {(1, 2), (1, 3)}
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)

    def test_different_root(self):
        """Тест: Граф с циклом, корень 2 (не 1)."""
        Vertexes = {1, 2, 3, 4}
        edges_set = {(1, 2), (2, 3), (3, 2), (3, 4), (4, 1)}
        edges_dict = {(1, 2): 10, (2, 3): 20, (3, 2): 30, (3, 4): 40, (4, 1): 50}
        root = 2
        n = 4
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = {(4, 1), (2, 3), (3, 4)}
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)


    def test_large_graph(self):
        """Тест: Большой граф с 5 вершинами и циклом."""
        Vertexes = {1, 2, 3, 4, 5}
        edges_set = {(1, 2), (2, 3), (3, 2), (3, 4), (4, 5), (5, 1), (2, 5)}
        edges_dict = {(1, 2): 10, (2, 3): 20, (3, 2): 30, (3, 4): 40, (4, 5): 50, (5, 1): 60, (2, 5): 70}
        root = 1
        n = 5
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = {(1, 2), (2, 3), (3, 4), (4, 5)}
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)
        
    def test_large_graph_with_cycles(self):
        """Тест: Граф с 5 вершинами, 16 рёбрами, циклами, корень 0."""
        Vertexes = {0, 1, 2, 3, 4}
        edges_set = {(0, 1), (0, 4), (0, 2), (0, 3), (1, 2), (1, 3), (1, 4), 
                     (2, 1), (2, 3), (2, 4), (3, 1), (3, 2), (3, 4), (4, 1), (4, 2), (4, 3)}
        edges_dict = {(0, 1): 20, (0, 4): 10, (0, 2): 15, (0, 3): 4, (1, 2): 28, (1, 3): 3, 
                      (1, 4): 12, (2, 1): 5, (2, 3): 8, (2, 4): 6, (3, 1): 2, (3, 2): 4, 
                      (3, 4): 20, (4, 1): 5, (4, 2): 7, (4, 3): 30}
        root = 0
        n = 5
        result = LiuEdmondsAlgorithm(Vertexes, edges_set, root, edges_dict, n)
        expected = {(0, 3), (3, 1), (3, 2), (2, 4)}
        self.assertEqual(set(result), expected)
        self.assertEqual(len(result), n - 1)        
        

if __name__ == "__main__":
    unittest.main()


