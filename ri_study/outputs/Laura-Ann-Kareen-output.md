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
      "area_name": "Main Plaza",
      "semantic_tag": "Public Gathering Space",
      "terrain_type": "plaza",
      "bounding_box": [0, 0, 1000, 1000],
      "approx_sq_ft": 16350,
      "unity_strategy": "paint_terrain"
    }
  ],
  "generated_objects": [
    {
      "area_name": "Museum of History",
      "semantic_tag": "Cultural Building",
      "object_type": "building",
      "bounding_box": [550, 0, 950, 400],
      "center_point": [750, 200],
      "approx_sq_ft": 4800,
      "target_dimensions_ft": {
        "width_ft": 60,
        "depth_ft": 80,
        "height_ft": 18
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern single-story museum building, large brick facade with integrated display windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 10k–20k poly budget; bake diffuse and normal maps separately. Footprint is 60ft x 80ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Left Shop 1",
      "semantic_tag": "Retail Store",
      "object_type": "building",
      "bounding_box": [250, 0, 350, 200],
      "center_point": [300, 100],
      "approx_sq_ft": 600,
      "target_dimensions_ft": {
        "width_ft": 30,
        "depth_ft": 20,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic single-story retail building, brick facade with large storefront windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 5k–10k poly budget; bake diffuse and normal maps separately. Footprint is 30ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Left Shop 2",
      "semantic_tag": "Retail Store",
      "object_type": "building",
      "bounding_box": [350, 0, 450, 200],
      "center_point": [400, 100],
      "approx_sq_ft": 600,
      "target_dimensions_ft": {
        "width_ft": 30,
        "depth_ft": 20,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic single-story retail building, brick facade with large storefront windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 5k–10k poly budget; bake diffuse and normal maps separately. Footprint is 30ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Left Shop 3",
      "semantic_tag": "Retail Store",
      "object_type": "building",
      "bounding_box": [450, 0, 550, 200],
      "center_point": [500, 100],
      "approx_sq_ft": 600,
      "target_dimensions_ft": {
        "width_ft": 30,
        "depth_ft": 20,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic single-story retail building, brick facade with large storefront windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 5k–10k poly budget; bake diffuse and normal maps separately. Footprint is 30ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Central Shop 1",
      "semantic_tag": "Retail Store",
      "object_type": "building",
      "bounding_box": [250, 250, 350, 350],
      "center_point": [300, 300],
      "approx_sq_ft": 300,
      "target_dimensions_ft": {
        "width_ft": 15,
        "depth_ft": 20,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic small single-story retail building, brick facade with large storefront windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 3k–5k poly budget; bake diffuse and normal maps separately. Footprint is 15ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Central Shop 2",
      "semantic_tag": "Retail Store",
      "object_type": "building",
      "bounding_box": [250, 350, 350, 450],
      "center_point": [300, 400],
      "approx_sq_ft": 300,
      "target_dimensions_ft": {
        "width_ft": 15,
        "depth_ft": 20,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic small single-story retail building, brick facade with large storefront windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 3k–5k poly budget; bake diffuse and normal maps separately. Footprint is 15ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Central Shop 3",
      "semantic_tag": "Retail Store",
      "object_type": "building",
      "bounding_box": [250, 450, 350, 550],
      "center_point": [300, 500],
      "approx_sq_ft": 300,
      "target_dimensions_ft": {
        "width_ft": 15,
        "depth_ft": 20,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic small single-story retail building, brick facade with large storefront windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 3k–5k poly budget; bake diffuse and normal maps separately. Footprint is 15ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "24 HR Chicken Shop",
      "semantic_tag": "Restaurant Building",
      "object_type": "building",
      "bounding_box": [450, 600, 650, 750],
      "center_point": [550, 675],
      "approx_sq_ft": 900,
      "target_dimensions_ft": {
        "width_ft": 22.5,
        "depth_ft": 40,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic single-story fast-food restaurant building, brick facade with large service windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 5k–10k poly budget; bake diffuse and normal maps separately. Footprint is 22.5ft x 40ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Right Shop 1",
      "semantic_tag": "Retail Store",
      "object_type": "building",
      "bounding_box": [650, 600, 750, 750],
      "center_point": [700, 675],
      "approx_sq_ft": 450,
      "target_dimensions_ft": {
        "width_ft": 22.5,
        "depth_ft": 20,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic small single-story retail building, brick facade with large storefront windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 3k–5k poly budget; bake diffuse and normal maps separately. Footprint is 22.5ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Right Shop 2",
      "semantic_tag": "Retail Store",
      "object_type": "building",
      "bounding_box": [750, 600, 850, 750],
      "center_point": [800, 675],
      "approx_sq_ft": 450,
      "target_dimensions_ft": {
        "width_ft": 22.5,
        "depth_ft": 20,
        "height_ft": 15
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic small single-story retail building, brick facade with large storefront windows, flat roof with parapet, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 3k–5k poly budget; bake diffuse and normal maps separately. Footprint is 22.5ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Bridge Escalator",
      "semantic_tag": "Transportation Structure",
      "object_type": "structure",
      "bounding_box": [100, 250, 200, 400],
      "center_point": [150, 325],
      "approx_sq_ft": 450,
      "target_dimensions_ft": {
        "width_ft": 22.5,
        "depth_ft": 20,
        "height_ft": 25
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern public escalator structure, enclosed with glass panels and a metal frame, connecting to an upper bridge level, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements for the base structure.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 5k–10k poly budget; bake diffuse and normal maps separately. Footprint is 22.5ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Bridge Elevator",
      "semantic_tag": "Transportation Structure",
      "object_type": "structure",
      "bounding_box": [100, 500, 200, 550],
      "center_point": [150, 525],
      "approx_sq_ft": 150,
      "target_dimensions_ft": {
        "width_ft": 7.5,
        "depth_ft": 20,
        "height_ft": 30
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern public elevator shaft structure, glass and metal enclosure, connecting to an upper bridge level, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements for the base structure.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 3k–5k poly budget; bake diffuse and normal maps separately. Footprint is 7.5ft x 20ft."
      },
      "unity_strategy": "generate_mesh"
    },
    {
      "area_name": "Tram Station",
      "semantic_tag": "Transportation Hub",
      "object_type": "structure",
      "bounding_box": [200, 700, 700, 950],
      "center_point": [450, 825],
      "approx_sq_ft": 3750,
      "target_dimensions_ft": {
        "width_ft": 37.5,
        "depth_ft": 100,
        "height_ft": 25
      },
      "image_gen_prompt": {
        "prompt": "Isometric 3/4 view of a photorealistic modern tram station structure, multi-story with a covered platform, brick base with large windows and metal roof, plain white background, no shadows, no people, physically based rendering, high resolution. Architectural style incorporates existing power plant bricks and contemporary window elements.",
        "negative_prompt": "humans, vehicles, trees, ground plane, sky, shadows, text, signage, watermark, blurry, cut off edges, fish-eye lens, wide-angle distortion",
        "meshy_notes": "Use image-to-3D with multiview reconstruction enabled; target 15k–25k poly budget; bake diffuse and normal maps separately. Footprint is 37.5ft x 100ft."
      },
      "unity_strategy": "generate_mesh"
    }
  ],
  "prefab_instances": []
}
```