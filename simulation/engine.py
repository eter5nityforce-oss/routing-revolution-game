import simpy
import random
from .models import Packet

class SimulationEngine:
    def __init__(self, network):
        self.env = simpy.Environment()
        self.network = network
        self.packet_sink = []  # List of delivered packets
        self.packets_dropped = 0
        self.active_processes = {}

    def start(self):
        # Initialize processes for all existing nodes and links
        for node_id in self.network.nodes:
            node = self.network.nodes[node_id]
            # Initialize SimPy Store if not present
            if node.queue is None:
                node.queue = simpy.Store(self.env)

            if node_id not in self.active_processes:
                self.active_processes[node_id] = self.env.process(self.node_process(node_id))

        # Start traffic generation (placeholder logic for now)
        pass

    def node_process(self, node_id):
        """Process packets at a node."""
        node = self.network.nodes[node_id]
        while True:
            # Wait for packet
            packet = yield node.queue.get()

            # Processing time based on packet size and node capacity
            # size (bits) / capacity (bits/s) = seconds
            processing_time = packet.size / node.capacity
            yield self.env.timeout(processing_time)

            # Routing decision
            next_hop = self.route_packet(packet, node_id)

            if next_hop:
                if next_hop == "DESTINATION_REACHED":
                    packet.path_history.append(node_id)
                    self.packet_sink.append(packet)
                else:
                    # Forward to next hop via link
                    self.env.process(self.link_process(node_id, next_hop, packet))
            else:
                self.packets_dropped += 1

    def link_process(self, src, dst, packet):
        """Transmit packet over a link."""
        link_id = (src, dst)
        if link_id in self.network.links:
            link = self.network.links[link_id]
            if link.is_active:
                # Transmission delay: size / bandwidth
                trans_delay = packet.size / link.bandwidth
                # Propagation latency
                latency = link.latency

                yield self.env.timeout(trans_delay + latency)

                # Arrive at next node
                packet.path_history.append(src)
                if dst in self.network.nodes:
                    node = self.network.nodes[dst]
                    if node.queue:
                        yield node.queue.put(packet)
                    else:
                        self.packets_dropped += 1 # Node not ready?
            else:
                 self.packets_dropped += 1 # Link down
        else:
             self.packets_dropped += 1 # Link does not exist

    def set_link_status(self, src, dst, active=True):
        link_id = (src, dst)
        if link_id in self.network.links:
            self.network.links[link_id].is_active = active

    def route_packet(self, packet, current_node):
        """Determine next hop."""
        if current_node == packet.dst:
            return "DESTINATION_REACHED"

        algo = self.network.routing_algorithm

        if algo == "static":
            # Check static routes: (current_node, dst_node) -> next_hop
            key = (current_node, packet.dst)
            if key in self.network.static_routes:
                return self.network.static_routes[key]
            return None

        elif algo == "shortest_path":
            path = self.network.get_shortest_path(current_node, packet.dst)
            if path and len(path) > 1:
                return path[1] # Next node in path

        return None

    def generate_traffic(self, src, dst, rate=1.0, count=10):
        """Generate packets from src to dst."""
        for _ in range(count):
            packet = Packet(src, dst, created_at=self.env.now)
            if src in self.network.nodes:
                node = self.network.nodes[src]
                if node.queue:
                    yield node.queue.put(packet)
            yield self.env.timeout(1.0 / rate)

    def run(self, duration=10):
        self.env.run(until=duration)
