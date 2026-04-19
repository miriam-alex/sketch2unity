```json
{
  "site_scale": {
    "site_width_ft": 100,
    "site_height_ft": 60,
    "normalized_canvas": [0, 0, 1000, 1000],
    "lot_boundary": [
      [130, 80],
      [100, 200],
      [100, 700],
      [150, 920],
      [250, 950],
      [880, 950],
      [900, 700],
      [900, 300],
      [880, 80],
      [750, 50],
      [200, 50]
    ],
    "scale_note": "All placements must fall within lot_boundary. Bounding boxes define placement. Real-world dimensions define scale."
  },
  "terrain_zones": [
    {
      "area_name": "Main Lawn",
      "semantic_tag": "lawn",
      "terrain_type": "grass",
      "bounding_box": [100, 50, 900, 950],
      "approx_sq_ft": 3935,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Cafe Outdoor Seating Plaza",
      "semantic_tag": "outdoor_dining",
      "terrain_type": "plaza",
      "bounding_box": [600, 230, 750, 420],
      "approx_sq_ft": 170,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Daycare Play Area Planting Bed",
      "semantic_tag": "playground",
      "terrain_type": "planting_bed",
      "bounding_box": [500, 560, 750, 750],
      "approx_sq_ft": 280,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Cafe Entrance Path",
      "semantic_tag": "path",
      "terrain_type": "pavement",
      "bounding_box": [750, 150, 800, 230],
      "approx_sq_ft": 25,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Daycare Entrance Path",
      "semantic_tag": "path",
      "terrain_type": "pavement",
      "bounding_box": [750, 760, 800, 850],
      "approx_sq_ft": 30,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Central Walkway",
      "semantic_tag": "walkway",
      "terrain_type": "pavement",
      "bounding_box": [450, 470, 800, 530],
      "approx_sq_ft": 130,
      "unity_strategy": "paint_terrain"
    }
  ],
  "generated_objects": [
    {
      "area_name": "Dr.'s Office Building",
      "semantic_tag": "medical_facility",
      "object_type": "building",
      "bounding_box": [280, 100, 500, 880],
      "center_point": [390, 490],
      "approx_sq_ft": 1030,
      "target_dimensions_ft": {
        "width_ft": 78,
        "depth_ft": 13.2,
        "height_ft": 24
      },
      "unity_strategy": "box_primitive"
    },
    {
      "area_name": "Cafe Building",
      "semantic_tag": "cafe",
      "object_type": "building",
      "bounding_box": [500, 100, 750, 230],
      "center_point": [625, 165],
      "approx_sq_ft": 200,
      "target_dimensions_ft": {
        "width_ft": 13,
        "depth_ft": 15,
        "height_ft": 14
      },
      "unity_strategy": "box_primitive"
    },
    {
      "area_name": "Daycare Building",
      "semantic_tag": "childcare",
      "object_type": "building",
      "bounding_box": [500, 750, 750, 880],
      "center_point": [625, 815],
      "approx_sq_ft": 200,
      "target_dimensions_ft": {
        "width_ft": 13,
        "depth_ft": 15,
        "height_ft": 14
      },
      "unity_strategy": "box_primitive"
    }
  ],
  "prefab_instances": [
    {
      "area_name": "Cafe Bench 1",
      "semantic_tag": "seating",
      "prefab_type": "bench",
      "center_point": [650, 270],
      "footprint_box": [600, 260, 700, 280],
      "rotation_deg": 90,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Cafe Bench 2",
      "semantic_tag": "seating",
      "prefab_type": "bench",
      "center_point": [680, 270],
      "footprint_box": [630, 260, 730, 280],
      "rotation_deg": 90,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Cafe Bench 3",
      "semantic_tag": "seating",
      "prefab_type": "bench",
      "center_point": [710, 270],
      "footprint_box": [660, 260, 760, 280],
      "rotation_deg": 90,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Cafe Bench 4",
      "semantic_tag": "seating",
      "prefab_type": "bench",
      "center_point": [650, 300],
      "footprint_box": [600, 290, 700, 310],
      "rotation_deg": 90,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Cafe Bench 5",
      "semantic_tag": "seating",
      "prefab_type": "bench",
      "center_point": [680, 300],
      "footprint_box": [630, 290, 730, 310],
      "rotation_deg": 90,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Cafe Area Tree 1",
      "semantic_tag": "landscaping",
      "prefab_type": "tree",
      "center_point": [550, 350],
      "footprint_box": [508, 325, 591, 375],
      "rotation_deg": 0,
      "scale_multiplier": 1.2,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Cafe Area Tree 2",
      "semantic_tag": "landscaping",
      "prefab_type": "tree",
      "center_point": [520, 380],
      "footprint_box": [478, 355, 561, 405],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Daycare Area Tree 1",
      "semantic_tag": "landscaping",
      "prefab_type": "tree",
      "center_point": [600, 650],
      "footprint_box": [558, 625, 641, 675],
      "rotation_deg": 0,
      "scale_multiplier": 1.2,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Daycare Area Tree 2",
      "semantic_tag": "landscaping",
      "prefab_type": "tree",
      "center_point": [630, 680],
      "footprint_box": [588, 655, 671, 705],
      "rotation_deg": 0,
      "scale_multiplier": 1.0,
      "unity_strategy": "place_prefab"
    },
    {
      "area_name": "Daycare Area Tree 3",
      "semantic_tag": "landscaping",
      "prefab_type": "tree",
      "center_point": [660, 620],
      "footprint_box": [618, 595, 701, 645],
      "rotation_deg": 0,
      "scale_multiplier": 1.1,
      "unity_strategy": "place_prefab"
    }
  ]
}
```