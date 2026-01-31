from flask import Flask, jsonify, request, render_template
from game.manager import GameManager
import threading
import time

app = Flask(__name__)
gm = GameManager()

# Background Simulation Loop
def simulation_loop():
    while True:
        if gm.game_state == "RUNNING":
            gm.update(delta_time=1.0)
        time.sleep(1.0) # Real-time 1s = Simulation 1s (approx)

sim_thread = threading.Thread(target=simulation_loop, daemon=True)
sim_thread.start()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/state', methods=['GET'])
def get_state():
    with gm.lock:
        status = gm.get_status()
        topology = gm.network.get_topology_data()
    return jsonify({
        "status": status,
        "topology": topology
    })

@app.route('/api/control', methods=['POST'])
def control_game():
    global gm
    data = request.json
    action = data.get('action')
    with gm.lock:
        if action == 'pause':
            gm.game_state = "PAUSED"
        elif action == 'resume':
            gm.game_state = "RUNNING"
        elif action == 'reset':
            gm = GameManager() # simplistic reset
    return jsonify({"status": "ok", "new_state": gm.game_state})

@app.route('/api/action', methods=['POST'])
def perform_action():
    data = request.json
    action_type = data.get('type')

    try:
        with gm.lock:
            if action_type == 'add_node':
                # {"type": "add_node", "id": "X", "node_type": "ROUTER"}
                node_id = data.get('id')
                node_type = data.get('node_type', 'ROUTER')
                gm.network.add_node(node_id, node_type)

            elif action_type == 'add_link':
                # {"type": "add_link", "src": "A", "dst": "B", "bw": 1000}
                src = data.get('src')
                dst = data.get('dst')
                bw = data.get('bw', 10000000)
                gm.network.add_link(src, dst, bandwidth=bw)

            elif action_type == 'generate_traffic':
                # {"type": "generate_traffic", "src": "A", "dst": "B", "count": 10}
                src = data.get('src')
                dst = data.get('dst')
                count = data.get('count', 10)
                gm.engine.env.process(gm.engine.generate_traffic(src, dst, count=count))

        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
