import networkx as nx
from .models import Node, Link

class Network:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.nodes = {}
        self.links = {}
        self.routing_algorithm = "shortest_path" # default
        self.static_routes = {} # (node, dst) -> next_hop

    def add_node(self, node_id, node_type="ROUTER", capacity=1000000):
        if node_id not in self.nodes:
            node = Node(node_id, node_type, capacity)
            self.nodes[node_id] = node
            self.graph.add_node(node_id, obj=node)
            return node
        else:
            # Update existing node
            node = self.nodes[node_id]
            node.capacity = capacity
            node.node_type = node_type
            return node

    def add_link(self, src, dst, bandwidth=10000000, latency=0.01, cost=10):
        link_id = (src, dst)
        if link_id not in self.links:
            link = Link(src, dst, bandwidth, latency, cost)
            self.links[link_id] = link
            self.graph.add_edge(src, dst, obj=link, weight=cost)
            return link
        else:
            # Update existing link
            link = self.links[link_id]
            link.bandwidth = bandwidth
            link.latency = latency
            link.cost = cost
            # Update graph weight if edge exists
            if self.graph.has_edge(src, dst):
                self.graph[src][dst]['weight'] = cost
            return link

    def set_routing_algorithm(self, algo):
        self.routing_algorithm = algo

    def add_static_route(self, node, dst, next_hop):
        self.static_routes[(node, dst)] = next_hop

    def get_shortest_path(self, src, dst):
        try:
            return nx.shortest_path(self.graph, src, dst, weight='weight')
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def get_topology_data(self):
        """Returns JSON-serializable topology data."""
        nodes_data = [
            {"id": n.node_id, "type": n.node_type, "capacity": n.capacity, "active": n.is_active}
            for n in self.nodes.values()
        ]
        links_data = [
            {
                "source": l.src,
                "target": l.dst,
                "bandwidth": l.bandwidth,
                "latency": l.latency,
                "active": l.is_active
            }
            for l in self.links.values()
        ]
        return {"nodes": nodes_data, "links": links_data}
