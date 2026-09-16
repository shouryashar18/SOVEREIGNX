from pydantic import BaseModel, Field
from typing import List, Optional


class Finding(BaseModel):
    title: str
    description: str
    severity: str
    component: Optional[str] = None


class Recommendation(BaseModel):
    action: str
    priority: str
    reason: Optional[str] = None


class AIModelMetrics(BaseModel):
    risk_score: float = Field(ge=0, le=100)
    severity: str
    primary_component: Optional[str] = None
    urgency_hours: Optional[int] = None


class AnalysisRequest(BaseModel):
    industry: str
    analysis_type: str = "full"


class AnalysisResponse(BaseModel):
    document_id: str
    workspace_id: str
    industry: str

    model_used: str
    vision_model_used: Optional[str] = None

    risk_score: float = Field(ge=0, le=100)
    severity: str

    primary_component: Optional[str] = None
    urgency_hours: Optional[int] = None

    findings: List[Finding] = []
    recommendations: List[Recommendation] = []
    compliance_concerns: List[str] = []

    status: str


class VisionAnalysisResponse(BaseModel):
    model_used: str
    task: str
    result: str

class AnalysisRequest(BaseModel):
    analysis_type: str