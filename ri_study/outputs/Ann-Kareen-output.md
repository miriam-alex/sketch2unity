{
  "site_scale": {
    "site_width_ft": 150,
    "site_height_ft": 200,
    "normalized_canvas": [0, 0, 1000, 1000],
    "scale_note": "Bounding boxes define placement. Real-world dimensions define scale."
  },
  "terrain_zones": [
    {
      "area_name": "Central Plaza",
      "semantic_tag": "plaza_pavement",
      "terrain_type": "plaza",
      "bounding_box": [150, 120, 850, 400],
      "approx_sq_ft": 8000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "East Waterfront Walk",
      "semantic_tag": "riverfront_asphalt",
      "terrain_type": "asphalt",
      "bounding_box": [100, 480, 900, 680],
      "approx_sq_ft": 6000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Northwest Planting Bed",
      "semantic_tag": "landscaped_garden",
      "terrain_type": "planting_bed",
      "bounding_box": [170, 70, 210, 130],
      "approx_sq_ft": 400,
      "unity_strategy": "paint_terrain"
    }
  ],
  "generated_objects": [
    {
      "area_name": "Museum of History",
      "semantic_tag": "educational_structure",
      "object_type": "building",
      "bounding_box": [420, 130, 550, 215],
      "center_point": [485, 172],
      "approx_sq_ft": 1500,
      "target_dimensions_ft": {
        "width_ft": 30,
        "depth_ft": 50,
        "height_ft": 25
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic 2-story museum pavilion, contemporary glass and metal curtain wall, sleek flat roof, museum signage on glass, plain white background, no shadows, no people, physically based rendering",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, water, blurry, cut off edges",
        "meshy_notes": "Reference Image K for contemporary glass/metal style; footprint estimated from Art Gallery analog 1,500 sq ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Retail Shop Cluster North",
      "semantic_tag": "commercial_row",
      "object_type": "building",
      "bounding_box": [85, 65, 175, 450], "center_point": [130, 257],
      "approx_sq_ft": 4500,
      "target_dimensions_ft": {
        "width_ft": 115,
        "depth_ft": 40,
        "height_ft": 20
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a modern single-story shopping row, four distinct retail units, floor-to-ceiling glass storefronts with black metal framing, flat roof, plain white background, no shadows, high resolution",
        "negative_prompt": "cars, people, street lamps, trees, floor reflections, sky, horizon",
        "meshy_notes": "Contemporary mixed-use infill style; treat as a single mesh row for efficiency."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "West Retail Wing",
      "semantic_tag": "commercial_shops",
      "object_type": "building",
      "bounding_box": [210, 65, 435, 130],
      "center_point": [322, 97],
      "approx_sq_ft": 2400,
      "target_dimensions_ft": {
        "width_ft": 25,
        "depth_ft": 95,
        "height_ft": 20
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a contemporary glass boutique retail block, metal panel accents, large windows, minimalist architecture, plain white background, PBR materials",
        "negative_prompt": "watermark, text, blurry, ground, environment, sun, glare",
        "meshy_notes": "Matches Shop 9, 10, 11 on the sketch; estimated 800 sq ft per unit."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "East Retail Wing",
      "semantic_tag": "commercial_shops",
      "object_type": "building",
      "bounding_box": [200, 395, 480, 465],
      "center_point": [340, 430],
      "approx_sq_ft": 2400,
      "target_dimensions_ft": {
        "width_ft": 25,
        "depth_ft": 110,
        "height_ft": 20
      },
      "image_gen_prompt": {
        "prompt": "Isometric view of a modern retail strip, glass facade, contemporary metal cladding, flat roof, white background, high-end boutique style",
        "negative_prompt": "trees, people, signage, car, road, grass",
        "meshy_notes": "Matches Shop 5-8 on the sketch."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Tram Hub Building",
      "semantic_tag": "transportation_hub",
      "object_type": "building",
      "bounding_box": [220, 680, 580, 825], "center_point": [400, 752],
      "approx_sq_ft": 4500,
      "target_dimensions_ft": {
        "width_ft": 50,
        "depth_ft": 90,
        "height_ft": 35
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic tram station building, steel structure with large glass panels, industrial-modern aesthetic, plain white background, no cable lines, no cars",
        "negative_prompt": "cables, sky, ground, vegetation, watermark, text",
        "meshy_notes": "Ensure open entryways for tram car docking."
      },
      "unity_strategy": "generate_mesh"
    }
  ],
  "prefab_instances": [
    {
      "area_name": "North Entry Tree",
      "semantic_tag": "foliage",
      "prefab_type": "tree",
      "center_point": [180, 95],
      "footprint_box": [165, 80, 195, 110],
      "rotation_deg": 0,
      "scale_multiplier": 1.2,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Southeast Corner Tree",
      "semantic_tag": "foliage",
      "prefab_type": "tree",
      "center_point": [520, 435],
      "footprint_box": [480, 400, 560, 470],
      "rotation_deg": 45,
      "scale_multiplier": 1.5,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Southwest Corner Tree",
      "semantic_tag": "foliage",
      "prefab_type": "tree",
      "center_point": [480, 105],
      "footprint_box": [430, 75, 550, 135],
      "rotation_deg": 0,
      "scale_multiplier": 1.8,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Plaza Bench 1",
      "semantic_tag": "site_furniture",
      "prefab_type": "bench",
      "center_point": [220, 165],
      "footprint_box": [215, 140, 225, 190],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Plaza Bench 2",
      "semantic_tag": "site_furniture",
      "prefab_type": "bench",
      "center_point": [270, 165],
      "footprint_box": [265, 140, 275, 190],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Plaza Bench 3",
      "semantic_tag": "site_furniture",
      "prefab_type": "bench",
      "center_point": [320, 165],
      "footprint_box": [315, 140, 325, 190],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    }
  ]
}