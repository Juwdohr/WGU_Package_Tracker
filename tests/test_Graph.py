import unittest
from Graph import Directed, Undirected, Vertex
from Graph.graph import Graph


def link_vertices(vertex_a, vertex_b, weight):
    vertex_a.previous_vertex = vertex_b
    vertex_a.distance = weight


class test_Vertex(unittest.TestCase):

    def setUp(self) -> None:
        self.vertex_numb = Vertex("1")
        self.vertex_address = Vertex('1060 Dalton Ave S')

    def test_Vertex_creation(self) -> None:
        self.assertEqual(self.vertex_numb.label, '1')
        self.assertEqual(self.vertex_numb.previous_vertex, None)
        self.assertEqual(self.vertex_numb.distance, float('inf'))

        self.assertEqual(self.vertex_address.label, '1060 Dalton Ave S')
        self.assertEqual(self.vertex_address.previous_vertex, None)
        self.assertEqual(self.vertex_address.distance, float('inf'))

    def test_linking(self) -> None:
        link_vertices(self.vertex_numb, self.vertex_address, 1.0)
        self.assertIsInstance(self.vertex_numb.previous_vertex, Vertex)
        self.assertEqual(self.vertex_numb.previous_vertex, self.vertex_address)
        self.assertEqual(self.vertex_numb.distance, 1.0)

        link_vertices(self.vertex_address, self.vertex_numb, 10.0)
        self.assertIsInstance(self.vertex_address.previous_vertex, Vertex)
        self.assertEqual(self.vertex_address.previous_vertex, self.vertex_numb)
        self.assertEqual(self.vertex_address.distance, 10.0)

        self.assertNotEqual(self.vertex_numb.distance, self.vertex_address.distance)

    def test_reset(self) -> None:
        link_vertices(self.vertex_numb, self.vertex_address, 1.0)
        link_vertices(self.vertex_address, self.vertex_numb, 10.0)

        self.vertex_numb.reset()
        self.assertEqual(self.vertex_numb.previous_vertex, None)
        self.assertEqual(self.vertex_numb.distance, float('inf'))
        self.assertEqual(self.vertex_address.previous_vertex, self.vertex_numb)
        self.assertEqual(self.vertex_address.distance, 10.0)

        self.vertex_address.reset()
        self.assertEqual(self.vertex_address.previous_vertex, None)
        self.assertEqual(self.vertex_address.distance, float('inf'))


class test_DirectedGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.directed_graph = Directed()
        self.vertex_numb = Vertex("1")
        self.vertex_address = Vertex('1060 Dalton Ave S')

    def test_DirectedGraph_Creation(self) -> None:
        self.assertIsInstance(self.directed_graph, Graph)
        self.assertEqual(self.directed_graph.edge_weights, {})

    def test_add_vertex(self) -> None:
        self.directed_graph.add_vertex(self.vertex_numb)
        self.directed_graph.add_vertex(self.vertex_address)
        self.assertEqual(len(self.directed_graph.adjacency_list), 2)
        self.assertEqual(self.directed_graph.edge_weights, {})

    def test_add_directed_edge(self) -> None:
        self.directed_graph.add_vertex(self.vertex_numb)
        self.directed_graph.add_vertex(self.vertex_address)

        self.directed_graph.add_directed_edge(self.vertex_numb, self.vertex_address, 5.0)
        self.assertEqual(len(self.directed_graph.adjacency_list), 2)
        self.assertEqual(len(self.directed_graph.edge_weights), 1)
        self.assertEqual(self.directed_graph.edge_weights[self.vertex_numb, self.vertex_address], 5.0)

        self.directed_graph.add_directed_edge(self.vertex_address, self.vertex_numb, 100.0)
        self.assertEqual(len(self.directed_graph.adjacency_list), 2)
        self.assertEqual(len(self.directed_graph.edge_weights), 2)
        self.assertEqual(self.directed_graph.edge_weights[self.vertex_address, self.vertex_numb], 100.0)

    def test_find_vertex(self) -> None:
        self.directed_graph.add_vertex(self.vertex_numb)
        self.directed_graph.add_vertex(self.vertex_address)

        self.assertNotEqual(self.directed_graph.find_vertex("1"), "1")
        self.assertNotEqual(self.directed_graph.find_vertex("1060 Dalton Ave S"), '1060 Dalton Ave S')

        self.assertIsInstance(self.directed_graph.find_vertex("1"), Vertex)
        self.assertIsInstance(self.directed_graph.find_vertex("1060 Dalton Ave S"), Vertex)


class test_UndirectedGraph(unittest.TestCase):
    def setUp(self) -> None:
        self.undirected_graph = Undirected()
        self.vertex_numb = Vertex("1")
        self.vertex_address = Vertex('1060 Dalton Ave S')

    def test_UndirectedGraph_creation(self) -> None:
        self.assertIsInstance(self.undirected_graph, Graph)
        self.assertEqual(self.undirected_graph.edge_weights, {})

    def test_add_vertex(self) -> None:
        self.undirected_graph.add_vertex(self.vertex_numb)
        self.undirected_graph.add_vertex(self.vertex_address)
        self.assertEqual(len(self.undirected_graph.adjacency_list), 2)
        self.assertEqual(self.undirected_graph.edge_weights, {})

    def test_add_undirected_edge(self) -> None:
        self.undirected_graph.add_vertex(self.vertex_numb)
        self.undirected_graph.add_vertex(self.vertex_address)

        self.undirected_graph.add_undirected_edge(self.vertex_numb, self.vertex_address, 5.0)
        self.assertEqual(len(self.undirected_graph.adjacency_list), 2)
        self.assertNotEqual(len(self.undirected_graph.edge_weights), 1)
        self.assertEqual(self.undirected_graph.edge_weights[self.vertex_numb, self.vertex_address], 5.0)

        self.undirected_graph.add_undirected_edge(self.vertex_address, self.vertex_numb, 100.0)
        self.assertEqual(len(self.undirected_graph.adjacency_list), 2)
        self.assertEqual(len(self.undirected_graph.edge_weights), 2)
        self.assertEqual(self.undirected_graph.edge_weights[self.vertex_address, self.vertex_numb], 100.0)

    def test_find_vertex(self) -> None:
        self.undirected_graph.add_vertex(self.vertex_numb)
        self.undirected_graph.add_vertex(self.vertex_address)

        self.assertNotEqual(self.undirected_graph.find_vertex("1"), "1")
        self.assertNotEqual(self.undirected_graph.find_vertex("1060 Dalton Ave S"), '1060 Dalton Ave S')

        self.assertIsInstance(self.undirected_graph.find_vertex("1"), Vertex)
        self.assertIsInstance(self.undirected_graph.find_vertex("1060 Dalton Ave S"), Vertex)


if __name__ == '__main__':
    unittest.main()
