# Multi-Agent Workflow

A practical multi-agent AI project built with Python and Microsoft Agent Framework. The project demonstrates three different workflow patterns: **Sequential, Concurrent, and Handoff**. It also integrates AI agents with a local SQL Server database to retrieve real customer, food, order, and payment information.

## Overview

This project explores how multiple AI agents can work together using different workflow patterns.

The project includes:

- **Sequential Workflow** — agents execute one after another in a defined order.
- **Concurrent Workflow** — multiple agents execute tasks independently and simultaneously.
- **Handoff Workflow** — a router agent directs a request to the appropriate specialized agent.
- **SQL Server Integration** — agents use Python tools to retrieve information from a local database.
- **Agent Framework DevUI** — provides an interface for testing and observing workflow execution.

## Workflow Architecture

### Sequential Workflow

In a sequential workflow, each agent runs after the previous agent finishes.

```text
User Request
     |
     v
  Agent 1
     |
     v
  Agent 2
     |
     v
  Agent 3
     |
     v
Final Response
