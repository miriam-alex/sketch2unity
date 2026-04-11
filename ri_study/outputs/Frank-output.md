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
      "area_name": "Vendor Plaza Zone",
      "semantic_tag": "public_plaza",
      "terrain_type": "plaza",
      "bounding_box": [0, 0, 330, 1000],
      "approx_sq_ft": 10000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Restaurant Plaza Zone",
      "semantic_tag": "public_plaza",
      "terrain_type": "plaza",
      "bounding_box": [330, 0, 660, 1000],
      "approx_sq_ft": 10000,
      "unity_strategy": "paint_terrain"
    },
    {
      "area_name": "Aquarium Plaza Zone",
      "semantic_tag": "public_plaza",
      "terrain_type": "plaza",
      "bounding_box": [660, 0, 1000, 1000],
      "approx_sq_ft": 10000,
      "unity_strategy": "paint_terrain"
    }
  ],
  "generated_objects": [
    {
      "area_name": "Food Truck Kiosk",
      "semantic_tag": "food_service_kiosk",
      "object_type": "kiosk",
      "bounding_box": [60, 450, 150, 550],
      "center_point": [105, 500],
      "approx_sq_ft": 250,
      "target_dimensions_ft": {
        "width_ft": 10,
        "depth_ft": 25,
        "height_ft": 10
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern food truck kiosk, sleek minimalist design, dark grey metallic exterior with subtle blue accents, integrated service window, flat roof, wheels visible, plain white background, no shadows, physically based rendering, high resolution, 10ft wide, 25ft deep, 10ft tall",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion, complex background",
        "meshy_notes": "Focus on clean edges and distinct forms; target 5k-10k poly budget."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Boba Stand Kiosk",
      "semantic_tag": "food_service_kiosk",
      "object_type": "kiosk",
      "bounding_box": [160, 420, 240, 480],
      "center_point": [200, 450],
      "approx_sq_ft": 144,
      "target_dimensions_ft": {
        "width_ft": 6,
        "depth_ft": 24,
        "height_ft": 8
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern boba tea stand kiosk, minimalist cube design, smooth light grey concrete texture, small service window, dark frame, flat roof, plain white background, no shadows, physically based rendering, high resolution, 6ft wide, 24ft deep, 8ft tall",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion, complex background",
        "meshy_notes": "Ensure clean geometric shapes; target 3k-5k poly budget."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "BBQ Stand Kiosk",
      "semantic_tag": "food_service_kiosk",
      "object_type": "kiosk",
      "bounding_box": [160, 490, 240, 550],
      "center_point": [200, 520],
      "approx_sq_ft": 144,
      "target_dimensions_ft": {
        "width_ft": 6,
        "depth_ft": 24,
        "height_ft": 8
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern BBQ food stand kiosk, industrial metal texture with black accents, simple rectangular form, integrated ventilation hood, flat roof, plain white background, no shadows, physically based rendering, high resolution, 6ft wide, 24ft deep, 8ft tall",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion, complex background",
        "meshy_notes": "Capture the industrial feel; target 3k-5k poly budget."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Vendor Area Curved Structure",
      "semantic_tag": "public_structure",
      "object_type": "structure",
      "bounding_box": [0, 600, 330, 900],
      "center_point": [165, 750],
      "approx_sq_ft": 3000,
      "target_dimensions_ft": {
        "width_ft": 30,
        "depth_ft": 100,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern curved public structure, smooth concrete facade, clean lines, minimalist design, no visible windows or doors as it defines a public space edge, flat roof, plain white background, no shadows, physically based rendering, high resolution, 30ft wide, 100ft long, 15ft tall",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion, complex background, overly ornate",
        "meshy_notes": "Prioritize smooth curved surfaces; target 10k-20k poly budget."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Better Restaurant Building",
      "semantic_tag": "restaurant_building",
      "object_type": "building",
      "bounding_box": [400, 350, 580, 650],
      "center_point": [490, 500],
      "approx_sq_ft": 1650,
      "target_dimensions_ft": {
        "width_ft": 30,
        "depth_ft": 55,
        "height_ft": 25
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern 3-story restaurant building, sleek glass and dark metal facade, prominent entrance, outdoor dining terrace on second level, flat roof with subtle parapet, plain white background, no shadows, physically based rendering, high resolution, 30ft wide, 55ft deep, 25ft tall",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion, complex background",
        "meshy_notes": "Emphasize clean architectural details; target 15k-25k poly budget."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Aquarium Building",
      "semantic_tag": "public_aquarium",
      "object_type": "building",
      "bounding_box": [720, 300, 950, 700],
      "center_point": [835, 500],
      "approx_sq_ft": 3600,
      "target_dimensions_ft": {
        "width_ft": 45,
        "depth_ft": 80,
        "height_ft": 35
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern aquarium building, contemporary design with large glass panels, smooth white concrete and blue accents, distinctive curved fish-fin roof element made of perforated metal, prominent entrance, plain white background, no shadows, physically based rendering, high resolution, 45ft wide, 80ft deep, 35ft tall",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion, complex background, fantasy elements",
        "meshy_notes": "Accurately capture the complex roof shape; target 20k-30k poly budget; ensure glass elements are distinct."
      },
      "unity_strategy": "generate_mesh"
    }
  ],
  "prefab_instances": []
}
```