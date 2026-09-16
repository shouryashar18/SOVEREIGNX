from app.services.ollama_service import ask_ollama


def run_safety_agent(
    industry: str,
    filename: str,
    ai_result: str
):

    prompt = f"""
You are the SovereignX Industrial Safety Agent.

Industry:
{industry}

Document:
{filename}

Existing AI Analysis:
{ai_result}

Analyze the information and return a structured safety assessment.

Return exactly in this format:

RISK LEVEL:
Low / Medium / High / Critical

HAZARDS:
- hazard 1
- hazard 2

SAFETY CONCERNS:
- concern 1
- concern 2

RECOMMENDATIONS:
- recommendation 1
- recommendation 2

SUMMARY:
Short technical summary.
"""

    result = ask_ollama(prompt)

    return result