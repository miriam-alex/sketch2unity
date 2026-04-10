```json
{
  "site_scale": {
    "site_width_ft": 150,
    "site_height_ft": 200,
    "normalized_canvas": [0, 0, 1000, 1000],
    "scale_note": "Bounding boxes define placement. Real-world dimensions define scale."
  },
  "terrain_zones": [
    {
      "area_name": "East River (West)",
      "semantic_tag": "water_body",
      "terrain_type": "water",
      "bounding_box": [0, 0, 1000, 200],
      "approx_sq_ft": 6000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "East River (East)",
      "semantic_tag": "water_body",
      "terrain_type": "water",
      "bounding_box": [0, 800, 1000, 1000],
      "approx_sq_ft": 6000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Museum Grounds Lawn",
      "semantic_tag": "landscape",
      "terrain_type": "grass",
      "bounding_box": [0, 200, 1000, 800],
      "approx_sq_ft": 18000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Museum Entrance Path",
      "semantic_tag": "access_path",
      "terrain_type": "pavement",
      "bounding_box": [700, 450, 1000, 550],
      "approx_sq_ft": 1200,
      "unity_strategy": "paint_terrain"
    }
  ],
  "generated_objects": [
    {
      "area_name": "Roosevelt Island Museum of History",
      "semantic_tag": "museum_building",
      "object_type": "building",
      "bounding_box": [250, 350, 700, 650],
      "center_point": [475, 500],
      "approx_sq_ft": 6750,
      "target_dimensions_ft": {
        "width_ft": 45,
        "depth_ft": 90,
        "height_ft": 48
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic 4-story Roosevelt Island Museum of History building. The building features a robust dark reddish-brown brick facade, similar in style and color to historic industrial architecture like the original power plant, with distinct rounded arch windows on the lower levels and rectangular windows on upper levels. The main entrance has double doors. An integrated pedestrian bridge structure with metal trusses extends from the upper right side of the building, connecting to an unseen off-site connection point. Flat roof with a subtle parapet. Plain white background, no shadows, no people, physically based rendering, high resolution photograph.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion, modern glass facade, plain concrete, cartoon, low poly.",
        "meshy_notes": "The building has 4 distinct floors. Pay attention to the integrated bridge structure on the right side. Use image-to-3D with multiview reconstruction enabled; target 20k-30k poly budget; bake diffuse and normal maps separately. Footprint estimated from nearest analog: A large public building, 6,750 sq ft footprint, 27,000 sq ft total area."
      },
      "unity_strategy": "generate_mesh"
    }
  ],
  "prefab_instances": []
}
```