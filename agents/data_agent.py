
import json
from groq import Groq

SYSTEM_PROMPT = """
You are the planning component of a data analysis agent.
Given a user question and dataset columns, return ONLY valid JSON with:
{
  "intent": "total|average|max|sum_by|count_by|trend",
  "metric": "column name or null",
  "group_by": "column name or null",
  "date_column": "column name or null"
}
Choose only columns that exist in the provided list. Do not calculate values.
"""

def create_analysis_plan(question, columns, api_key):
    client = Groq(api_key=api_key)
    prompt = f"Dataset columns: {columns}\nQuestion: {question}"
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        temperature=0,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    content = response.choices[0].message.content.strip()
    content = content.replace("```json", "").replace("```", "").strip()
    return json.loads(content)
