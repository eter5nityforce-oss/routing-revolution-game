from simulation.network import Network
from simulation.engine import SimulationEngine
from game.scenarios import SCENARIOS
import time
import threading

class GameManager:
    def __init__(self, scenario_name="basic"):
        self.lock = threading.RLock()
        self.network = Network()
        self.engine = SimulationEngine(self.network)
        if scenario_name and scenario_name in SCENARIOS:
             SCENARIOS[scenario_name](self)
        self.money = 1000
        self.score = 0
        self.game_state = "RUNNING" # RUNNING, PAUSED, GAME_OVER, VICTORY
        self.current_time = 0

        # Stats
        self.total_packets_delivered = 0
        self.total_packets_lost = 0
        self.total_latency = 0
        self.avg_latency = 0.0

        # SLA Constraints
        self.sla_max_latency = 0.5 # seconds
        self.sla_max_loss_rate = 0.05 # 5%

        self.engine.start()

    def update(self, delta_time=1.0):
        with self.lock:
            if self.game_state != "RUNNING":
                return

            # Ensure all nodes are running
            self.engine.start()

            # Advance simulation
            target_time = self.current_time + delta_time
            self.engine.run(duration=target_time)
            self.current_time = target_time

            # Collect stats from engine
            new_packets = self.engine.packet_sink[self.total_packets_delivered:]
            if new_packets:
                # Latency = Current Sim Time - Packet Creation Time
                batch_latency = sum((self.engine.env.now - p.created_at) for p in new_packets)
                self.total_latency += batch_latency

            self.total_packets_delivered = len(self.engine.packet_sink)
            self.total_packets_lost = self.engine.packets_dropped

            if self.total_packets_delivered > 0:
                self.avg_latency = self.total_latency / self.total_packets_delivered

            # Check Win/Lose
            loss_rate = 0
            total_traffic = self.total_packets_delivered + self.total_packets_lost
            if total_traffic > 0:
                loss_rate = self.total_packets_lost / total_traffic

            if loss_rate > self.sla_max_loss_rate and self.current_time > 5: # Grace period
                self.game_state = "GAME_OVER"
                # print(f"Game Over: Loss Rate {loss_rate:.2f} > {self.sla_max_loss_rate}")

    def get_status(self):
        with self.lock:
            return {
                "money": self.money,
                "score": self.score,
                "state": self.game_state,
                "time": self.current_time,
                "delivered": self.total_packets_delivered,
                "dropped": self.total_packets_lost,
                "avg_latency": self.avg_latency
            }
