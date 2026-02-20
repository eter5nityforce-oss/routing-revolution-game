def scenario_basic(gm):
    gm.network.add_node("ClientA", "ENDPOINT")
    gm.network.add_node("Router1", "ROUTER")
    gm.network.add_node("Server1", "SERVER")

    gm.network.add_link("ClientA", "Router1", bandwidth=10000000, latency=0.01)
    gm.network.add_link("Router1", "Server1", bandwidth=10000000, latency=0.01)

    # Background traffic
    gm.engine.env.process(gm.engine.generate_traffic("ClientA", "Server1", rate=5, count=1000))

def scenario_redundancy(gm):
    gm.network.add_node("Start", "ENDPOINT")
    gm.network.add_node("R1", "ROUTER")
    gm.network.add_node("R2", "ROUTER")
    gm.network.add_node("End", "ENDPOINT")

    # Path 1
    gm.network.add_link("Start", "R1", cost=10)
    gm.network.add_link("R1", "End", cost=10)

    # Path 2 (Backup, higher cost initially or just parallel)
    gm.network.add_link("Start", "R2", cost=20)
    gm.network.add_link("R2", "End", cost=20)

    gm.engine.env.process(gm.engine.generate_traffic("Start", "End", rate=5, count=1000))

SCENARIOS = {
    "basic": scenario_basic,
    "redundancy": scenario_redundancy
}
