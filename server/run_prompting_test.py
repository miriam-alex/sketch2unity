from server.layout_prompt import process_sketch, visualize_output, choose_sketch_path
from pathlib import Path
import json

OUTPUT_PATH = Path("sample_output.json")

selected_sketch_path = choose_sketch_path()
if selected_sketch_path is None:
    print("No sketch selected. Exiting.")
    raise SystemExit(0)

layout_output = process_sketch(
    output_path=OUTPUT_PATH,
    sketch_path=selected_sketch_path,
    lot_boundary=[[0, 0], [0, 1000], [1000, 0], [1000, 1000]],
    site_width_ft=1000,
    site_height_ft=1000,
)

with open(OUTPUT_PATH, 'r') as file:
    content = file.read()
    print(content)
    site_data = json.loads(content)
    visualize_output(site_data)
