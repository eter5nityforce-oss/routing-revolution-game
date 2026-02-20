import unittest
from simulation.network import Network
from simulation.engine import SimulationEngine

class TestSimulation(unittest.TestCase):
    def test_simple_delivery(self):
        net = Network()
        net.add_node("A", "ENDPOINT")
        net.add_node("B", "ROUTER")
        net.add_node("C", "ENDPOINT")
        net.add_link("A", "B")
        net.add_link("B", "C")

        sim = SimulationEngine(net)

        # Manually add a traffic generator process
        sim.env.process(sim.generate_traffic("A", "C", count=5))

        # Start node processes
        sim.start()

        # Run
        sim.run(duration=10)

        # Check results
        # 5 packets generated. Path A -> B -> C.
        self.assertEqual(len(sim.packet_sink), 5)
        for p in sim.packet_sink:
            self.assertEqual(p.dst, "C")
            self.assertEqual(p.path_history, ["A", "B", "C"])

if __name__ == '__main__':
    unittest.main()
