"""
Context Agent — loads assignment background, dataset info, and rubric into
a shared context string that all other agents receive in their system prompts.
"""

import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from dataset_context import get_dataset_context_string


ASSIGNMENT_INSTRUCTIONS = """
ASSIGNMENT 1.4 — Fruit Sorting / Classification (Indiana Wesleyan University)

Learning Objective:
Students select ONE classification method (Decision Tree OR K-means Clustering)
and document the THEORETICAL process for applying it to the Fruits Classification
dataset. No actual coding or manual sorting is required — only a written,
step-by-step theoretical description.

CRITICAL GRADING NOTE: Because this is a theoretical assignment, rubric criteria
for "Implementation Process" should assess the quality of the WRITTEN description
of how the method would be implemented — including parameter choices, preprocessing
decisions, and potential challenges — not actual code or computed output.
"Results and Outcomes" should assess the student's description of EXPECTED or
PREDICTED outcomes and their ability to reason about what the method would produce.

Required elements:
1. Dataset Understanding — identify characteristics/attributes of the dataset
   (classes: Apple, Banana, Grape, Mango, Strawberry; visual attributes: color,
   shape, texture, size; image format: 225x225 RGB JPEG, 2000 images/class)
2. Method Documentation — step-by-step description of how Decision Tree or
   K-means Clustering WOULD sort/classify the fruits, including:
     - Each step from start to finish
     - Key decision points or criteria
     - How each step leads to the final classification
3. Method Justification — explain WHY the chosen method suits this dataset
4. Instructions Quality — written in plain English, followable by others
5. Documentation and Presentation — organized, professional, clear writing
"""


def build_context(rubric_path: Path) -> str:
    rubric = json.loads(rubric_path.read_text())
    criteria_text = []
    for c in rubric["criteria"]:
        levels = " | ".join(
            f"{lvl} ({data['points']}pts): {data['description']}"
            for lvl, data in c["levels"].items()
        )
        criteria_text.append(
            f"  [{c['name']} — max {c['max_points']} pts]\n    {levels}"
        )

    return f"""
=== ASSIGNMENT CONTEXT ===
{ASSIGNMENT_INSTRUCTIONS}

=== DATASET REFERENCE ===
{get_dataset_context_string()}

=== GRADING RUBRIC ===
Assignment: {rubric['assignment']}
Total points: {rubric['total_points']}

Criteria:
{chr(10).join(criteria_text)}
"""


def get_rubric(rubric_path: Path) -> dict:
    return json.loads(rubric_path.read_text())
