# 🤖 Multi-Agent Research System

> An intelligent multi-agent research backend that autonomously searches the web, reads relevant sources, generates structured research reports, and critically evaluates the final output.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-Agentic%20AI-green)
![Groq](https://img.shields.io/badge/LLM-Groq-orange)
![Tavily](https://img.shields.io/badge/Web%20Search-Tavily-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Overview

**Multi-Agent Research System** is an AI-powered research automation backend designed to transform a simple research topic into a structured, critically reviewed research report.

Instead of asking a single LLM to perform the entire task, the system separates the research workflow into specialized stages.

The current pipeline follows:

```text
User Topic
    ↓
Search Agent
    ↓
Web Search
    ↓
Reader Agent
    ↓
URL Scraping
    ↓
Writer
    ↓
Research Report
    ↓
Critic
    ↓
Quality Evaluation
    ↓
Final Research State

Each stage has a specific responsibility, making the system easier to understand, debug, extend, and improve.

✨ Key Features
🔎 Autonomous Web Research

The Search Agent uses Tavily to search the web for relevant information.

It can retrieve:

Recent information
Relevant articles
Research material
Source URLs
Search snippets
Multiple web results

The Search Agent can decide when to use the web-search tool based on the research task.

📖 Source Reading

After searching, the Reader Agent identifies a relevant URL from the search results and uses a dedicated scraping tool to extract deeper content.

The scraper:

Sends an HTTP request to the selected URL
Uses a browser-like User-Agent
Parses HTML using BeautifulSoup
Removes unnecessary HTML elements
Extracts readable text
Limits extracted content to a manageable size

The extracted content is then passed to the next stage of the pipeline.

✍️ AI Research Writer

The Writer stage transforms the collected research into a structured report.

The generated report is organized around:

Introduction
      ↓
Key Findings
      ↓
Conclusion
      ↓
Sources

The Writer is instructed to produce:

Clear explanations
Structured findings
Detailed analysis
Professional language
Source URLs
🧐 AI Research Critic

The generated report is passed to a separate Critic stage.

The Critic evaluates the report and produces:

Score: X/10

Strengths:
- ...

Areas to Improve:
- ...

One line verdict:
...

This introduces a generation → evaluation pattern into the research workflow.

🧠 Multi-Agent Architecture

The system separates responsibilities between specialized AI components.

                     ┌───────────────────┐
                     │    User Topic     │
                     └─────────┬─────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Search Agent     │
                    │                     │
                    │   Groq + Tavily     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Search Results   │
                    │                     │
                    │ Titles / URLs /     │
                    │ Snippets            │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Reader Agent     │
                    │                     │
                    │   Groq + Scraper    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Scraped Content    │
                    │                     │
                    │   Deeper Source     │
                    │      Context        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Research Writer   │
                    │                     │
                    │   Groq LLM Chain    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Research Report   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Research Critic   │
                    │                     │
                    │ Score + Feedback    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Final State      │
                    │                     │
                    │ Search              │
                    │ Scraped Content     │
                    │ Report              │
                    │ Feedback            │
                    └─────────────────────┘
🔄 Complete Workflow
1. User Provides a Topic

The user submits a research topic through the FastAPI API.

Example:

Impact of Generative AI on Software Development

The topic becomes the initial input to the research pipeline.

2. Search Agent

The Search Agent receives the research topic and is instructed to find relevant information.

Conceptually:

Research Topic
      ↓
Search Agent
      ↓
Tavily Web Search
      ↓
Search Results

The search results contain information such as:

Title
URL
Snippet

The resulting information is stored in the research state.

3. Reader Agent

The Reader Agent receives the search results and identifies a relevant URL.

Its workflow is:

Search Results
      ↓
Reader Agent
      ↓
Select Relevant URL
      ↓
Scrape URL
      ↓
Extract Detailed Content

The Reader Agent has access to a dedicated URL scraping tool.

4. Research Writer

The Writer receives the research information collected during the previous stages.

Conceptually:

Search Results
      +
Scraped Content
      ↓
Writer Prompt
      ↓
Groq LLM
      ↓
Research Report

The Writer produces a structured research report containing an introduction, findings, conclusion, and sources.

5. Research Critic

The generated report is then evaluated by the Critic.

Research Report
      ↓
Critic Prompt
      ↓
Groq LLM
      ↓
Score
+
Strengths
+
Areas to Improve
+
Verdict

This provides an explicit quality-control stage after report generation.

🧩 Agent & Tool Design

The project uses specialized agents and dedicated tools.

Search Agent
Groq LLM
    ↓
Search Agent
    ↓
Tavily Web Search
Responsibility

Discover relevant information and sources from the web.

Reader Agent
Groq LLM
    ↓
Reader Agent
    ↓
URL Scraper
    ↓
Clean Web Content
Responsibility

Select a relevant source and retrieve deeper information from it.

Writer

The Writer is implemented as an LLM chain.

Research Context
       ↓
Writer Prompt
       ↓
Groq LLM
       ↓
Structured Research Report
Responsibility

Convert collected research into a readable and structured report.

Critic

The Critic is implemented as a separate LLM chain.

Research Report
       ↓
Critic Prompt
       ↓
Groq LLM
       ↓
Score + Feedback
Responsibility

Evaluate the quality of the generated research report.

🛠️ Tech Stack
Technology	Purpose
Python	Core application
FastAPI	REST API backend
Pydantic	Request validation
LangChain	LLM and agent orchestration
Groq	LLM inference
Tavily	Web search
Requests	HTTP requests
BeautifulSoup	HTML parsing
python-dotenv	Environment variables
Uvicorn	ASGI server
📂 Project Structure
Multi-Agent-Research-System/
│
├── agents.py
│   ├── Search Agent
│   ├── Reader Agent
│   ├── Writer Chain
│   └── Critic Chain
│
├── tools.py
│   ├── web_search()
│   └── scrape_url()
│
├── pipeline.py
│   └── Research orchestration
│
├── main.py
│   ├── FastAPI application
│   ├── /health endpoint
│   └── /research endpoint
│
├── requirements.txt
├── .gitignore
└── README.md
🔌 API

The system exposes a REST API using FastAPI.

Health Check
Endpoint
GET /health
Response
{
  "status": "ok"
}
Research Endpoint
Endpoint
POST /research
Request
{
  "topic": "Artificial Intelligence in Healthcare"
}
Response
{
  "search_result": "...",
  "scraped_content": "...",
  "report": "...",
  "feedback": "..."
}

The response contains the accumulated research state.

🔐 Environment Variables

Create a .env file in the project root.

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
Important

Never commit your .env file to GitHub.

The .gitignore should exclude sensitive and generated files such as:

.env
.venv/
__pycache__/
*.pyc
.idea/
.vscode/
🚀 Local Setup
1. Clone the Repository
git clone <your-repository-url>

cd Multi-Agent-Research-System
2. Create Virtual Environment
python -m venv .venv
Windows
.venv\Scripts\activate
Linux / macOS
source .venv/bin/activate
3. Install Dependencies
pip install -r requirements.txt
4. Configure API Keys

Create:

.env

Add:

GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
▶️ Run the Application

Start the FastAPI server:

uvicorn main:app --reload

The backend will be available at:

http://127.0.0.1:8000
📚 API Documentation

FastAPI automatically provides interactive API documentation.

Open:

http://127.0.0.1:8000/docs

You can test the available endpoints directly from the Swagger UI.

🧪 Example
Input
Research Topic:

"Impact of Large Language Models on Software Engineering"
Internal Pipeline
Topic
 ↓
Search Agent
 ↓
Tavily
 ↓
Search Results
 ↓
Reader Agent
 ↓
Relevant URL
 ↓
Web Scraper
 ↓
Detailed Content
 ↓
Writer
 ↓
Research Report
 ↓
Critic
 ↓
Evaluation
Final Output

The API returns the accumulated research state:

search_result
scraped_content
report
feedback
🧠 Why Use Multiple Agents?

A single LLM could theoretically perform the entire task.

However, separating responsibilities creates a more modular agentic architecture.

Single LLM Approach
User
 ↓
One LLM
 ↓
Final Answer
Multi-Agent Approach
User
 ↓
Search
 ↓
Read
 ↓
Write
 ↓
Critique
 ↓
Final Output

Each component focuses on a specific responsibility.

This makes the system:

Modular
Easier to debug
Easier to extend
Easier to evaluate
Easier to reason about
Better suited for complex workflows
🔄 State-Based Pipeline

The research workflow maintains a shared state.

Conceptually:

state = {
    "search_result": ...,
    "scraped_content": ...,
    "report": ...,
    "feedback": ...
}

The state progressively accumulates information.

Initial State
     ↓
Search Result Added
     ↓
Scraped Content Added
     ↓
Report Added
     ↓
Critic Feedback Added
     ↓
Final Research State

This makes the pipeline easy to extend with additional stages.

🎯 Design Philosophy

The architecture follows a specialization-first approach.

Search

Find relevant information.

Reader

Read deeper into selected sources.

Writer

Convert research into a structured report.

Critic

Evaluate the generated report.

This creates a clear separation of responsibilities across the research workflow.

⚡ Agentic AI Concepts Demonstrated

This project demonstrates practical implementation of:

Agentic AI
AI Agents
Multi-Agent Systems
Tool Calling
Agent Specialization
LLM Orchestration
Web Search
Web Scraping
Research Automation
Prompt Engineering
LLM Chains
Critic / Evaluator Pattern
State-Based Pipelines
REST APIs
FastAPI
External AI APIs
Automated Research Workflows
🔍 Agentic Workflow vs Traditional LLM
Traditional LLM
User Question
      ↓
     LLM
      ↓
   Response

The model primarily relies on the context provided to it.

This System
User Topic
      ↓
Search Agent
      ↓
Web Search Tool
      ↓
Reader Agent
      ↓
Scraping Tool
      ↓
Writer
      ↓
Critic
      ↓
Research Output

The system can gather external information, process source content, generate a report, and evaluate the generated result.

🛡️ Error Handling

The API includes basic validation and exception handling.

Empty Topic

If the user submits an empty research topic, the API validates the request instead of executing the research pipeline.

Example:

{
  "topic": ""
}
Pipeline Errors

Unexpected errors during the research pipeline are handled by the API and returned as HTTP errors rather than silently failing.

⚠️ Current Limitations

The current implementation is designed as an agentic AI backend / portfolio project.

Potential production-level improvements include:

 Persistent research history
 Database integration
 Authentication
 User-specific research sessions
 Async tool execution
 Parallel research agents
 Multiple-source verification
 Source credibility scoring
 Improved web content extraction
 PDF/document research
 Citation validation
 Structured JSON report schema
 Streaming responses
 Rate limiting
 Retry mechanisms
 Observability and tracing
 Docker deployment
 Cloud deployment
 Automated evaluation
 Human feedback loop
🔮 Future Architecture

The current sequential architecture can be extended into a more advanced research system.

                         User
                          │
                          ▼
                 ┌─────────────────┐
                 │ Research Planner│
                 └────────┬────────┘
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
      Search Agent   Academic Agent  News Agent
            │             │             │
            └─────────────┼─────────────┘
                          ▼
                  Source Verification
                          │
                          ▼
                    Reader Agents
                          │
                          ▼
                  Evidence Aggregator
                          │
                          ▼
                    Report Writer
                          │
                          ▼
                     Critic Agent
                          │
                          ▼
                   Final Research

Possible future capabilities include:

Research planning
Parallel agent execution
Multiple search providers
Academic paper search
Source verification
Evidence aggregation
Iterative report refinement
Citation checking
Long-term research memory
📊 Current Pipeline
┌───────────────────────────────────────────────┐
│              MULTI-AGENT RESEARCH             │
└───────────────────────────────────────────────┘

              USER TOPIC
                  │
                  ▼
        ┌───────────────────┐
        │   SEARCH AGENT    │
        │      Groq         │
        │       +           │
        │     Tavily        │
        └─────────┬─────────┘
                  │
                  ▼
           SEARCH RESULTS
                  │
                  ▼
        ┌───────────────────┐
        │   READER AGENT    │
        │      Groq         │
        │       +           │
        │   URL Scraper     │
        └─────────┬─────────┘
                  │
                  ▼
          SCRAPED CONTENT
                  │
                  ▼
        ┌───────────────────┐
        │      WRITER       │
        │      Groq         │
        └─────────┬─────────┘
                  │
                  ▼
           RESEARCH REPORT
                  │
                  ▼
        ┌───────────────────┐
        │      CRITIC       │
        │      Groq         │
        └─────────┬─────────┘
                  │
                  ▼
        SCORE + FEEDBACK
💡 What Makes This Project Interesting?

The core of this project is not simply calling an LLM.

It demonstrates how LLMs can be combined with:

LLMs
 +
Tools
 +
Specialized Responsibilities
 +
External Information
 +
Sequential Workflow
 +
Evaluation

to create a practical agentic research system.

The architecture separates:

Information Discovery
        ↓
Information Extraction
        ↓
Information Synthesis
        ↓
Quality Evaluation

This provides a strong foundation for building more advanced autonomous research systems.

👨‍💻 Author
Kushagra Nayak

AI / ML Engineer focused on:

Generative AI
Agentic AI
Multi-Agent Systems
Retrieval-Augmented Generation
LLM Applications
AI Agents
Backend Development
Intelligent Automation
⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

📜 License

This project is licensed under the MIT License.


**Bas pura block copy → `README.md` → paste → save → Git commit → push.**
