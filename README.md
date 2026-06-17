# To Run

Set up an .env file with the GOOGLE_API_KEY and/or ANTHROPIC_API_KEY variables.

`python -m venv .venv`

`pip install -r requirements.txt`

`source .venv/bin/activate`

`python server/server.py`

Run Unity project

# Testing With Lot Boundary Context

You can pass lot boundary coordinates directly as a Python list to `process_sketch`.

Example:

```python
from prompting import process_sketch

process_sketch(
	lot_boundary=[[20, 100], [60, 940], [930, 880], [900, 120]],
	site_width_ft=220,
	site_height_ft=180,
)
```

Notes:
- `lot_boundary` must be a list of `[y, x]` points.
- Coordinates must be in normalized range `0` to `1000`.
- At least 3 points are required.
