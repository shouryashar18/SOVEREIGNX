from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import db

import os
import requests
from uuid import uuid4
from datetime import datetime


router = APIRouter(
    prefix="/analysis",
    tags=["AI Analysis"]
)


# =====================================================
# CONFIG
# =====================================================

OLLAMA_URL = "http://127.0.0.1:11434"
MODEL_NAME = "llava:latest"

# Project root
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

STORAGE_DIR = os.path.join(
    BASE_DIR,
    "storage"
)

os.makedirs(
    STORAGE_DIR,
    exist_ok=True
)


# =====================================================
# REQUEST MODEL
# =====================================================

class AnalysisRequest(BaseModel):

    analysis_type: str = "general"


# =====================================================
# FIND DOCUMENT FILE
# =====================================================

def find_document_file(document):

    filename = document.get("filename")
    document_id = document.get("id")

    if not filename or not document_id:
        return None

    # -------------------------------------------------
    # 1. Stored path
    # -------------------------------------------------

    stored_path = document.get("file_path")

    if stored_path:

        # Convert Windows path to current OS path
        stored_path = stored_path.replace(
            "\\",
            os.sep
        )

        # Absolute path
        if os.path.isabs(stored_path):

            if os.path.exists(stored_path):
                return stored_path

        # Relative to project root
        possible = os.path.join(
            BASE_DIR,
            stored_path
        )

        if os.path.exists(possible):
            return possible

        # Relative to current directory
        if os.path.exists(stored_path):
            return os.path.abspath(
                stored_path
            )

    # -------------------------------------------------
    # 2. Standard storage path
    # -------------------------------------------------

    safe_filename = os.path.basename(
        filename
    )

    possible = os.path.join(
        STORAGE_DIR,
        f"{document_id}_{safe_filename}"
    )

    if os.path.exists(possible):
        return possible

    # -------------------------------------------------
    # 3. Search storage directory
    # -------------------------------------------------

    prefix = f"{document_id}_"

    if os.path.exists(STORAGE_DIR):

        for item in os.listdir(
            STORAGE_DIR
        ):

            if item.startswith(prefix):

                found = os.path.join(
                    STORAGE_DIR,
                    item
                )

                if os.path.isfile(found):
                    return found

    return None


# =====================================================
# ANALYZE WITH OLLAMA
# =====================================================

def run_ollama_analysis(
    file_path,
    filename,
    industry,
    analysis_type
):

    extension = os.path.splitext(
        filename
    )[1].lower()

    # -------------------------------------------------
    # IMAGE
    # -------------------------------------------------

    image_extensions = [
        ".png",
        ".jpg",
        ".jpeg",
        ".webp"
    ]

    if extension in image_extensions:

        import base64

        with open(
            file_path,
            "rb"
        ) as f:

            image_data = base64.b64encode(
                f.read()
            ).decode("utf-8")

        prompt = f"""
You are SovereignX, an offline industrial AI system.

Industry:
{industry}

Document:
{filename}

Analysis type:
{analysis_type}

Analyze the uploaded industrial image.

Provide:

1. Equipment/components identified
2. Technical observations
3. Safety concerns
4. Possible risks
5. Recommendations
6. Overall conclusion

Be specific and practical.
Do not invent information that is not visible.
"""

        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "images": [
                image_data
            ],
            "stream": False
        }

    # -------------------------------------------------
    # TEXT FILE
    # -------------------------------------------------

    elif extension in [
        ".txt",
        ".csv"
    ]:

        with open(
            file_path,
            "r",
            encoding="utf-8",
            errors="ignore"
        ) as f:

            text = f.read()

        prompt = f"""
You are SovereignX, an offline industrial AI.

Industry:
{industry}

Analysis type:
{analysis_type}

Analyze this document:

{text[:30000]}

Provide:
1. Summary
2. Technical findings
3. Safety risks
4. Concerns
5. Recommendations
6. Conclusion
"""

        payload = {
            "model": "qwen2.5:7b-instruct",
            "prompt": prompt,
            "stream": False
        }

    # -------------------------------------------------
    # OTHER FILES
    # -------------------------------------------------

    else:

        raise Exception(
            f"File type {extension} is not supported by the current local AI pipeline."
        )

    # -------------------------------------------------
    # CALL OLLAMA
    # -------------------------------------------------

    print("\n========================================")
    print("CALLING LOCAL OLLAMA")
    print("Model:", payload["model"])
    print("File:", filename)
    print("========================================")

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json=payload,
        timeout=600
    )

    if response.status_code != 200:

        raise Exception(
            f"Ollama error {response.status_code}: {response.text}"
        )

    result = response.json()

    return result.get(
        "response",
        ""
    )


# =====================================================
# START AI ANALYSIS
# =====================================================

@router.post("/{document_id}")
def start_analysis(
    document_id: str,
    request: AnalysisRequest
):

    print("\n========================================")
    print("SOVEREIGNX AI ANALYSIS STARTED")
    print("Document ID:", document_id)
    print("Analysis:", request.analysis_type)
    print("========================================")

    # -------------------------------------------------
    # GET DOCUMENT
    # -------------------------------------------------

    document = db.documents.find_one(
        {
            "id": document_id
        }
    )

    if document is None:

        raise HTTPException(
            status_code=404,
            detail="Document not found in database"
        )

    filename = document.get(
        "filename",
        "unknown"
    )

    # -------------------------------------------------
    # FIND FILE
    # -------------------------------------------------

    file_path = find_document_file(
        document
    )

    print("Resolved file path:", file_path)

    if file_path is None:

        raise HTTPException(
            status_code=404,
            detail=(
                f"Uploaded file not found. "
                f"Expected file for: {filename}"
            )
        )

    print("File exists:", os.path.exists(file_path))

    # -------------------------------------------------
    # WORKSPACE
    # -------------------------------------------------

    workspace = db.workspaces.find_one(
        {
            "id": document.get(
                "workspace_id"
            )
        }
    )

    industry = "General"

    if workspace:

        industry = workspace.get(
            "industry",
            "General"
        )

    # -------------------------------------------------
    # UPDATE STATUS
    # -------------------------------------------------

    db.documents.update_one(
        {
            "id": document_id
        },
        {
            "$set": {
                "status": "processing"
            }
        }
    )

    try:

        print("\nRunning local AI...")
        print("Industry:", industry)
        print("Analysis type:", request.analysis_type)

        result = run_ollama_analysis(
            file_path=file_path,
            filename=filename,
            industry=industry,
            analysis_type=request.analysis_type
        )

        # -------------------------------------------------
        # SAVE RESULT
        # -------------------------------------------------

        analysis_id = str(
            uuid4()
        )

        analysis_data = {

            "id": analysis_id,

            "document_id":
                document_id,

            "workspace_id":
                document.get(
                    "workspace_id"
                ),

            "analysis_type":
                request.analysis_type,

            "industry":
                industry,

            "model":
                MODEL_NAME,

            "result":
                result,

            "status":
                "completed",

            "created_at":
                datetime.utcnow()
        }

        db.analyses.insert_one(
            analysis_data
        )

        # -------------------------------------------------
        # UPDATE DOCUMENT
        # -------------------------------------------------

        db.documents.update_one(
            {
                "id": document_id
            },
            {
                "$set": {
                    "status": "analyzed"
                }
            }
        )

        print("\n========================================")
        print("AI ANALYSIS COMPLETED")
        print("Analysis ID:", analysis_id)
        print("========================================")

        return {

            "document_id":
                document_id,

            "analysis_id":
                analysis_id,

            "status":
                "completed",

            "analysis_type":
                request.analysis_type,

            "industry":
                industry,

            "model":
                MODEL_NAME,

            "result":
                result
        }

    except Exception as e:

        print("\n========================================")
        print("AI ANALYSIS FAILED")
        print(str(e))
        print("========================================")

        db.documents.update_one(
            {
                "id": document_id
            },
            {
                "$set": {
                    "status":
                        "analysis_failed"
                }
            }
        )

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =====================================================
# GET ANALYSIS RESULT
# =====================================================

@router.get("/{document_id}")
def get_analysis(
    document_id: str
):

    analyses = list(
        db.analyses.find(
            {
                "document_id":
                    document_id
            },
            {
                "_id": 0
            }
        ).sort(
            "created_at",
            -1
        )
    )

    if not analyses:

        return {

            "document_id":
                document_id,

            "status":
                "processing",

            "analyses":
                []
        }

    return {

        "document_id":
            document_id,

        "status":
            "completed",

        "analyses":
            analyses
    }