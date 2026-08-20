# Multi-Agent Workflow Project

A practical multi-agent AI project built with Python and Microsoft Agent Framework.

This project demonstrates three different multi-agent workflow patterns:

- Sequential Workflow
- Concurrent Workflow
- Handoff Workflow

The project also demonstrates how AI agents can interact with a local SQL Server database using database tools.

---

## Project Overview

The goal of this project is to explore how multiple AI agents can work together using different workflow patterns.

The project includes:

1. **Sequential Workflow** – agents execute one after another in a predefined order.
2. **Concurrent Workflow** – multiple agents execute tasks simultaneously.
3. **Handoff Workflow** – a router agent sends the user's request to the appropriate specialized agent.
4. **Database Integration** – specialized agents can retrieve real data from a local SQL Server database.
5. **Agent Framework DevUI** – provides a user interface for testing and observing agent workflows.

---

# Technologies Used

- Python
- Microsoft Agent Framework
- OpenAI
- Agent Framework Core
- Agent Framework Orchestrations
- Agent Framework DevUI
- SQL Server
- SQLAlchemy
- pyodbc
- python-dotenv
- uv

---

# Project Structure

```text
multi-agent-workflow/
│
├── .env
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml
│
├── main.py
│
├── agent_instructions.py
├── db.py
│
├── seq-workflow.py
├── concurrent-workflow.py
├── enquiry_workflow.py
└── translator-workflow.py
