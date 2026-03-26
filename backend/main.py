from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import init_db
from data_loader import load_all_data
from graph_builder import get_graph_data, get_node_details, get_node_connections
from chat import answer_question
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str

@app.on_event("startup")
async def startup():

    print("Initializing database...")

    init_db()

    load_all_data()

    print("Data loaded successfully")

@app.get("/api/graph")
def graph(limit: int = 200):
    nodes, edges = get_graph_data(limit)
    return {"nodes": nodes, "edges": edges}

@app.get("/api/node/{node_type}/{node_id:path}")
def node_details(node_type: str, node_id: str):
    details = get_node_details(node_id, node_type)
    connections = get_node_connections(node_id)
    return {"details": details, "connections": connections}

@app.post("/api/chat")
def chat(req: ChatRequest):
    result = answer_question(req.question)
    return result

@app.get("/")
def root():
    return {"status": "O2C Graph API running!"}