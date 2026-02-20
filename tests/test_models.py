import unittest
from simulation.models import Packet, Node, Link
from simulation.network import Network

class TestModels(unittest.TestCase):
    def test_packet_creation(self):
        p = Packet("A", "B", 1024, 1)
        self.assertEqual(p.src, "A")
        self.assertEqual(p.dst, "B")
        self.assertEqual(p.size, 1024)

    def test_network_structure(self):
        net = Network()
        net.add_node("A", "ENDPOINT")
        net.add_node("B", "ROUTER")
        net.add_node("C", "ENDPOINT")

        net.add_link("A", "B", cost=5)
        net.add_link("B", "C", cost=5)

        self.assertIn("A", net.nodes)
        self.assertIn(("A", "B"), net.links)

        path = net.get_shortest_path("A", "C")
        self.assertEqual(path, ["A", "B", "C"])

if __name__ == '__main__':
    unittest.main()
