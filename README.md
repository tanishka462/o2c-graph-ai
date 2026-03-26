# AI Order-to-Cash Graph Intelligence System

## Overview

This project implements an AI-powered Order-to-Cash (O2C) analytics platform combining graph visualization with LLM-powered natural language querying.

The system allows users to:
• Explore SAP O2C relationships via graph visualization
• Query business data using natural language
• Automatically generate SQL using LLM
• Analyze customers, orders, billing and payments

## Architecture

Frontend:
React + Vite

Backend:
FastAPI Python service

Database:
SQLite relational database

AI Layer:
Google Gemini LLM for SQL generation

Architecture flow:

React UI → FastAPI → LLM SQL Generator → SQLite → Graph Builder → UI

## Database Choice

SQLite was selected due to:
• Simplicity
• Zero configuration
• Relational nature of SAP O2C data
• Fast local querying

## LLM Prompt Strategy

The LLM is used strictly for SQL generation.

Techniques used:

• Schema grounded prompting
• SQL only responses
• LIMIT enforcement
• Table mapping rules
• Fallback deterministic queries

## Guardrails

Implemented safeguards:

• Schema restricted prompting
• Query limits
• SQL validation
• Fallback rule engine
• Dataset scope restriction

## AI Usage

AI tools used:

ChatGPT:
Architecture design
Debugging
Prompt refinement

Gemini:
SQL generation
Answer explanations

GitHub Copilot:
Code completion

## Features

Graph visualization
AI SQL query generation
Document lookup
Business partner analysis
Payment tracking

## Setup

Backend:

pip install -r requirements.txt

uvicorn main:app --reload

Frontend:

npm install

npm run dev

## Example Questions

show customers

show sales orders

show journal entries

find journal entry 91150187

## Demo

Frontend:
(Add Vercel link)

Backend:
(Add Render link)