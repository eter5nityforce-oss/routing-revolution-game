# Routing Revolution Game (라우팅 혁명 게임)

An expert-level, real-time discrete-event network simulation game. Manage a complex network, ensure SLA compliance, and survive cyber-attacks!

## Features
- **Simulation Engine:** Built on `SimPy` for accurate discrete-event simulation (packets, queues, latency).
- **Real-Time Gameplay:** The simulation runs in real-time, controlled via a web interface.
- **Dynamic Scenarios:** Handle traffic bursts, link failures, and routing challenges.
- **Interactive UI:** Visualize network topology and packet flow using Vis.js.
- **Restful API:** Python Flask backend exposing state and control endpoints.

## Prerequisites
- Python 3.8+
- `pip`

## Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Demo: How to Play

### 1. Start the Server
Run the Flask application:
```bash
python3 app.py
```
The server will start on `http://localhost:5000`.

### 2. Access the Game
Open your web browser and navigate to `http://localhost:5000`.

### 3. Gameplay Controls
- **Dashboard:**
  - **Top Bar:** View Money, Time, and Game State.
  - **Sidebar:**
    - **Controls:** Pause/Resume/Reset the simulation.
    - **Add Node:** Create new Routers, Endpoints, or Servers.
    - **Add Link:** Connect nodes with links (default 10Mbps).
    - **Traffic:** Manually trigger packet bursts between nodes.
    - **Metrics:** Monitor delivered vs. dropped packets.
  - **Main Area:** Interactive Network Graph.
    - **Blue Nodes:** Routers
    - **Yellow Nodes:** Endpoints
    - **Red Nodes:** Servers
    - **Arrows:** Links (hover for bandwidth)

### 4. Scenarios
By default, the game loads the `basic` scenario:
- **ClientA** sends traffic to **Server1** via **Router1**.
- Watch the "Delivered" count increase.

**Challenge:**
1. Add a new node `Router2`.
2. Add links `ClientA -> Router2` and `Router2 -> Server1`.
3. If `Router1` fails (simulated by high traffic or manual disruption), traffic needs to be rerouted!

## API Reference

- `GET /api/state`: Get current simulation state (nodes, links, stats).
- `POST /api/control`: `{"action": "pause" | "resume" | "reset"}`
- `POST /api/action`: Perform game actions.
  - Add Node: `{"type": "add_node", "id": "ID", "node_type": "ROUTER"}`
  - Add Link: `{"type": "add_link", "src": "A", "dst": "B"}`
  - Generate Traffic: `{"type": "generate_traffic", "src": "A", "dst": "B", "count": 10}`

## Architecture
- **simulation/**: Core DES engine (`engine.py`, `models.py`).
- **game/**: Game logic and state management (`manager.py`, `scenarios.py`).
- **app.py**: Flask REST API.
- **static/js/main.js**: Frontend logic using Fetch API and Vis.js.

## License
MIT
