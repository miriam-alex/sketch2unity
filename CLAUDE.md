# sketch2unity

A pipeline that ingests hand-drawn layout sketches, uses an LLM to generate structured JSON describing the layout, then streams that JSON to a Unity application which instantiates prefabs from it.

## Architecture

```
sketch (PNG/JPG)
  → layout_prompt.py  (LLM call: Gemini or Claude)
  → sample_output.json
  → server/server.py  (Flask HTTP bridge, port 5002)
  → Unity (C# reads JSON, places prefabs)
```

## Running

```bash
source .venv/bin/activate
python server/server.py
# Then run the Unity project
```

## Key Files

- `server/server.py` — Flask server (port 5002); routes: `/health`, `/api/list`, `/api/search`, `/api/download/<filename>`, `/api/layout/generate`
- `server/layout_prompt.py` — LLM integration (Gemini or Claude) + `choose_sketch_path()` for file picker + `process_sketch()` for the full pipeline
- `server/site_parsing.md` — the system prompt sent to the LLM
- `sample_output.json` — most recent layout generation output
- `models/` — `.obj` / `.glb` 3D model files served to Unity
- `unity/model2unity/` — Unity project

## Environment

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=...
ANTHROPIC_API_KEY=...
```

## LLM Provider

Controlled by `CURRENT_PROVIDER` in `layout_prompt.py` (line 22). Set to `"gemini"` or `"claude"`.

- Gemini model: `GEMINI_MODEL_ID` (currently `gemini-3.5-flash`)
- Claude model: `CLAUDE_MODEL_ID` (currently `claude-sonnet-4-6`)

## macOS Threading Note

`choose_sketch_path()` uses `osascript` (not Tkinter) on macOS. Tkinter's `NSWindow` crashes when created from a Flask background thread. The `osascript` approach spawns a subprocess and is thread-safe.

## Layout JSON Schema

`sample_output.json` / `sample_output.md` show the expected output shape. Key top-level keys:
- `site_scale` — normalized canvas + real-world dimensions
- `terrain_zones` — list of zones with `bounding_box`, `terrain_type`, `area_name`
- `generated_objects` — non-building objects with `bounding_box`, `center_point`, `object_type`
- `generated_buildings` — buildings with `bounding_box`, `center_point`, `area_name`
- `prefab_instances` — tree/bench/etc. with `center_point`, `footprint_box`, `prefab_type`, `scale_multiplier`

## lot_boundary Convention

Points are `[y, x]` (not `[x, y]`), normalized 0–1000. Minimum 3 points required.
