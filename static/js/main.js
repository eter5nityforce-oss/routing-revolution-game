let network = null;
let nodes = new vis.DataSet([]);
let edges = new vis.DataSet([]);

function initNetwork() {
    const container = document.getElementById('network');
    const data = { nodes: nodes, edges: edges };
    const options = {
        nodes: {
            shape: 'dot',
            size: 20,
            font: { size: 14 }
        },
        edges: {
            arrows: 'to',
            width: 2
        },
        physics: {
            enabled: true,
            stabilization: false
        }
    };
    network = new vis.Network(container, data, options);
}

async function fetchState() {
    try {
        const response = await fetch('/api/state');
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error('Error fetching state:', error);
    }
}

function updateUI(data) {
    // Update Stats
    const s = data.status;
    const latency = s.avg_latency !== undefined ? s.avg_latency.toFixed(3) : "0.000";
    document.getElementById('game-stats').innerText = `Money: $${s.money} | Time: ${s.time.toFixed(1)}s | State: ${s.state} | Latency: ${latency}s`;
    document.getElementById('stat-delivered').innerText = s.delivered;
    document.getElementById('stat-dropped').innerText = s.dropped;

    // Update Topology
    // Sync nodes
    const currentNodes = new Set(nodes.getIds());
    const newNodes = new Set();

    data.topology.nodes.forEach(n => {
        newNodes.add(n.id);
        if (!currentNodes.has(n.id)) {
            let color = '#97C2FC'; // Router
            if (n.type === 'ENDPOINT') color = '#FFFF00';
            if (n.type === 'SERVER') color = '#FB7E81';

            nodes.add({ id: n.id, label: n.id, color: color, title: `Type: ${n.type}\nCap: ${n.capacity}` });
        }
    });
    // Remove deleted nodes (optional, assuming we don't delete for now)

    // Sync edges
    const currentEdges = new Set(edges.getIds());
    data.topology.links.forEach(l => {
        const id = `${l.source}-${l.target}`;
        if (!currentEdges.has(id)) {
            edges.add({ id: id, from: l.source, to: l.target, label: `${l.bandwidth/1000000} Mbps` });
        }
    });

    if (currentNodes.size === 0 && newNodes.size > 0) {
        network.fit();
    }
}

async function controlGame(action) {
    await fetch('/api/control', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action: action })
    });
}

async function addNode() {
    const id = document.getElementById('node-id').value;
    const type = document.getElementById('node-type').value;
    if (!id) return;

    await fetch('/api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'add_node', id: id, node_type: type })
    });
    document.getElementById('node-id').value = '';
}

async function addLink() {
    const src = document.getElementById('link-src').value;
    const dst = document.getElementById('link-dst').value;
    if (!src || !dst) return;

    await fetch('/api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'add_link', src: src, dst: dst })
    });
    document.getElementById('link-src').value = '';
    document.getElementById('link-dst').value = '';
}

async function generateTraffic() {
    const src = document.getElementById('traffic-src').value;
    const dst = document.getElementById('traffic-dst').value;
    if (!src || !dst) return;

    await fetch('/api/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ type: 'generate_traffic', src: src, dst: dst, count: 20 })
    });
}

// Init
initNetwork();
setInterval(fetchState, 1000);
fetchState();
