from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


llm = ChatOllama(
    model="qwen2.5:7b-instruct",
    temperature=0.1,
    num_predict=150
)


def analyze_document(
    document_text: str,
    industry: str,
    source_file: str = ""
):

    prompt = f"""
You are an industrial AI analysis engine for a private
on-premise industrial AI workbench.

Industry: {industry}
Source File: {source_file}

Analyze the following industrial document:

{document_text}

Return:

risk_score: <number 0-100>
severity: <LOW/MEDIUM/HIGH/CRITICAL>
primary_component: <component>
key_finding: <short finding>
recommended_action: <short action>

Keep the response very concise.
Maximum 100 words.
Return only these 5 fields.
Do not provide explanations or detailed reasoning.
"""

    response = llm.invoke([
        HumanMessage(content=prompt)
    ])

    return response.content