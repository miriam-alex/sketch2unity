```json
{
  "site_scale": {
    "site_width_ft": 100,
    "site_height_ft": 300,
    "normalized_canvas": [0, 0, 1000, 1000],
    "scale_note": "Bounding boxes define placement. Real-world dimensions define scale."
  },
  "terrain_zones": [
    {
      "area_name": "Community Plaza",
      "semantic_tag": "public_space",
      "terrain_type": "plaza",
      "bounding_box": [600, 0, 1000, 1000],
      "approx_sq_ft": 12000,
      "unity_strategy": "paint_terrain"
    }
  ],
  "generated_objects": [
    {
      "area_name": "Bridge Abutment Base",
      "semantic_tag": "infrastructure_support",
      "object_type": "structure",
      "bounding_box": [750, 700, 950, 900],
      "center_point": [850, 800],
      "approx_sq_ft": 1200,
      "target_dimensions_ft": {
        "width_ft": 20,
        "depth_ft": 60,
        "height_ft": 50
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic rugged stone bridge abutment, archway at base, weathered grey stone, no shadows, no people, plain white background, physically based rendering, high resolution.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 10k–20k poly budget; bake diffuse and normal maps separately."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Multi-level Escalator",
      "semantic_tag": "transportation_hub",
      "object_type": "structure",
      "bounding_box": [700, 450, 900, 550],
      "center_point": [800, 500],
      "approx_sq_ft": 600,
      "target_dimensions_ft": {
        "width_ft": 10,
        "depth_ft": 60,
        "height_ft": 40
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern multi-level outdoor escalator structure, glass and steel construction, illuminated steps, plain white background, no shadows, no people, physically based rendering, high resolution.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 8k–15k poly budget; bake diffuse and normal maps separately."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Colorful Climbing Wall",
      "semantic_tag": "recreational_facility",
      "object_type": "structure",
      "bounding_box": [800, 200, 850, 400],
      "center_point": [825, 300],
      "approx_sq_ft": 300,
      "target_dimensions_ft": {
        "width_ft": 20,
        "depth_ft": 15,
        "height_ft": 30
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern outdoor climbing wall, integrated colorful climbing holds, sleek gray paneling, plain white background, no shadows, no people, physically based rendering, high resolution.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 5k–10k poly budget; bake diffuse and normal maps separately."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Ice Cream Shop",
      "semantic_tag": "retail_food",
      "object_type": "building",
      "bounding_box": [800, 50, 900, 200],
      "center_point": [850, 125],
      "approx_sq_ft": 450,
      "target_dimensions_ft": {
        "width_ft": 15,
        "depth_ft": 30,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic cute and traditional single-story ice cream shop building, colorful awning, large display windows, light pastel facade, flat roof, plain white background, no shadows, no people, physically based rendering, high resolution, 15ft wide by 30ft deep.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Footprint estimated from nearest analog: Ice Cream / Gelato Shop 500 sq ft. Use image-to-3D with multiview reconstruction enabled; target 5k–10k poly budget; bake diffuse and normal maps separately."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "24-Hour Chicken Shop",
      "semantic_tag": "retail_food",
      "object_type": "building",
      "bounding_box": [750, 250, 900, 500],
      "center_point": [825, 375],
      "approx_sq_ft": 1125,
      "target_dimensions_ft": {
        "width_ft": 25,
        "depth_ft": 45,
        "height_ft": 18
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic cute and traditional single-story 24-hour chicken shop building, prominent signage for 'Chicken 24 HR', warm brick facade, inviting entrance, flat roof, plain white background, no shadows, no people, physically based rendering, high resolution, 25ft wide by 45ft deep.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Footprint estimated from nearest analog: Deli 1000 sq ft. Use image-to-3D with multiview reconstruction enabled; target 5k–10k poly budget; bake diffuse and normal maps separately."
      },
      "unity_strategy": "generate_mesh"
    }
  ],
  "prefab_instances": []
}
```