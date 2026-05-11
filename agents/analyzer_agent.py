"""
Analyzer Agent — extracts structured elements from a 1.4 submission.
Supports text + multiple embedded images (diagrams, visual aids).
"""

import anthropic

MAX_IMAGES = 10


def analyze(
    client: anthropic.Anthropic,
    submission_text: str,
    context: str,
    images: list[str] | None = None,
) -> str:
    images = images or []
    has_images = len(images) > 0

    content = []
    for img_b64 in images[:MAX_IMAGES]:
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/png", "data": img_b64},
        })

    image_instruction = ""
    if has_images:
        image_instruction = f"""
You have {len(images)} image(s) extracted from the student's document.
For each image: read all visible text, describe any diagrams or flowcharts,
identify decision trees or cluster diagrams if present.
"""

    content.append({
        "type": "text",
        "text": f"""Analyze this Assignment 1.4 submission completely. Do not skip any section.
{image_instruction}
Extracted document text:
---
{submission_text if submission_text.strip() else "[No text — evaluate from images only]"}
---

Extract and label ALL sections:

1. METHOD_CHOSEN
   Which method did the student select: Decision Tree or K-means Clustering?
   Quote the exact statement where they chose it.

2. DATASET_UNDERSTANDING
   What characteristics/attributes of the Fruits dataset did the student identify?
   (Look for: classes, colors, shapes, textures, sizes, image counts, splits.)
   Note any gaps or inaccuracies versus the reference dataset.

3. STEP_BY_STEP_PROCESS
   List every step the student described for their chosen method, in order.
   Note whether steps are clear, logically ordered, and complete.

4. DECISION_POINTS
   What key logical decision points or criteria did the student include?
   (For Decision Tree: branching conditions. For K-means: convergence criteria, centroid logic.)

5. HOW_STEPS_LEAD_TO_CLASSIFICATION
   Did the student explain how each step leads to the final classification outcome?

6. METHOD_JUSTIFICATION
   What reasons did the student give for choosing their method?
   Did they connect it to the dataset's specific characteristics?

7. VISUAL_ELEMENTS
   Describe any diagrams, flowcharts, or visual aids (from images or described in text).

8. TEXT_IN_IMAGES
   List all text extracted from any images (labels, headings, step descriptions).

9. MISSING_ELEMENTS
   What required assignment elements are absent or underdeveloped?

10. ACCURACY_ISSUES
    Note any factual errors about the dataset or method descriptions.
    (e.g., wrong class names, incorrect algorithm behavior described)""",
    })

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=f"""You are an academic submission analyzer. Extract information objectively and completely.
Do not score — only identify what is present, absent, and inaccurate.

{context}""",
        messages=[{"role": "user", "content": content}],
    )
    return response.content[0].text
