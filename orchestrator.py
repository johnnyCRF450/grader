"""
Orchestrator — coordinates the 4-agent grading pipeline and returns
a complete GradeReport for a single student submission.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import anthropic

from agents.context_agent import build_context, get_rubric
from agents.analyzer_agent import analyze_submission
from agents.scorer_agent import score_submission
from agents.feedback_agent import generate_feedback


RUBRIC_PATH = Path(__file__).parent / "rubric.json"


@dataclass
class GradeReport:
    student_label: str
    analysis: str
    scores: dict
    feedback: str

    @property
    def total_points(self) -> int:
        return self.scores["total_points"]

    @property
    def total_possible(self) -> int:
        return self.scores["total_possible"]

    @property
    def percentage(self) -> float:
        return round(self.total_points / self.total_possible * 100, 1)

    def to_dict(self) -> dict:
        return {
            "student": self.student_label,
            "total_points": self.total_points,
            "total_possible": self.total_possible,
            "percentage": self.percentage,
            "score_breakdown": self.scores["scores"],
            "feedback": self.feedback,
        }

    def summary(self) -> str:
        lines = [
            f"Student: {self.student_label}",
            f"Grade: {self.total_points}/{self.total_possible} ({self.percentage}%)",
            "",
            "Score Breakdown:",
        ]
        for s in self.scores["scores"]:
            lines.append(
                f"  {s['criterion_name']}: {s['points_awarded']}/{s['max_points']} ({s['level_awarded']})"
            )
        lines += ["", "--- FEEDBACK ---", self.feedback]
        return "\n".join(lines)


def grade(submission_text: str, student_label: str = "Student") -> GradeReport:
    client = anthropic.Anthropic()
    rubric = get_rubric(RUBRIC_PATH)
    context = build_context(RUBRIC_PATH)

    print(f"[1/4] Analyzing submission...")
    analysis = analyze_submission(client, submission_text, context)

    print(f"[2/4] Scoring against rubric...")
    scores = score_submission(client, analysis, submission_text, context, rubric)

    print(f"[3/4] Generating feedback...")
    feedback = generate_feedback(client, submission_text, analysis, scores, context)

    print(f"[4/4] Done.")
    return GradeReport(
        student_label=student_label,
        analysis=analysis,
        scores=scores,
        feedback=feedback,
    )
