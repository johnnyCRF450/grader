"""
Rubric Scorer Agent — scores each rubric criterion based on the analyzer's
output and returns a structured score breakdown with justification.
"""

import json
import anthropic


def score_submission(
    client: anthropic.Anthropic,
    analysis: str,
    submission_text: str,
    context: str,
    rubric: dict,
) -> dict:
    criteria_json = json.dumps(rubric["criteria"], indent=2)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=f"""You are a fair and rigorous academic grader. Score student submissions
against the rubric criteria provided. Be consistent, specific, and cite evidence
from the submission to support each score.

{context}""",
        messages=[
            {
                "role": "user",
                "content": f"""Score this student submission against each rubric criterion.

SUBMISSION ANALYSIS:
{analysis}

ORIGINAL SUBMISSION (for reference):
---
{submission_text}
---

RUBRIC CRITERIA (JSON):
{criteria_json}

For each criterion, respond with EXACTLY this JSON structure:
{{
  "scores": [
    {{
      "criterion_id": "<id>",
      "criterion_name": "<name>",
      "level_awarded": "<excellent|competent|needs_improvement|inadequate>",
      "points_awarded": <number — must match the points value for the awarded level>,
      "max_points": <number>,
      "evidence": "<direct quote or specific reference from the submission supporting this score>",
      "rationale": "<1-2 sentences explaining why this level was awarded, not a higher or lower one>"
    }}
  ],
  "total_points": <sum of all points_awarded>,
  "total_possible": {rubric['total_points']}
}}

Scoring rules:
- Use ONLY the four levels defined: excellent, competent, needs_improvement, inadequate
- Points MUST be the exact value defined in the rubric for that level (e.g., inadequate for a 10-pt criterion = 6, not 0)
- This is a THEORETICAL assignment — students describe what WOULD happen, not actual results
- For "Results and Outcomes": credit students for describing expected/predicted outcomes, not requiring actual computed metrics
- Return ONLY valid JSON, no other text.""",
            }
        ],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())
