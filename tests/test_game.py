import unittest
from game.manager import GameManager

class TestGame(unittest.TestCase):
    def test_manager_update(self):
        gm = GameManager(scenario_name=None)
        # Add simple network
        gm.network.add_node("A", "ENDPOINT")
        gm.network.add_node("B", "ENDPOINT")
        gm.network.add_link("A", "B")

        # Add traffic manually for test (since generate_traffic isn't auto-called yet)
        gm.engine.env.process(gm.engine.generate_traffic("A", "B", count=5))

        # Update game
        gm.update(delta_time=10)

        status = gm.get_status()
        self.assertEqual(status["delivered"], 5)
        self.assertEqual(status["state"], "RUNNING")

    def test_loss_condition(self):
        gm = GameManager(scenario_name=None)
        gm.network.add_node("A", "ENDPOINT")
        gm.network.add_node("B", "ENDPOINT")
        # No link!

        gm.engine.env.process(gm.engine.generate_traffic("A", "B", count=10))

        gm.update(delta_time=10)
        # Should lose because packets dropped
        status = gm.get_status()
        self.assertEqual(status["dropped"], 10)
        self.assertEqual(status["state"], "GAME_OVER")

if __name__ == '__main__':
    unittest.main()
