import requests


OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL_NAME = "llava:latest"


def run_safety_agent(
    industry: str,
    filename: str,
    ai_result: str
):

    prompt = f"""
You are SovereignX Industrial Safety AI Agent.

Industry:
{industry}

Document:
{filename}

Previous AI Analysis:
{ai_result}

Based on the above analysis, perform a detailed industrial safety assessment.

Return the result in this structure:

1. SAFETY SUMMARY
2. IDENTIFIED HAZARDS
3. RISK LEVEL
4. POSSIBLE FAILURE POINTS
5. SAFETY CONCERNS
6. RECOMMENDED ACTIONS
7. PREVENTIVE MEASURES
8. FINAL SAFETY ASSESSMENT

Be technical, clear and concise.
Do not invent information that is not supported by the provided analysis.
"""


    try:

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )


        if response.status_code != 200:

            raise Exception(
                f"Ollama returned HTTP {response.status_code}: "
                f"{response.text}"
            )


        data = response.json()


        result = data.get(
            "response",
            ""
        )


        if not result:

            raise Exception(
                "Ollama returned an empty response"
            )


        return result


    except requests.exceptions.ConnectionError:

        raise Exception(
            "Ollama is not running. "
            "Start Ollama using: ollama serve"
        )


    except requests.exceptions.Timeout:

        raise Exception(
            "Ollama request timed out."
        )


    except Exception as e:

        raise Exception(
            f"AI Agent failed: {str(e)}"
        )