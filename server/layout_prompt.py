import os
import time
import random
import json
import base64
import subprocess
import sys
from pathlib import Path
from typing import Iterable
from dotenv import load_dotenv
from google import genai
from google.genai import types
import anthropic
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

load_dotenv()

# =========================================================
# Provider selection
# =========================================================
CURRENT_PROVIDER = "claude"  # "gemini" or "claude"

# =========================================================
# Gemini configuration
# =========================================================
GEMINI_MODEL_ID = "gemini-3.5-flash"
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# =========================================================
# Claude configuration (placeholders — fill in as needed)
# =========================================================
CLAUDE_MODEL_ID = "claude-sonnet-4-6"            # TODO: confirm/replace with desired Claude model id
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY")  # TODO: set ANTHROPIC_API_KEY in your .env
CLAUDE_MAX_TOKENS = 12000                        

# =========================================================
# Shared configuration
# =========================================================
PROMPT_PATH = Path("prompts/site_parsing.md")
OUTPUT_PATH = Path("sample_output.json")
MAX_RETRIES = 3

# =========================================================
# Client setup
# =========================================================
gemini_client = genai.Client(api_key=GEMINI_API_KEY)
claude_client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)


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

    for obj in site_data["generated_buildings"]:
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
            f'{obj["area_name"]}',
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

def extract_json(response: str) -> dict:
    try:
        start = response.index('{')
        end = response.rindex('}')
        return response[start:end + 1]
    except ValueError as e:
        raise ValueError(f"Could not extract JSON from response: {e}\n\nRaw response:\n{response}")

class ResponseTruncatedError(Exception):
    """
    Raised when the model stopped because it hit the output token limit,
    not because it actually finished. The JSON will be incomplete, so this
    is treated as a distinct failure mode from rate limits / API errors.
    """
    pass


def _call_model(prompt_text, runtime_context, image_bytes):
    """
    Makes a single API call to whichever provider CURRENT_PROVIDER points to.
    Returns the raw text response from the model (not yet JSON-extracted).
    Raises on any API error so the retry wrapper can decide what to do with it.
    Raises ResponseTruncatedError specifically if the response was cut off
    before the model finished (i.e. it hit the max output token limit).
    """
    if CURRENT_PROVIDER == "gemini":
        contents = [prompt_text]
        if runtime_context:
            contents.append(runtime_context)
        contents.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))

        response = gemini_client.models.generate_content(
            model=GEMINI_MODEL_ID,
            contents=contents,
        )

        finish_reason = None
        if getattr(response, "candidates", None):
            finish_reason = getattr(response.candidates[0], "finish_reason", None)
        if finish_reason is not None and "MAX_TOKENS" in str(finish_reason).upper():
            raise ResponseTruncatedError(
                "Gemini's response was truncated before it finished the JSON "
                "(hit the max output token limit). Increase the output token "
                "budget for this model and try again."
            )

        return response.text

    elif CURRENT_PROVIDER == "claude":
        text_parts = [prompt_text]
        if runtime_context:
            text_parts.append(runtime_context)
        combined_text = "\n".join(text_parts)

        image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

        response = claude_client.messages.create(
            model=CLAUDE_MODEL_ID,
            max_tokens=CLAUDE_MAX_TOKENS,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": image_b64,
                            },
                        },
                        {
                            "type": "text",
                            "text": combined_text,
                        },
                    ],
                }
            ],
        )

        if response.stop_reason == "max_tokens":
            raise ResponseTruncatedError(
                f"Claude's response was truncated at the {CLAUDE_MAX_TOKENS}-token "
                "limit before it finished the JSON. Increase CLAUDE_MAX_TOKENS and "
                "try again."
            )

        return "".join(
            block.text for block in response.content if getattr(block, "type", None) == "text"
        )

    else:
        raise ValueError(
            f"Unknown CURRENT_PROVIDER: {CURRENT_PROVIDER!r}. Expected 'gemini' or 'claude'."
        )


def call_model_with_retries(prompt_text, runtime_context, image_bytes):
    """
    Factored-out retry + dispatch logic. Looks at CURRENT_PROVIDER and calls the
    matching provider via _call_model, retrying on rate-limit/overload errors.
    Returns the extracted JSON string (same format the old inline code produced),
    or None if every retry failed / a permanent error occurred.
    """
    output = None

    for attempt in range(MAX_RETRIES):
        try:
            print(f"🔄 [Calling {CURRENT_PROVIDER} (Attempt {attempt+1})...")
            raw_output = _call_model(prompt_text, runtime_context, image_bytes)
            output = extract_json(raw_output)
            break

        except ResponseTruncatedError as e:
            # Retrying with the same token budget would just truncate again,
            # so fail loud immediately instead of burning retries.
            print(f"✂️ {e}")
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

    prompt_text = prompt_path.read_text(encoding="utf-8")
    image_bytes = sketch_path.read_bytes()

    print(f"🔄 [Processing {sketch_path}...")
    output = call_model_with_retries(prompt_text, runtime_context, image_bytes)

    if output is not None:
        output_path.write_text(output, encoding="utf-8")
        print(f"Success: {output_path.name}")
        if normalized_boundary is not None:
            print(f"Applied lot boundary with {len(normalized_boundary)} points")

    return output


def choose_sketch_path():
    # On macOS, Tkinter crashes when called from a background thread (Flask handler)
    # because NSWindow must be instantiated on the main thread. Use osascript instead,
    # which spawns a separate process and is safe from any thread.
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
    else:
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

    user_input = input("Enter the full path to your sketch image (or press Enter to cancel): ").strip()
    if not user_input:
        return None

    return Path(user_input)

if __name__ == "__main__":
    # Site 1 (Site A) lot boundary — pentagonal waterfront parcel along Bronx River,
    # wider at north, tapering southeast toward the river bank.
    SITE_1_LOT_BOUNDARY = [
        [ 50, 150],   # northwest corner
        [ 80, 700],   # northeast corner
        [320, 620],   # east side mid (angles inward)
        [420, 350],   # southeast tip
        [280,  80],   # west side mid (river bank)
    ]

    selected_sketch_path = choose_sketch_path()
    if selected_sketch_path is None:
        print("No sketch selected. Exiting.")
        raise SystemExit(0)

    layout_output = process_sketch(
        sketch_path=selected_sketch_path,
        lot_boundary=SITE_1_LOT_BOUNDARY,
        site_width_ft=220,
        site_height_ft=180,
    )

    if layout_output is None:
        print("Layout generation failed.")
        raise SystemExit(1)

    data = json.loads(layout_output)
    visualize_output(data)