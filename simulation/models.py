import uuid
import time

class Packet:
    def __init__(self, src, dst, size=1024, priority=1, packet_type="DATA", created_at=0):
        self.id = str(uuid.uuid4())[:8]
        self.src = src
        self.dst = dst
        self.size = size  # in bits
        self.priority = priority
        self.packet_type = packet_type
        self.created_at = created_at
        self.path_history = []
        self.hops = 0

    def __repr__(self):
        return f"Packet({self.id}, {self.src}->{self.dst}, pri={self.priority})"

class Node:
    def __init__(self, node_id, node_type="ROUTER", capacity=1000000):
        self.node_id = node_id
        self.node_type = node_type  # ROUTER, ENDPOINT, SERVER
        self.capacity = capacity  # Processing capacity in bits per second
        self.queue = None  # Will be assigned simpy.Store by engine
        self.is_active = True

    def __repr__(self):
        return f"Node({self.node_id}, {self.node_type})"

class Link:
    def __init__(self, src, dst, bandwidth=10000000, latency=0.01, cost=10):
        self.src = src
        self.dst = dst
        self.bandwidth = bandwidth  # bits per second
        self.latency = latency  # seconds
        self.cost = cost
        self.is_active = True
        self.current_load = 0

    def __repr__(self):
        return f"Link({self.src}->{self.dst}, bw={self.bandwidth})"
