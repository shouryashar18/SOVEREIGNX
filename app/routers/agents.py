from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.database import db
from app.services.agents import run_safety_agent


router = APIRouter(
    prefix="/agents",
    tags=["AI Agents"]
)


# =====================================================
# CHAT REQUEST MODEL
# =====================================================

class AgentChatRequest(BaseModel):

    message: str

    agent: str = "Safety Agent"

    workspace_id: Optional[str] = None

    industry: Optional[str] = "Industrial"

    document_id: Optional[str] = None

    agent_id: Optional[str] = None


# =====================================================
# AI AGENTS CHAT
# =====================================================

@router.post("/chat")
def agent_chat(request: AgentChatRequest):

    try:

        message = request.message.strip()

        if not message:

            raise HTTPException(
                status_code=400,
                detail="Message cannot be empty"
            )


        # =================================================
        # GET DOCUMENT IF PROVIDED
        # =================================================

        filename = "No document provided"

        previous_analysis = ""


        if request.document_id:

            document = db.documents.find_one(
                {
                    "id": request.document_id
                },
                {
                    "_id": 0
                }
            )


            if document:

                filename = document.get(
                    "filename",
                    "Unknown"
                )


            analysis = db.analyses.find_one(
                {
                    "document_id":
                        request.document_id
                },
                {
                    "_id": 0
                }
            )


            if analysis:

                previous_analysis = analysis.get(
                    "result",
                    ""
                )


        # =================================================
        # BUILD AI INPUT
        # =================================================

        if previous_analysis:

            ai_result = f"""
User Request:

{message}


Previous Document Analysis:

{previous_analysis}
"""

        else:

            ai_result = f"""
User Request:

{message}

No previous document analysis is available.

Answer the user's request using the available
information only.
"""


        # =================================================
        # RUN LOCAL AI
        # =================================================

        result = run_safety_agent(

            industry=request.industry or "Industrial",

            filename=filename,

            ai_result=ai_result

        )


        # =================================================
        # SAVE RESULT
        # =================================================

        db.agent_results.insert_one(
            {
                "agent":
                    request.agent,

                "agent_id":
                    request.agent_id,

                "workspace_id":
                    request.workspace_id,

                "industry":
                    request.industry,

                "document_id":
                    request.document_id,

                "filename":
                    filename,

                "message":
                    message,

                "result":
                    result
            }
        )


        # =================================================
        # RETURN
        # =================================================

        return {

            "status":
                "completed",

            "agent":
                request.agent,

            "agent_id":
                request.agent_id,

            "industry":
                request.industry,

            "document_id":
                request.document_id,

            "response":
                result

        }


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )


# =====================================================
# SAFETY AGENT WITH DOCUMENT
# =====================================================

@router.post("/safety/{document_id}")
def safety_agent(
    document_id: str
):

    document = db.documents.find_one(
        {
            "id": document_id
        },
        {
            "_id": 0
        }
    )


    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )


    filename = document.get(
        "filename",
        "Unknown"
    )


    analysis = db.analyses.find_one(
        {
            "document_id": document_id
        },
        {
            "_id": 0
        }
    )


    if analysis is None:

        raise HTTPException(
            status_code=404,
            detail=(
                "AI analysis not found. "
                "Run AI analysis first."
            )
        )


    industry = analysis.get(
        "industry",
        "Industrial"
    )


    ai_result = analysis.get(
        "result",
        ""
    )


    if not ai_result:

        raise HTTPException(
            status_code=400,
            detail="AI analysis result is empty"
        )


    try:

        agent_result = run_safety_agent(

            industry=industry,

            filename=filename,

            ai_result=ai_result

        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


    db.agent_results.insert_one(
        {
            "document_id":
                document_id,

            "agent":
                "Safety Agent",

            "industry":
                industry,

            "filename":
                filename,

            "result":
                agent_result
        }
    )


    return {

        "status":
            "completed",

        "agent":
            "Safety Agent",

        "document_id":
            document_id,

        "industry":
            industry,

        "filename":
            filename,

        "result":
            agent_result,

        "response":
            agent_result

    }
