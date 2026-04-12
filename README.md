# AI Itinerary Planner Agent

A production-style **AI-powered itinerary planning agent** built with a clean, modular Python architecture.

This project demonstrates how to design an agent-based system that accepts a destination as input, orchestrates multiple tools, validates requests, calls external travel APIs, and returns structured itinerary suggestions such as **nearest airports, hotel recommendations, and travel planning details**.

It is designed as both a **reference project for scalable backend + AI agent architecture** and a **portfolio-ready engineering project**.

---

## Overview

The goal of this project is to showcase how modern AI-agent workflows can be designed using production engineering principles:

* clear separation of concerns
* service-oriented design
* tool-based orchestration
* retry and resilience patterns
* validation and configuration management
* scalable folder structure

This project is especially useful for developers learning how to move from a prototype script to a **production-ready AI backend service**.

---

## Features

* Modular **agent orchestration layer**
* Dedicated **tool abstraction layer**
* Service-based external API integrations
* Centralized validation and config management
* Retry support with exponential backoff using `tenacity`
* Async-ready workflow design
* Structured logging
* Clean and scalable project structure
* Easy to extend with new tools/services

---

## Project Structure

```text
agents/       # agent orchestration and workflow logic
services/     # external API/service integrations
tools/        # callable tools used by the agent
clients/      # request/response models and DTOs
models/       # domain models
config.py     # application constants and settings
validation.py # validation helpers
main.py       # application entry point
```

---

## Architecture

```text
User Input
   ↓
Agent Layer
   ↓
Tool Layer
   ↓
Service Layer
   ↓
External APIs
   ↓
Structured Itinerary Response
```

### Layer Responsibilities

### Agent Layer

Responsible for:

* understanding user request
* deciding tool execution order
* orchestrating workflow
* aggregating final response

### Tool Layer

Responsible for:

* input validation
* response transformation
* service invocation
* reusable business actions

### Service Layer

Responsible for:

* external API communication
* retries
* request formatting
* response parsing

This layered design makes the application **maintainable, testable, and scalable**.

---

## Tech Stack

* **Python**
* **asyncio**
* **requests / http clients**
* **tenacity** for retry logic
* **logging**
* modular service architecture

---

## Installation

Clone the repository:

```bash
git clone <your-repo-url>
cd itinerary-planner-agent
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create a `.env` file or configure your API keys in config:

```text
GOOGLE_MAP_PLACE_API_URL=<Your Google Places API endpoint>
GOOGLE_API_TOKEN=<Your Google API key>
SEARCH_API_BASE_URL=<Your Search API base URL>
SEARCH_API_AIRPORT_DETAILS=<Airport details endpoint>
SEARCH_API_KEY=<Your Search API key>
ANTHROPIC_API_KEY=<Your Anthropic API key>
```

Recommended: include `.env` in the repository.

---

## Running the Project

```bash
python main.py
```

---

## Example Usage

### Input

```text
Goa
```

### Output

```text
Nearest airport: Goa International Airport
Top hotel recommendations
Suggested itinerary summary
```

---

## Engineering Highlights

This project intentionally focuses on production engineering practices:

* modular folder design
* low coupling / high cohesion
* centralized validation
* retry with exponential backoff
* reusable service abstractions
* clean logging strategy

These patterns are commonly used in **real-world backend and AI systems**.

---

## Use Cases

This project can be used as:

* reference architecture for AI agents
* backend system design sample
* interview portfolio project
* base template for FastAPI AI services
* Docker / Kubernetes learning project

## 🔐 Environment Variables

All sensitive configuration (API keys, URLs) is managed through environment variables in a `.env` file, keeping credentials secure and configuration flexible.
