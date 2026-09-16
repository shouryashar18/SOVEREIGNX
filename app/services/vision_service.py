import os
import ollama


def analyze_image(
    image_path: str,
    industry: str = "mechanical",
    user_prompt: str = ""
) -> dict:
    """
    Analyze industrial diagrams/equipment images
    using the local LLaVA model through Ollama.
    """

    if not os.path.exists(image_path):
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    prompt = f"""
You are an industrial vision inspection agent
running inside a private ON-PREMISE AI Workbench.

Industry: {industry}

Analyze the uploaded industrial diagram,
P&ID, schematic, or equipment image.

Identify:

1. Equipment identifiers
2. Component identifiers
3. Gauge readings
4. Visible defects or abnormalities
5. Connections and flow information
6. Potential technical risks
7. Potential safety concerns

User instruction:
{user_prompt}

Do not invent information that is not visible
in the image.

Return a clear technical analysis.
"""

    try:
        response = ollama.generate(
            model="llava:latest",
         prompt=prompt,
         images=[os.path.abspath(image_path)],
         options={
        "num_predict": 150
    }
)

        return {
            "model_used": "llava:latest",
            "industry": industry,
            "task": "Industrial Vision Inspection",
            "result": response["response"]
        }

    except Exception as e:
        raise RuntimeError(
            f"Local LLaVA analysis failed: {str(e)}"
        )