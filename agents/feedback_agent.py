"""
Feedback Generator Agent — produces a motivational, personalized grade report
combining the score breakdown with constructive and encouraging commentary.
"""

import json
import anthropic


def generate_feedback(
    client: anthropic.Anthropic,
    submission_text: str,
    analysis: str,
    scores: dict,
    context: str,
) -> str:
    score_summary = "\n".join(
        f"  - {s['criterion_name']}: {s['points_awarded']}/{s['max_points']} "
        f"({s['level_awarded']}) — {s['rationale']}"
        for s in scores["scores"]
    )

    pct = round(scores["total_points"] / scores["total_possible"] * 100, 1)
    letter = _letter_grade(pct)

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=f"""You are an encouraging, constructive academic instructor grading
undergraduate student work. Your feedback should:
- Be warm, specific, and motivating
- Acknowledge genuine strengths before discussing areas for growth
- Give concrete, actionable suggestions (not vague advice)
- Use plain, approachable language
- Avoid condescension
- Be appropriate for an adult learner in a technology course

{context}""",
        messages=[
            {
                "role": "user",
                "content": f"""Write a grade report and motivational response for this student.

SCORE BREAKDOWN:
{score_summary}
Total: {scores['total_points']}/{scores['total_possible']} ({pct}% — {letter})

SUBMISSION ANALYSIS:
{analysis}

Write:
1. A brief opening that acknowledges their work positively
2. STRENGTHS: 2-3 specific things they did well (with examples from their work)
3. AREAS FOR GROWTH: 2-3 specific, actionable improvements
4. FINAL GRADE: {scores['total_points']}/{scores['total_possible']} ({pct}% — {letter})
5. A closing motivational sentence

Keep the full response under 400 words. Write in second person ("you", "your work").""",
            }
        ],
    )
    return response.content[0].text


def _letter_grade(pct: float) -> str:
    if pct >= 93: return "A"
    if pct >= 90: return "A-"
    if pct >= 87: return "B+"
    if pct >= 83: return "B"
    if pct >= 80: return "B-"
    if pct >= 77: return "C+"
    if pct >= 73: return "C"
    if pct >= 70: return "C-"
    if pct >= 67: return "D+"
    if pct >= 60: return "D"
    return "F"
