import os
import time
import random
import json
import subprocess
import sys
from pathlib import Path
from typing import Iterable
from dotenv import load_dotenv
from google import genai
from google.genai import types
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

load_dotenv()

# Configuration
MODEL_ID = "gemini-2.5-flash"
PROMPT_PATH = Path("prompts/site_parsing.md")
OUTPUT_PATH = Path("sample_output.json")

# Client Setup
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
MAX_RETRIES = 3


def normalize_lot_boundary(lot_boundary):
    if lot_boundary is None:
        return None

    if not isinstance(lot_boundary, Iterable) or isinstance(lot_boundary, (str, bytes)):
        raise ValueError("lot_boundary must be a list-like collection of [y, x] points")

    normalized = []
    for idx, point in enumerate(lot_boundary):
        if not isinstance(point, Iterable) or isinstance(point, (str, bytes)):
            raise ValueError(f"lot_boundary point {idx} must be [y, x]")

        values = list(point)
        if len(values) != 2:
            raise ValueError(f"lot_boundary point {idx} must contain exactly 2 values: [y, x]")

        y, x = values
        if not isinstance(y, (int, float)) or not isinstance(x, (int, float)):
            raise ValueError(f"lot_boundary point {idx} must contain numeric [y, x] values")

        if not (0 <= y <= 1000 and 0 <= x <= 1000):
            raise ValueError(
                f"lot_boundary point {idx} is out of normalized range 0-1000: {values}"
            )

        normalized.append([int(round(y)), int(round(x))])

    if len(normalized) < 3:
        raise ValueError("lot_boundary must have at least 3 points")

    return normalized


def build_runtime_site_context(site_width_ft=None, site_height_ft=None, lot_boundary=None):
    if site_width_ft is None and site_height_ft is None and lot_boundary is None:
        return None

    site_scale = {
        "site_width_ft": site_width_ft,
        "site_height_ft": site_height_ft,
        "normalized_canvas": [0, 0, 1000, 1000],
        "lot_boundary": lot_boundary,
        "scale_note": (
            "All placements must fall within lot_boundary. Bounding boxes define placement. "
            "Real-world dimensions define scale."
        ),
    }

    return (
        "\nRuntime site context for this request (authoritative):\n"
        "Use the following site_scale values exactly.\n\n"
        "```json\n"
        f"{json.dumps(site_scale, indent=2)}\n"
        "```\n"
    )

def visualize_output(site_data):

    terrain_colors = {
    "grass": "#7fbf7f",
    "pavement": "#bdbdbd",
    "asphalt": "#8c8c8c"
    }

    prefab_colors = {
        "oak_tree": "#2e8b57",
        "wooden_bench": "#8b5a2b"
    }

    default_terrain_color = "#cccccc"
    default_prefab_color = "#4f81bd"

    # -----------------------------
    # Styling helpers
    # -----------------------------
    terrain_colors = {
        "grass": "#7fbf7f",
        "pavement": "#bdbdbd",
        "asphalt": "#8c8c8c"
    }

    prefab_colors = {
        "oak_tree": "#2e8b57",
        "wooden_bench": "#8b5a2b"
    }

    default_terrain_color = "#cccccc"
    default_prefab_color = "#4f81bd"

    # -----------------------------
    # Figure setup
    # -----------------------------
    canvas = site_data["site_scale"]["normalized_canvas"]
    x_min, y_min, x_max, y_max = canvas

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal")

    # Optional: invert Y so it feels more like screen / layout coordinates
    ax.invert_yaxis()

    # -----------------------------
    # Draw terrain zones
    # -----------------------------
    for zone in site_data["terrain_zones"]:
        x1, y1, x2, y2 = zone["bounding_box"]
        width = x2 - x1
        height = y2 - y1
        color = terrain_colors.get(zone["terrain_type"], default_terrain_color)

        rect = Rectangle(
            (x1, y1),
            width,
            height,
            facecolor=color,
            edgecolor="black",
            linewidth=1,
            alpha=0.6
        )
        ax.add_patch(rect)

        cx = x1 + width / 2
        cy = y1 + height / 2
        ax.text(
            cx,
            cy,
            f'{zone["area_name"]}\n({zone["terrain_type"]})',
            ha="center",
            va="center",
            fontsize=9,
            color="black"
        )

    # -----------------------------
    # Draw generated objects (buildings)
    # -----------------------------
    for obj in site_data["generated_objects"]:
        x1, y1, x2, y2 = obj["bounding_box"]
        width = x2 - x1
        height = y2 - y1

        rect = Rectangle(
            (x1, y1),
            width,
            height,
            facecolor="orange",
            edgecolor="darkred",
            linewidth=2,
            alpha=0.7
        )
        ax.add_patch(rect)

        cx, cy = obj["center_point"]
        ax.text(
            cx,
            cy,
            f'{obj["area_name"]}\n({obj["object_type"]})',
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color="black"
        )

    # -----------------------------
    # Draw prefab instances as circles
    # -----------------------------
    for prefab in site_data["prefab_instances"]:
        cx, cy = prefab["center_point"]
        x1, y1, x2, y2 = prefab["footprint_box"]

        # Radius based on footprint size
        radius = max(x2 - x1, y2 - y1) * 0.18 * prefab.get("scale_multiplier", 1.0)
        color = prefab_colors.get(prefab["prefab_type"], default_prefab_color)

        circle = Circle(
            (cx, cy),
            radius=radius,
            facecolor=color,
            edgecolor="black",
            linewidth=1.5,
            alpha=0.9
        )
        ax.add_patch(circle)

        ax.text(
            cx,
            cy,
            f'{prefab["area_name"]}\n({prefab["prefab_type"]})',
            ha="center",
            va="center",
            fontsize=8,
            color="white"
        )

    # -----------------------------
    # Final plot formatting
    # -----------------------------
    ax.set_title("Site Layout Visualization", fontsize=14, pad=12)
    ax.set_xlabel("Normalized X")
    ax.set_ylabel("Normalized Y")
    ax.grid(True, linestyle="--", alpha=0.3)

    plt.tight_layout()
    plt.show()


def process_sketch(
    lot_boundary=None,
    site_width_ft=None,
    site_height_ft=None,
    sketch_path=None,
    prompt_path=PROMPT_PATH,
    output_path=OUTPUT_PATH,
):

    if sketch_path is None:
        print("No sketch path was provided")
        return

    sketch_path = Path(sketch_path)
    prompt_path = Path(prompt_path)
    output_path = Path(output_path)

    if not sketch_path.exists():
        print(f"{sketch_path} does not exist")
        return
    
    if not prompt_path.exists():
        print(f"{prompt_path} does not exist")
        return

    try:
        normalized_boundary = normalize_lot_boundary(lot_boundary)
    except ValueError as exc:
        print(f"Invalid lot boundary: {exc}")
        return

    runtime_context = build_runtime_site_context(
        site_width_ft=site_width_ft,
        site_height_ft=site_height_ft,
        lot_boundary=normalized_boundary,
    )

    output = None

    for attempt in range(MAX_RETRIES):
        try:
            print(f"🔄 [Processing {sketch_path} (Attempt {attempt+1})...")
            
            prompt_text = prompt_path.read_text(encoding="utf-8")
            image_bytes = sketch_path.read_bytes()

            contents = [prompt_text]
            if runtime_context:
                contents.append(runtime_context)
            contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))

            response = client.models.generate_content(
                model=MODEL_ID,
                contents=contents,
            )
            output = response.text
            output_path.write_text(output, encoding="utf-8")
            print(f"Success: {output_path.name}")
            if normalized_boundary is not None:
                print(f"Applied lot boundary with {len(normalized_boundary)} points")
            break

        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "503" in err_msg:
                # If we hit a wall, wait a full minute + jitter
                wait = 60 + random.uniform(5, 15)
                print(f"🚨 API Overloaded. Sleeping {wait:.1f}s before retry...")
                time.sleep(wait)
            else:
                print(f"❌ Permanent Error: {e}")
                break

    return output


def choose_sketch_path():
    try:
        import tkinter as tk
        from tkinter import filedialog

        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)

        selected_path = filedialog.askopenfilename(
            title="Select a sketch image",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("All files", "*.*"),
            ],
        )

        root.destroy()
        if selected_path:
            return Path(selected_path)
    except Exception:
        pass

    if sys.platform == "darwin":
        script = (
            'POSIX path of (choose file with prompt "Select a sketch image" '
            'of type {"public.image"})'
        )
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            selected_path = result.stdout.strip()
            if selected_path:
                return Path(selected_path)

    user_input = input("Enter the full path to your sketch image (or press Enter to cancel): ").strip()
    if not user_input:
        return None

    return Path(user_input)

if __name__ == "__main__":
    selected_sketch_path = choose_sketch_path()
    if selected_sketch_path is None:
        print("No sketch selected. Exiting.")
        raise SystemExit(0)

    layout_output = process_sketch(
        sketch_path=selected_sketch_path,
        lot_boundary=[[0, 0], [0, 1000], [1000, 0], [1000, 1000]],
        site_width_ft=1000,
        site_height_ft=1000,
    )
        