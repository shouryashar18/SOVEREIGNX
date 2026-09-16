from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.workspace import router as workspace_router
from app.routers.documents import router as documents_router
from app.routers.analysis import router as analysis_router
from app.routers.agents import router as agents_router


app = FastAPI(
    title="Sovereign Industrial AI Workbench",
    version="1.0.0"
)


# =====================================================
# CORS
# =====================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# ROUTERS
# =====================================================

app.include_router(
    workspace_router
)

app.include_router(
    documents_router
)

app.include_router(
    analysis_router
)

app.include_router(agents_router)


# =====================================================
# ROOT
# =====================================================

@app.get("/")
def root():
    return {
        "message": "SovereignX Backend Running",
        "status": "online"
    }


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/health")
def health():
    return {
        "status": "ok"
    }