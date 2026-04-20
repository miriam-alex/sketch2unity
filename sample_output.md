```json
{
  "site_scale": {
    "site_width_ft": 1000,
    "site_height_ft": 1000,
    "normalized_canvas": [
      0,
      0,
      1000,
      1000
    ],
    "lot_boundary": [
      [
        0,
        0
      ],
      [
        0,
        1000
      ],
      [
        1000,
        0
      ],
      [
        1000,
        1000
      ]
    ],
    "scale_note": "All placements must fall within lot_boundary. Bounding boxes define placement. Real-world dimensions define scale."
  },
  "terrain_zones": [
    {
      "area_name": "Cafe Front Walkway",
      "semantic_tag": "pedestrian_path",
      "terrain_type": "pavement",
      "bounding_box": [
        980,
        0,
        1000,
        350
      ],
      "approx_sq_ft": 7000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Daycare Front Walkway",
      "semantic_tag": "pedestrian_path",
      "terrain_type": "pavement",
      "bounding_box": [
        980,
        650,
        1000,
        1000
      ],
      "approx_sq_ft": 7000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Central Pathway Extension",
      "semantic_tag": "pedestrian_path",
      "terrain_type": "pavement",
      "bounding_box": [
        980,
        350,
        1000,
        650
      ],
      "approx_sq_ft": 6000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Central Pathway",
      "semantic_tag": "pedestrian_path",
      "terrain_type": "pavement",
      "bounding_box": [
        500,
        450,
        980,
        550
      ],
      "approx_sq_ft": 48000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Left Courtyard Planting",
      "semantic_tag": "landscaping",
      "terrain_type": "planting_bed",
      "bounding_box": [
        500,
        350,
        980,
        450
      ],
      "approx_sq_ft": 48000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Right Courtyard Planting",
      "semantic_tag": "landscaping",
      "terrain_type": "planting_bed",
      "bounding_box": [
        500,
        550,
        980,
        650
      ],
      "approx_sq_ft": 48000,
      "unity_strategy": "paint_terrain"
    }
  ],
  "generated_objects": [
    {
      "area_name": "Dr.'s Office",
      "semantic_tag": "medical_facility",
      "object_type": "building",
      "bounding_box": [
        0,
        0,
        500,
        1000
      ],
      "center_point": [
        250,
        500
      ],
      "approx_sq_ft": 500000,
      "target_dimensions_ft": {
        "width_ft": 1000,
        "depth_ft": 500,
        "height_ft": 40
      },
      "unity_strategy": "box_primitive"
    },
    {
      "area_name": "Cafe",
      "semantic_tag": "restaurant",
      "object_type": "building",
      "bounding_box": [
        500,
        0,
        980,
        350
      ],
      "center_point": [
        740,
        175
      ],
      "approx_sq_ft": 168000,
      "target_dimensions_ft": {
        "width_ft": 350,
        "depth_ft": 480,
        "height_ft": 14
      },
      "unity_strategy": "box_primitive"
    },
    {
      "area_name": "Daycare",
      "semantic_tag": "childcare_center",
      "object_type": "building",
      "bounding_box": [
        500,
        650,
        980,
        1000
      ],
      "center_point": [
        740,
        825
      ],
      "approx_sq_ft": 168000,
      "target_dimensions_ft": {
        "width_ft": 350,
        "depth_ft": 480,
        "height_ft": 14
      },
      "unity_strategy": "box_primitive"
    }
  ],
  "prefab_instances": [
    {
      "area_name": "Courtyard Bench 1",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [
        700,
        380
      ],
      "footprint_box": [
        690,
        370,
        710,
        390
      ],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Courtyard Bench 2",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [
        730,
        400
      ],
      "footprint_box": [
        720,
        390,
        740,
        410
      ],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Courtyard Bench 3",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [
        760,
        380
      ],
      "footprint_box": [
        750,
        370,
        770,
        390
      ],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Courtyard Bench 4",
      "semantic_tag": "outdoor_seating",
      "prefab_type": "bench",
      "center_point": [
        790,
        400
      ],
      "footprint_box": [
        780,
        390,
        800,
        410
      ],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Courtyard Tree Left",
      "semantic_tag": "shade_tree",
      "prefab_type": "tree",
      "center_point": [
        630,
        400
      ],
      "footprint_box": [
        610,
        380,
        650,
        420
      ],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Courtyard Tree Right",
      "semantic_tag": "shade_tree",
      "prefab_type": "tree",
      "center_point": [
        630,
        580
      ],
      "footprint_box": [
        610,
        560,
        650,
        600
      ],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    }
  ]
}
```