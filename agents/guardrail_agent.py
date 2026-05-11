"""
Guardrail Agent — validates a 1.4 submission meets minimum requirements.
Advisory only — never halts the grading pipeline.
"""

import json
import anthropic

MINIMUM_WORDS = 100


def validate(client: anthropic.Anthropic, submission_text: str, context: str) -> dict:
    word_count = len(submission_text.split())

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=500,
        system=f"""You are a submission pre-screening validator for an academic grading system.
Assess whether a student submission meets minimum requirements.

{context}""",
        messages=[{
            "role": "user",
            "content": f"""Validate this Assignment 1.4 submission. Respond ONLY with valid JSON.

Submission ({word_count} words):
---
{submission_text}
---

Check each:
1. RELEVANCE: Is this about fruit sorting/classification using Decision Tree or K-means?
2. METHOD_CHOSEN: Did the student clearly pick Decision Tree OR K-means? (not both, not neither)
3. HAS_STEPS: Does it describe a step-by-step process?
4. HAS_JUSTIFICATION: Does it explain why they chose their method?
5. INAPPROPRIATE_CONTENT: Any academic dishonesty indicators?

Return JSON exactly:
{{
  "is_relevant": true|false,
  "method_chosen": "decision_tree"|"k-means"|"both"|"none",
  "has_steps": true|false,
  "has_justification": true|false,
  "inappropriate_content": false,
  "passes_guardrails": true,
  "flag_for_human_review": true|false,
  "flag_reason": "string or null",
  "warnings": ["list of concerns, empty if none"]
}}

IMPORTANT: passes_guardrails is ALWAYS true — grading continues regardless of issues.
flag_for_human_review if: method is unclear, content seems off-topic, or integrity concern.""",
        }],
    )

    raw = response.content[0].text.strip()
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    result = json.loads(raw.strip())
    result["word_count"] = word_count
    return result
