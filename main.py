# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pipeline import run_research_pipeline

app = FastAPI(title="MARS Backend")

# --- CORS ---------------------------------------------------------
# Vite dev server default port is 5173 — matches your screenshot URL.
# Add your Vercel production domain once deployed.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        # "https://your-mars-app.vercel.app",
        "https://multi-agent-research-system-frontend.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ResearchRequest(BaseModel):
    topic: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/research")
def research(payload: ResearchRequest):
    """
    Runs your existing Search -> Reader -> Writer -> Critic pipeline
    unchanged. Defined as a sync `def` (not `async def`) on purpose:
    FastAPI runs sync endpoints in a threadpool automatically, so the
    blocking LLM/requests calls inside run_research_pipeline don't
    stall the event loop.
    """
    topic = payload.topic.strip()
    if not topic:
        raise HTTPException(status_code=422, detail="Topic cannot be empty.")

    try:
        result = run_research_pipeline(topic)
    except Exception as e:
        # Surfaces as `detail` in the response body — the frontend's
        # apiClient reads `detail` specifically for its error message.
        raise HTTPException(status_code=500, detail=str(e))

    return result