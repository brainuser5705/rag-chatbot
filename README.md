# Python RAG Chatbot

Tkinter GUI application for a AI Chatbot enhanced with a RAG (Retrieval Augmented Generation) pipeline.

The RAG pipeline is comprised of:
- Unstructured (Document Ingestion)
- Qdrant (Vector Database)
- LM Studios (Embedding and LLM)

Other tools/frameworks used:
- Langchain (OpenAI API endpoints, LLM interactions)
- Redis Queue (Job queue)

---

## Project Directory

- `models/` contains classes representing the main components of the RAG system.
- `main.py` runs the Tkinter GUI
- `process.py` has the functions called by the GUI to initiate the RAG system and chatbot functionality.

---

## How to Run

To run on WSL, install Xming for Windows and type `export DISPLAY=localhost:0.0` in the terminal.

Local Environment variables to set in `.env` file:
- QDRANT_SERVER_URL
- UNSTRUCTURED_API_KEY
- UNSTRUCTURED_API_URL
- LM_STUDIOS_SERVER_URL

---

## TO DO

- langchain chat...
- qdrant sharding
- tkinter stuff...
- async api calls
- coloring