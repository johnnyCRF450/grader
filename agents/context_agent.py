"""
Context Agent — assembles the shared context string for Assignment 1.4.
"""

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from dataset_context import get_dataset_context_string

ASSIGNMENT_INSTRUCTIONS = """
ASSIGNMENT 1.4 — Fruit Sorting / Classification (Indiana Wesleyan University)

TASK:
Students select ONE classification method (Decision Tree OR K-means Clustering)
and document the THEORETICAL process for applying it to the Fruits Classification
dataset. No actual coding or manual sorting is required — only a written,
step-by-step theoretical description in plain English.

Required elements:
1. Dataset Understanding — identify characteristics/attributes of the dataset
   (classes: Apple, Banana, Grape, Mango, Strawberry; visual attributes: color,
   shape, texture, size; image format: 225×225 RGB JPEG, 2000 images/class)
2. Method Documentation — step-by-step description of how the chosen method
   WOULD sort/classify the fruits, including:
     - Each step from start to finish
     - Key decision points or criteria
     - How each step leads to the final classification
3. Method Justification — explain WHY the chosen method suits this dataset
4. Instructions Quality — written in plain English, followable by others
5. Documentation and Presentation — organized, professional, clear writing

CRITICAL GRADING NOTE: This is a THEORETICAL assignment. "Implementation Process"
should assess the quality of the WRITTEN description — not actual code or output.
"Results and Outcomes" should assess the student's description of EXPECTED outcomes.
"""


def build_context(rubric_path: Path) -> str:
    rubric = json.loads(rubric_path.read_text())
    criteria_text = []
    for c in rubric["criteria"]:
        levels = " | ".join(
            f"{lvl} ({data['points']}pts)"
            for lvl, data in c["levels"].items()
        )
        criteria_text.append(f"  [{c['name']} — max {c['max_points']} pts]: {levels}")

    return f"""
=== ASSIGNMENT CONTEXT ===
{ASSIGNMENT_INSTRUCTIONS}

=== GRADING RUBRIC ===
Assignment: {rubric['assignment']}
Total points: {rubric['total_points']}
Note: {rubric.get('grading_note','')}

Criteria:
{chr(10).join(criteria_text)}

=== DATASET REFERENCE ===
{get_dataset_context_string()}
"""


def get_rubric(rubric_path: Path) -> dict:
    return json.loads(rubric_path.read_text())
