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
      "area_name": "Site Road",
      "semantic_tag": "road",
      "terrain_type": "asphalt",
      "bounding_box": [100, 0, 800, 450],
      "approx_sq_ft": 9450,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Central Plaza",
      "semantic_tag": "plaza_area",
      "terrain_type": "plaza",
      "bounding_box": [0, 400, 1000, 1000],
      "approx_sq_ft": 18000,
      "unity_strategy": "paint_terrain"
    }
  ],
  "generated_objects": [
    {
      "area_name": "Roosevelt Island Museum of History",
      "semantic_tag": "museum",
      "object_type": "building",
      "bounding_box": [200, 650, 800, 950],
      "center_point": [500, 800],
      "approx_sq_ft": 5400,
      "target_dimensions_ft": {
        "width_ft": 30,
        "depth_ft": 180,
        "height_ft": 36
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern 2-story museum building, reclaimed red brick facade with regular fenestration and tall arched windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 15k-25k poly budget; bake diffuse and normal maps separately. Building footprint is 5400 sq ft, intended as two stories."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Aquarium Building",
      "semantic_tag": "aquarium",
      "object_type": "building",
      "bounding_box": [350, 450, 750, 800],
      "center_point": [550, 625],
      "approx_sq_ft": 4200,
      "target_dimensions_ft": {
        "width_ft": 35,
        "depth_ft": 120,
        "height_ft": 25
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern 1-2 story aquarium building, lower half with reclaimed dark red brick facade from a power plant, upper half with expansive clear glass windows, a subtle curved side, flat roof, plain white background, no shadows, no people, physically based rendering, high resolution.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 15k-25k poly budget; bake diffuse and normal maps separately. Footprint estimated for a public facility, 4200 sq ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Ferry to Aquarium Pedestrian Bridge",
      "semantic_tag": "pedestrian_bridge",
      "object_type": "structure",
      "bounding_box": [200, 200, 500, 650],
      "center_point": [350, 425],
      "approx_sq_ft": 2250,
      "target_dimensions_ft": {
        "width_ft": 15,
        "depth_ft": 150,
        "height_ft": 20
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern pedestrian bridge, inclined steel truss structure with transparent glass side panels and a textured concrete walking surface, connecting to a building roof, plain white background, no shadows, no people, physically based rendering, high resolution.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 10k-15k poly budget; bake diffuse and normal maps separately. Ensure a structurally sound bridge deck and support system for pedestrian traffic."
      },
      "unity_strategy": "generate_mesh"
    }
  ],
  "prefab_instances": [
    {
      "area_name": "Plaza Bench 1",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [923, 530],
      "footprint_box": [920, 500, 927, 560],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Plaza Bench 2",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [923, 630],
      "footprint_box": [920, 600, 927, 660],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Plaza Bench 3",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [923, 730],
      "footprint_box": [920, 700, 927, 760],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Plaza Bench 4",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [923, 830],
      "footprint_box": [920, 800, 927, 860],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Plaza Bench 5",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [923, 930],
      "footprint_box": [920, 900, 927, 960],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    }
  ]
}
```