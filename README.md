# 🧩 Automated Software Developement LifeCycle

A proof-of-concept **agentic workflow** that automates major phases of the SDLC (requirements → design → planning → implementation → testing → deployment) using **LangGraph**, **Google Gemini**, and a lightweight **Human-In-The-Loop (HITL)** gate.  
It exposes a **FastAPI** backend where you can POST a project specification and receive a fully processed SDLC state.
---

## ✨ Features

- **Gemini (Google Generative AI)** for requirement analysis & reasoning
- **LangGraph** workflow orchestrating:
  - Requirements → Design → Planning → Implementation → Testing → Deployment
- **Human-in-the-loop** gates (manual approval / rejection)
- **FastAPI** endpoints for programmatic access
- Auto-persisted final state as JSON
- Modular folder structure for easy extension

---

## 📁 Project Structure
```
Automated-SDLC/
├── api.py # FastAPI app & routes
├── main.py # Optional CLI entrypoint
├── requirements.txt # Python dependencies
├── .env # API keys (GOOGLE_API_KEY)
├── output/ # Workflow results (final_state.json, etc.)
├── notebooks/ # Experiments & playground
│ └── exp.ipynb
└── src/
 ├── init.py
 ├── workflow.py # LangGraph build + run
 ├── data_models.py # TypedDicts & dataclasses
 ├── hitl.py # Human-in-the-loop logic
 ├── llm.py # Gemini wrapper (LangChain)
 ├── utils.py # Helpers (JSON parsing, etc.)
 └── nodes/ # Workflow nodes
    ├── init.py
    ├── requirements.py
    └── design.py
    ├── implementation.py
    ├── test.py
    └── deployement.py
├── api.py
├── main.py
```


---

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone https://github.com/Ash2809/Automated-SDLC.git
```

```
cd automated-sdlc
```
```
python -m venv .venv && source .venv/bin/activate   # (Windows: .venv\Scripts\activate)
```
```
pip install -r requirements.txt
```
### 2. Configure

**Create a .env file with your Google API key:**

GOOGLE_API_KEY=your_google_key_here

### 3. Run the API
```
uvicorn api:app --reload
```
**FastAPI interactive docs available at: http://127.0.0.1:8000/docs**

---
### 🧑‍💻 Development Notes

**Human-in-the-loop gates:** For each major step, the workflow can pause for approval (CLI or other provider).

**Extensibility:** Add new workflow nodes in src/nodes/ and wire them into src/workflow.py.

**Persistence:** The orchestrator saves the last workflow state into output/final_state.json.

---

### 🔮 Future Developement Scope

Richer HITL UX (web dashboard)

Real test execution & coverage metrics

Deployment to cloud (Docker + Kubernetes)

Support for multiple LLM providers

---

### ⚖️ License

**MIT License — free for personal and commercial use.**

---

### 🙏 Acknowledgements

LangGraph

LangChain

FastAPI

Google Generative AI (Gemini)