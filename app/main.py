"""
FastAPI application entry point for the Digital Finance AI Service.

Provides four AI capabilities:
  - /api/v1/scoring   — qualification scoring
  - /api/v1/matching  — plan matching
  - /api/v1/risk      — risk warning
  - /api/v1/summary   — report summarization
"""

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import matching, risk, scoring, summary

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Digital Finance AI Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scoring.router, prefix="/api/v1/scoring", tags=["scoring"])
app.include_router(matching.router, prefix="/api/v1/matching", tags=["matching"])
app.include_router(risk.router, prefix="/api/v1/risk", tags=["risk"])
app.include_router(summary.router, prefix="/api/v1/summary", tags=["summary"])


@app.get("/")
async def root():
    return {"service": "ai-service", "version": "1.0.0", "status": "healthy"}


@app.get("/health")
async def health():
    return {"status": "ok"}