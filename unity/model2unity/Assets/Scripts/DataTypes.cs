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
public class TerrainZone
{
    public string area_name;
    public string terrain_type;
    public int[] bounding_box; // [xMin, yMin, xMax, yMax]
}

[System.Serializable]
public class SiteScale {
    public int[] normalized_canvas; // [0, 0, 1000, 1000]
    public float site_width_ft;
    public float site_height_ft;
    public int[][] lot_boundary;
    public string scale_note;
}

[System.Serializable]
public class PrefabInstance {
    public string area_name;
    public string prefab_type;
    public int[] center_point;
    public float rotation_deg;
    public float scale_multiplier;
}

[System.Serializable]
public class FullTerrainData {
    public SiteScale site_scale;
    public List<GeneratedObject> generated_objects;
    public List<TerrainZone> terrain_zones;
    public List<PrefabInstance> prefab_instances;
}