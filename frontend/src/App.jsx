import { useState } from "react";
import GraphCanvas from "./components/GraphCanvas";
import ChatPanel from "./components/ChatPanel";
import "./App.css";

function App() {
  const [selectedNode, setSelectedNode] = useState(null);

  return (
    <div className="app-container">
      <div className="header">
        <span className="header-logo">⬡</span>
        <span className="header-title">Mapping</span>
        <span className="header-sep">/</span>
        <span className="header-sub">Order to Cash</span>
      </div>
      <div className="main-content">
        <GraphCanvas onNodeSelect={setSelectedNode} />
        <ChatPanel selectedNode={selectedNode} />
      </div>
    </div>
  );
}

export default App;