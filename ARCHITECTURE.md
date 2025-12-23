# Kaien System Architecture

## Vision
A modular, autonomous AI operating environment with self-development capabilities, OSINT engines, and RAG memory.

## Core Structure
1.  **Server (The Nexus):**
    -   Framework: FastAPI (Async).
    -   Role: Central orchestration, state management, tool dispatch.
    -   Database: SQLite (Session history), ChromaDB (Vector memory).
    -   API: Exposes endpoints for Client communication.

2.  **Client (The Interface):**
    -   CLI: Built with `Typer` and `Rich` for a beautiful terminal UI.
    -   Web: Built with Flask (as requested) or Streamlit/FastHTML for dashboarding.
    -   Communication: WebSockets for real-time streaming.

3.  **Modules (The Spokes):**
    -   **Shell Agent:** Safe async wrapper around `subprocess`.
    -   **Research Agent:** Implements `Deep Research` loop (LangGraph).
    -   **OSINT Agent:** Dockerized security tools.
    -   **Dev Agent:** File manipulation and testing.

## Technology Stack
-   **Language:** Python 3.11+
-   **LLM Interface:** LiteLLM (for provider agnosticism).
-   **Orchestration:** LangGraph (for complex workflows).
-   **Vector Store:** ChromaDB.
-   **Protocol:** Model Context Protocol (MCP) for tool definitions.