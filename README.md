# Agent Framework Workflows

A multi-agent workflow project built with Python and Microsoft Agent Framework.

This project demonstrates three different multi-agent workflow patterns:

- Sequential Workflow
- Concurrent Workflow
- Handoff Workflow

The Handoff workflow is connected to a local SQL Server database and uses multiple specialized agents to answer customer enquiries.

---

## Workflows

### 1. Sequential Workflow

The Sequential workflow executes agents in a specific order.

Example:

```text
Agent 1
   ↓
Agent 2
   ↓
Agent 3
