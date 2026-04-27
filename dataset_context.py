"""
Dataset knowledge base for Fruits Classification (Kaggle).
Loaded into a DataFrame and used as reference context by all agents.
"""

import pandas as pd

DATASET_META = {
    "name": "Fruits Classification Dataset",
    "source": "Kaggle — utkarshsaxenadn/fruits-classification",
    "classes": ["Apple", "Banana", "Grape", "Mango", "Strawberry"],
    "n_classes": 5,
    "total_images": 10000,
    "images_per_class": 2000,
    "train_images": 9700,   # 97% — 1940 per class
    "valid_images": 200,    # 2%  — 40 per class
    "test_images": 100,     # 1%  — 20 per class
    "image_size_px": "225x225",
    "image_format": "JPEG",
    "color_mode": "RGB",
    "folder_structure": "train/<class>/, valid/<class>/, test/<class>/",
    "task_type": "Multi-class image classification",
    "kaggle_url": "https://www.kaggle.com/datasets/utkarshsaxenadn/fruits-classification",
}

# Visual/perceptual characteristics per fruit class
# Color averages derived from actual pixel analysis of the downloaded dataset
CLASS_CHARACTERISTICS = pd.DataFrame([
    {
        "fruit": "Apple",
        "dominant_colors": "Red, Green",
        "shape": "Round",
        "surface_texture": "Smooth skin",
        "avg_rgb": "(141, 94, 79)",
        "visual_notes": "High red channel in ripe specimens; can be green when unripe",
        "distinguishing_features": "Round shape, red/green coloring, stem visible in some images",
    },
    {
        "fruit": "Banana",
        "dominant_colors": "Yellow",
        "shape": "Elongated, curved",
        "surface_texture": "Smooth skin",
        "avg_rgb": "(172, 137, 98)",
        "visual_notes": "Green when unripe, yellow when ripe; very distinctive elongated curve",
        "distinguishing_features": "Long curved shape, yellow coloring, often shown in bunches",
    },
    {
        "fruit": "Grape",
        "dominant_colors": "Purple, Green",
        "shape": "Small, round clusters",
        "surface_texture": "Smooth, waxy skin",
        "avg_rgb": "(155, 159, 168)",
        "visual_notes": "High blue channel; distinctive purple/blue-green hues; appears in bunches",
        "distinguishing_features": "Cluster arrangement, small round shape, purple or green color",
    },
    {
        "fruit": "Mango",
        "dominant_colors": "Yellow-Orange",
        "shape": "Oval/oblong",
        "surface_texture": "Smooth skin",
        "avg_rgb": "(156, 137, 88)",
        "visual_notes": "High red+green channels creating orange-yellow appearance",
        "distinguishing_features": "Oval shape, yellow-orange gradient coloring, smooth surface",
    },
    {
        "fruit": "Strawberry",
        "dominant_colors": "Red",
        "shape": "Heart/conical",
        "surface_texture": "Seeded surface with leafy green crown",
        "avg_rgb": "(124, 108, 60)",
        "visual_notes": "Very high red channel; distinctive seed-dotted texture and green leafy top",
        "distinguishing_features": "Conical/heart shape, red with yellow seeds, green crown",
    },
])

CLASS_CHARACTERISTICS = CLASS_CHARACTERISTICS.set_index("fruit")


def get_dataset_context_string() -> str:
    """Returns a formatted string summary of the dataset for LLM prompts."""
    lines = [
        f"Dataset: {DATASET_META['name']}",
        f"Source: {DATASET_META['source']}",
        f"Task: {DATASET_META['task_type']}",
        f"Classes ({DATASET_META['n_classes']}): {', '.join(DATASET_META['classes'])}",
        f"Total images: {DATASET_META['total_images']} ({DATASET_META['images_per_class']} per class)",
        f"Splits: Train={DATASET_META['train_images']}, Valid={DATASET_META['valid_images']}, Test={DATASET_META['test_images']}",
        f"Image size: {DATASET_META['image_size_px']} pixels, {DATASET_META['color_mode']} {DATASET_META['image_format']}",
        f"Folder structure: {DATASET_META['folder_structure']}",
        "",
        "Class characteristics:",
    ]
    for fruit, row in CLASS_CHARACTERISTICS.iterrows():
        lines.append(
            f"  {fruit}: {row['dominant_colors']} | {row['shape']} | {row['surface_texture']} | {row['distinguishing_features']}"
        )
    return "\n".join(lines)


if __name__ == "__main__":
    print(get_dataset_context_string())
    print()
    print(CLASS_CHARACTERISTICS.to_string())
