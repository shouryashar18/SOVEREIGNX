import os

from app.services.document_parser import read_file_content
from app.services.ai_service import analyze_document
from app.services.vision_service import analyze_image


IMAGE_EXTENSIONS = [".jpg", ".jpeg", ".png", ".bmp"]
DOCUMENT_EXTENSIONS = [".txt", ".docx", ".pdf"]


def analyze_file(
    file_path: str,
    industry: str = "mechanical",
    source_file: str = ""
) -> dict:

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"File not found: {file_path}"
        )

    extension = os.path.splitext(file_path)[1].lower()

    if not source_file:
        source_file = os.path.basename(file_path)

    if extension in IMAGE_EXTENSIONS:

        vision_result = analyze_image(
            image_path=file_path,
            industry=industry,
            user_prompt=(
                f"Inspect this industrial image for "
                f"{industry} related technical and safety issues."
            )
        )

        return {
            "status": "completed",
            "pipeline": "vision",
            "industry": industry,
            "source_file": source_file,
            "model_used": "llava:latest",
            "result": vision_result["result"]
        }

    if extension in DOCUMENT_EXTENSIONS:

        document_text = read_file_content(file_path)

        if not document_text:
            raise ValueError(
                "The uploaded document contains no readable text."
            )

        ai_result = analyze_document(
            document_text=document_text,
            industry=industry,
            source_file=source_file
        )

        return {
            "status": "completed",
            "pipeline": "document_reasoning",
            "industry": industry,
            "source_file": source_file,
            "model_used": "qwen2.5:7b-instruct",
            "result": ai_result
        }

    raise ValueError(
        f"Unsupported file type: {extension}"
    )