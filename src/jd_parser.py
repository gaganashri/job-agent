
from openai import OpenAI
from src.config import OPENAI_API_KEY, BASE_URL

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=BASE_URL
)


PROMPT = """
You are a highly accurate job description parser.

Extract the following details from the JD and return strictly in JSON format:
{{
  "title": "",
  "seniority": "",
  "skills": [],
  "summary": ""
}}

INSTRUCTIONS:
- seniority must be one of: junior, mid, senior, lead, unknown
- skills must be 5 to 15 key technical skills only
- summary must be 1–2 sentences describing the job

JOB DESCRIPTION:
\"\"\"{jd}\"\"\"
"""

def parse_jd(jd_text):
    prompt = PROMPT.format(jd=jd_text)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            max_tokens=300
        )

        content = response.choices[0].message.content

        import json, re
        match = re.search(r"\{.*\}", content, re.S)
        if match:
            return json.loads(match.group(0))

        return {"error": "JSON not found", "raw": content}

    except Exception as e:
        return {"error": str(e)}

# ---------------- TEST BLOCK ----------------
if __name__ == "__main__":
    print("Running JD parser test...\n")

    example_jd = """
We need an AI Engineer skilled in Python, ML, LLMs, embeddings, and cloud deployment.
"""

    result = parse_jd(example_jd)
    print("Parsed Output:\n", result)
