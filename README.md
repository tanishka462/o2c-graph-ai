# O2C Graph AI Explorer

## Overview

O2C Graph AI Explorer is an AI-powered graph exploration tool designed to analyze the SAP Order-to-Cash (O2C) process. The system allows users to visualize relationships between business entities such as customers, sales orders, deliveries, billing documents, journal entries, and payments.

The application combines:
- Graph visualization
- Natural language querying
- SQL generation using LLM
- Relationship exploration

Users can:
- Explore entity relationships visually
- Ask natural language questions
- View generated SQL queries
- Inspect returned data

---

## Live Demo

Frontend:
https://o2c-graph-ai.vercel.app

Backend API:
https://o2c-graph-ai-1.onrender.com/docs

Note:
Backend may take 30-60 seconds to wake up due to free hosting tier.

---

## Architecture

System architecture follows a simple 3-layer design:

Frontend (React + Vite)
        |
Backend API (FastAPI)
        |
SQLite Database + LLM

### Frontend
Technology:
- React
- Vite
- Vis Network Graph Library
- Axios

Responsibilities:
- Graph visualization
- Chat interface
- Node inspection
- API communication

### Backend
Technology:
- FastAPI
- Python
- SQLite
- Gemini LLM

Responsibilities:
- Data loading
- Graph building
- SQL generation
- Question answering
- Guardrails enforcement

### Database

Technology:
SQLite

Why SQLite:
- Lightweight
- No infrastructure required
- Suitable for read-heavy dataset
- Easy deployment
- Good for prototyping

---

## Graph Modelling

Entities modeled:

BusinessPartner  
SalesOrder  
SalesOrderItem  
Delivery  
DeliveryItem  
BillingDocument  
JournalEntry  
Payment  
Product  
Plant  

Relationships modeled:

Customer → SalesOrder  
SalesOrder → Items  
Items → Products  
Items → Delivery  
Delivery → Plant  
Billing → JournalEntry  
JournalEntry → Payment  

Graph design allows exploration of full O2C lifecycle.

---

## LLM Integration Strategy

The LLM is used only for:

Natural language → SQL translation  
Answer explanation

The LLM is NOT allowed to:
- Modify database
- Execute unsafe queries
- Access external data

Prompt includes:

Database schema  
Table relationships  
Allowed query types  
Response format rules  

Example workflow:

User question  
→ Prompt constructed with schema  
→ LLM generates SQL  
→ SQL validated  
→ Query executed  
→ Result returned  

---

## Prompt Engineering Strategy

Prompt contains:

Role definition:
"You are a data analyst for SAP Order-to-Cash data."

Schema context:
Tables and relationships.

Rules:
Only SELECT queries.
No modifications.

Output format:
SQL + explanation.

Fallback:
Return NOT_RELATED if question invalid.

This ensures safe and relevant SQL generation.

---

## Guardrails

Multiple safety guardrails implemented:

Query Guardrails:
- Only SELECT allowed
- Block INSERT/DELETE/UPDATE
- Block DROP/ALTER
- Limit result size

Question Guardrails:
- Reject unrelated questions
- Reject non-O2C topics
- Schema restricted answering

Execution Guardrails:
- SQL validation before execution
- Exception handling
- Safe fallback responses

LLM Guardrails:
- Schema constrained prompting
- Deterministic output format
- Query verification

---

## AI Usage

AI tools were actively used during development.

Tools used:

ChatGPT:
Architecture planning  
Debugging  
Prompt design  
Deployment fixes  
CORS troubleshooting  
Data loading debugging  

AI was used for:

Code improvements  
Error debugging  
SQL prompting design  
Architecture decisions  
Deployment troubleshooting  

Development approach:

Design → Build → Test → Debug → Improve.

---

## Challenges Faced

Key challenges:

CORS issues between Vercel and Render  
Data loading in cloud environment  
LLM query reliability  
Graph performance optimization  
Deployment debugging  

Solutions:

Explicit CORS configuration  
Absolute data paths  
SQL validation layer  
Graph limits  
Structured prompts  

---

## Key Engineering Decisions

Why FastAPI:
Fast development
Async support
Easy deployment
Simple routing

Why Graph:
O2C is relationship heavy.
Graph makes lifecycle visible.

Why LLM SQL generation:
Natural language improves usability.

Why SQLite:
Simple deployment.
Dataset size manageable.

Why separated layers:
Maintainability.
Testability.
Scalability.

---

## Running Locally

Backend:

Navigate:
backend

Install:

pip install -r requirements.txt

Run:

uvicorn main:app --reload

Frontend:

Navigate:
frontend

Install:

npm install

Run:

npm run dev

---

## Project Structure
