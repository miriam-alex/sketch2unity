from layout_prompt import process_sketch, visualize_output
from pathlib import Path
import json

# layout_output = process_sketch(
# 	lot_boundary=[[0, 0], [0, 1000], [1000, 0], [1000, 1000]],
# 	site_width_ft=1000,
# 	site_height_ft=1000,
# )

OUTPUT_PATH = Path("sample_output.json")

with open(OUTPUT_PATH, 'r') as file:
    content = file.read()
    print(content)
    site_data = json.loads(content)
    visualize_output(site_data)
