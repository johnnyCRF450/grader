"""
Gradio web UI — paste a student submission, get back grade + feedback.
Run: python app.py
"""

import json
import csv
import os
from datetime import datetime
from pathlib import Path

import gradio as gr

from orchestrator import grade

LOG_PATH = Path(__file__).parent / "grades_log.csv"


def _ensure_log():
    if not LOG_PATH.exists():
        with open(LOG_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp", "student", "total_points", "total_possible",
                "percentage", "feedback"
            ])


def run_grader(submission_text: str, student_name: str) -> tuple[str, str]:
    if not submission_text.strip():
        return "Please paste a submission before grading.", ""

    label = student_name.strip() or "Student"

    try:
        report = grade(submission_text, student_label=label)
    except Exception as e:
        return f"Error during grading: {e}", ""

    # Log to CSV
    _ensure_log()
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().isoformat(),
            label,
            report.total_points,
            report.total_possible,
            report.percentage,
            report.feedback.replace("\n", " "),
        ])

    breakdown = "\n".join(
        f"{s['criterion_name']}: {s['points_awarded']}/{s['max_points']} — {s['level_awarded']}\n  {s['rationale']}"
        for s in report.scores["scores"]
    )
    score_display = (
        f"TOTAL: {report.total_points}/{report.total_possible} ({report.percentage}%)\n\n"
        f"Breakdown:\n{breakdown}"
    )

    return score_display, report.feedback


with gr.Blocks(title="Assignment 1.4 Grader") as demo:
    gr.Markdown("## Assignment 1.4 — Fruit Classification Grader")
    gr.Markdown(
        "Paste a student's submission below. The system will analyze it against "
        "the rubric and generate a score breakdown and motivational feedback."
    )

    with gr.Row():
        student_name = gr.Textbox(label="Student Name / ID", placeholder="e.g. Jane Smith")

    submission = gr.Textbox(
        label="Student Submission (paste full text here)",
        lines=20,
        placeholder="Paste the student's written submission here...",
    )

    grade_btn = gr.Button("Grade Submission", variant="primary")

    with gr.Row():
        score_out = gr.Textbox(label="Score Breakdown", lines=12, interactive=False)
        feedback_out = gr.Textbox(label="Feedback & Motivational Response", lines=12, interactive=False)

    grade_btn.click(
        fn=run_grader,
        inputs=[submission, student_name],
        outputs=[score_out, feedback_out],
    )

    gr.Markdown(f"*Grades are automatically logged to `grades_log.csv`.*")


if __name__ == "__main__":
    demo.launch()
