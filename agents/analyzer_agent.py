"""
Submission Analyzer Agent — reads the student's raw submission text and
extracts structured key elements for downstream scoring.
"""

import anthropic
from .context_agent import build_context
from pathlib import Path


def analyze_submission(client: anthropic.Anthropic, submission_text: str, context: str) -> str:
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=f"""You are an academic submission analyzer. Your job is to read a student's
submission and extract the key elements present. Be objective and factual.

{context}""",
        messages=[
            {
                "role": "user",
                "content": f"""Analyze this student submission and extract the following elements.
For each element, quote or summarize what the student wrote.

Student Submission:
---
{submission_text}
---

Extract:
1. DATASET_UNDERSTANDING: What characteristics/attributes of the dataset did the student identify?
2. METHOD_CHOSEN: Which method did the student choose (Decision Tree or K-means)?
3. METHOD_STEPS: What step-by-step process did the student describe?
4. DECISION_POINTS: What decision criteria or logical branch points did they explain?
5. METHOD_JUSTIFICATION: What reasoning did they give for choosing their method?
6. MISSING_ELEMENTS: What required elements appear absent or very weak?

Format your response with these exact headers.""",
            }
        ],
    )
    return response.content[0].text
