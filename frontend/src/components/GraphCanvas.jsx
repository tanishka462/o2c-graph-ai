import { useEffect, useRef, useState } from "react";
import { Network } from "vis-network";
import axios from "axios";

const NODE_COLORS = {
  BusinessPartner: { background: "#4A90D9", border: "#2171B5" },
  SalesOrder: { background: "#74C476", border: "#41AB5D" },
  SalesOrderItem: { background: "#A1D99B", border: "#74C476" },
  Delivery: { background: "#FD8D3C", border: "#E6550D" },
  DeliveryItem: { background: "#FDAE6B", border: "#FD8D3C" },
  BillingDocument: { background: "#9E9AC8", border: "#756BB1" },
  JournalEntry: { background: "#F768A1", border: "#DD3497" },
  Payment: { background: "#41B3A3", border: "#2C8C7A" },
  Product: { background: "#FA9FB5", border: "#F768A1" },
  Plant: { background: "#BCBDDC", border: "#9E9AC8" },
};

export default function GraphCanvas({ onNodeSelect }) {
  const containerRef = useRef(null);
  const networkRef = useRef(null);
  const [loading, setLoading] = useState(true);
  const [nodeInfo, setNodeInfo] = useState(null);
  const [stats, setStats] = useState({ nodes: 0, edges: 0 });

  useEffect(() => {
    fetchGraph();
  }, []);

  async function fetchGraph() {
    try {
      const res = await axios.get("https://o2c-graph-ai-1.onrender.com/api/graph");
      const { nodes, edges } = res.data;
      setStats({ nodes: nodes.length, edges: edges.length });
      buildNetwork(nodes, edges);
    } catch (e) {
      console.error("Graph fetch error:", e);
    } finally {
      setLoading(false);
    }
  }

  function buildNetwork(nodes, edges) {
    const visNodes = nodes.map((n) => ({
      id: n.id,
      label: n.label,
      title: `${n.type}: ${n.id}`,
      color: NODE_COLORS[n.type] || { background: "#B0C4DE", border: "#778899" },
      font: { size: 11, color: "#333" },
      shape: "dot",
      size: getNodeSize(n.type),
      type: n.type,
    }));

    const visEdges = edges.map((e, i) => ({
      id: i,
      from: e.from,
      to: e.to,
      label: e.label,
      font: { size: 9, color: "#999", align: "middle" },
      color: { color: "#B0C4DE", opacity: 0.7 },
      arrows: { to: { enabled: true, scaleFactor: 0.5 } },
      smooth: { type: "continuous" },
    }));

    const data = {
      nodes: visNodes,
      edges: visEdges,
    };

    const options = {
      physics: {
        enabled: true,
        barnesHut: {
          gravitationalConstant: -8000,
          centralGravity: 0.3,
          springLength: 120,
          springConstant: 0.04,
          damping: 0.09,
        },
      },
      interaction: {
        hover: true,
        tooltipDelay: 200,
        zoomView: true,
        dragView: true,
      },
      layout: {
        improvedLayout: false,
      },
    };

    if (networkRef.current) {
      networkRef.current.destroy();
    }

    networkRef.current = new Network(containerRef.current, data, options);

    networkRef.current.on("click", async (params) => {
      if (params.nodes.length > 0) {
        const nodeId = params.nodes[0];
        const node = visNodes.find((n) => n.id === nodeId);
        if (node) {
          onNodeSelect(node);
          fetchNodeDetails(nodeId, node.type);
        }
      } else {
        setNodeInfo(null);
        onNodeSelect(null);
      }
    });
  }

  function getNodeSize(type) {
    const sizes = {
      BusinessPartner: 18,
      SalesOrder: 15,
      BillingDocument: 15,
      JournalEntry: 13,
      Payment: 13,
      Delivery: 13,
      Product: 12,
      Plant: 12,
      SalesOrderItem: 10,
      DeliveryItem: 10,
    };
    return sizes[type] || 10;
  }

  async function fetchNodeDetails(nodeId, nodeType) {
    try {
      const res = await axios.get(
        `https://o2c-graph-ai-1.onrender.com/api/node/${nodeType}/${encodeURIComponent(nodeId)}`
      );
      setNodeInfo({ id: nodeId, type: nodeType, ...res.data });
    } catch (e) {
      console.error("Node detail error:", e);
    }
  }

  return (
    <div style={{ flex: 1, position: "relative", background: "#fafafa" }}>
      {loading && (
        <div style={{
          position: "absolute", top: "50%", left: "50%",
          transform: "translate(-50%,-50%)", zIndex: 10,
          background: "white", padding: "20px 30px",
          borderRadius: 8, boxShadow: "0 2px 12px rgba(0,0,0,0.1)",
          fontSize: 14, color: "#555"
        }}>
          Loading graph...
        </div>
      )}

      <div style={{
        position: "absolute", top: 12, left: 12, zIndex: 5,
        display: "flex", gap: 8
      }}>
        <button style={btnStyle} onClick={() => networkRef.current?.fit()}>
          ⤢ Fit
        </button>
        <button style={btnStyle} onClick={() => networkRef.current?.setOptions({ physics: { enabled: true } })}>
          ◎ Reset
        </button>
        <span style={{
          background: "white", padding: "6px 12px",
          borderRadius: 6, fontSize: 12, color: "#666",
          border: "1px solid #e5e5e5"
        }}>
          {stats.nodes} nodes · {stats.edges} edges
        </span>
      </div>

      {/* Legend */}
      <div style={{
        position: "absolute", bottom: 12, left: 12, zIndex: 5,
        background: "white", padding: "10px 14px",
        borderRadius: 8, boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
        fontSize: 11
      }}>
        {Object.entries(NODE_COLORS).slice(0, 6).map(([type, color]) => (
          <div key={type} style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 3 }}>
            <div style={{
              width: 10, height: 10, borderRadius: "50%",
              background: color.background, border: `2px solid ${color.border}`
            }} />
            <span style={{ color: "#555" }}>{type}</span>
          </div>
        ))}
      </div>

      {/* Node Info Panel */}
      {nodeInfo && (
        <div style={{
          position: "absolute", top: 12, right: 12, zIndex: 5,
          background: "white", borderRadius: 8,
          boxShadow: "0 2px 12px rgba(0,0,0,0.1)",
          padding: "16px", width: 280, maxHeight: "70vh",
          overflowY: "auto", fontSize: 12
        }}>
          <div style={{
            fontWeight: 700, fontSize: 14, marginBottom: 10,
            color: "#222", borderBottom: "1px solid #eee", paddingBottom: 8
          }}>
            {nodeInfo.type}
          </div>
          {Object.entries(nodeInfo.details || {}).slice(0, 12).map(([k, v]) => (
            v && (
              <div key={k} style={{ marginBottom: 5 }}>
                <span style={{ color: "#888", fontWeight: 600 }}>{k}: </span>
                <span style={{ color: "#333" }}>{String(v).substring(0, 40)}</span>
              </div>
            )
          ))}
          <div style={{ marginTop: 10, color: "#aaa", fontSize: 11 }}>
            {nodeInfo.connections?.length || 0} connections
          </div>
          <button
            style={{ ...btnStyle, marginTop: 8, width: "100%", justifyContent: "center" }}
            onClick={() => setNodeInfo(null)}
          >
            Close
          </button>
        </div>
      )}

      <div ref={containerRef} style={{ width: "100%", height: "100%" }} />
    </div>
  );
}

const btnStyle = {
  background: "white",
  border: "1px solid #e5e5e5",
  borderRadius: 6,
  padding: "6px 12px",
  fontSize: 12,
  cursor: "pointer",
  color: "#444",
  display: "flex",
  alignItems: "center",
  gap: 4,
};