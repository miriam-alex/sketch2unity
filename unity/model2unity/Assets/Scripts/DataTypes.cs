using UnityEngine;
using System.Collections.Generic;

[System.Serializable]
public class TargetDimensionsFt
{
    public float width_ft;
    public float depth_ft;
    public float height_ft;
}

[System.Serializable]
public class GeneratedObject
{
    public string area_name;
    public string semantic_tag;
    public string object_type;
    public int[] bounding_box;
    public int[] center_point;
    public float approx_sq_ft;
    public TargetDimensionsFt target_dimensions_ft;
    public string unity_strategy;
}

[System.Serializable]
public class GeneratedBuilding
{
    public string area_name;
    public string semantic_tag;
    public int[] bounding_box;
    public int[] center_point;
    public float rotation_y_deg;
    public float approx_sq_ft;
    public string unity_strategy;
}

[System.Serializable]
public class TerrainZone
{
    public string area_name;
    public string semantic_tag; // Added for completeness
    public string terrain_type;
    public int[] bounding_box; 
    public float approx_sq_ft;
    public string unity_strategy;
}

[System.Serializable]
public class SiteScale {
    public int[] normalized_canvas; 
    public float site_width_ft;
    public float site_height_ft;
    public float[][] lot_boundary; // Changed to float[][] for precision
    public string scale_note;
}

[System.Serializable]
public class PrefabInstance {
    public string area_name;
    public string semantic_tag;
    public string prefab_type;
    public int[] center_point;
    public int[] footprint_box; // Added from JSON
    public float rotation_deg;
    public float scale_multiplier;
    public string unity_strategy;
}

[System.Serializable]
public class FullTerrainData {
    public SiteScale site_scale;
    public List<TerrainZone> terrain_zones;
    public List<GeneratedBuilding> generated_buildings; // Mapped to your JSON example
    public List<GeneratedObject> generated_objects;     // For the "box" buildings
    public List<PrefabInstance> prefab_instances;
}