# SovereignX — On-Premise Agentic AI Workbench

**SIH26117 — Sovereign On-Premise Agentic AI Workbench using Open-Weight Multimodal LLMs for Confidential Industrial Work**

SovereignX is an **on-premise Agentic AI Workbench** designed for confidential industrial environments. It enables organizations to work with industrial documents, diagrams, and data using **open-weight multimodal AI models running locally**, without depending on external cloud AI services.

## Key Features

* 🏭 Industry-specific workspaces
* 📁 Secure document and file management
* 🤖 Local AI-powered document analysis
* 👁️ Multimodal analysis of industrial diagrams and images
* 📊 Analysis results and risk identification
* 📝 Automated report generation
* 🔐 Organization-based workspace structure
* 🧠 Open-weight local AI models through Ollama
* ☁️ No dependency on external cloud AI APIs

## Technology Stack

### Frontend

* React
* Vite
* JavaScript
* HTML/CSS

### Backend

* FastAPI
* Python
* MongoDB
* REST APIs

### Local AI

* Ollama
* Qwen 2.5 7B Instruct
* LLaVA

## Project Structure

```text
SOVEREIGNX/
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routers/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   └── requirements.txt
│
└── README.md
```

## How It Works

1. The user selects an industrial sector.
2. An organization/workspace is created.
3. Users access their dedicated workspace.
4. Industrial documents, diagrams, or images can be uploaded.
5. The backend processes the uploaded data.
6. Local AI models analyze the content.
7. The system identifies relevant risks, observations, and insights.
8. Analysis results can be used to generate reports.

## Running the Project

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The FastAPI API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

## Local AI Setup

SovereignX uses Ollama to run AI models locally.

Required models:

```bash
ollama pull qwen2.5:7b-instruct
ollama pull llava:latest
```

The AI processing remains local, supporting confidential industrial use cases.

## Screens & UI

The project includes multiple UI screens covering areas such as:

* Industry Selection
* Authentication
* Dashboard
* AI Agents
* Document Analysis
* Analysis Studio
* Compliance
* Industrial Workspaces

## Current Status

SovereignX is under active development as an SIH project. The current implementation combines the frontend interface, FastAPI backend, MongoDB workspace management, document processing, and local multimodal AI capabilities.

## Future Scope

* Complete end-to-end agentic workflows
* Advanced industrial risk analysis
* More industry-specific AI agents
* Improved report generation
* Role-based access control
* Additional multimodal models
* Production-ready deployment for on-premise environments
