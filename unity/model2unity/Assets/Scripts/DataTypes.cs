using UnityEngine;
using System.Collections.Generic;

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
    public List<TerrainZone> terrain_zones;
    public List<PrefabInstance> prefab_instances;
}