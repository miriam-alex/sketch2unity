using UnityEngine;
using System.Collections.Generic;

public class WorldGenerator : MonoBehaviour 
{
    [Header("References")]
    [SerializeField] private Terrain targetTerrain;
    [SerializeField] private PrefabRegistry prefabRegistry;
    [SerializeField] private TerrainRegistry terrainRegistry;
    [SerializeField] private BuildingGenerator buildingGenerator;

    [Header("Input")] 
    [SerializeField] private float prefabScaleFactor = 1;
    
    [Header("Test")] 
    [SerializeField] private bool testGeneration;
    [TextArea(15, 30)]
    [SerializeField] private string jsonInput;
    private float _canvasHeight;
    private float _canvasWidth;
    
    public void Start() {

        if (!testGeneration)
        {
            return;
        }
        
        if (string.IsNullOrWhiteSpace(jsonInput)) {
            Debug.Log("JSON input is null or whitespace");
            return;
        }

        Debug.Log("starting world generator!");

        FullTerrainData data = JsonUtility.FromJson<FullTerrainData>(jsonInput);
        ApplyLayoutData(data);
    }

    public void ApplyLayoutData(FullTerrainData data) {
        if (data == null) {
            Debug.LogWarning("WorldGenerator.ApplyLayoutData received null data.");
            return;
        }

        if (data.site_scale == null || data.site_scale.normalized_canvas == null || data.site_scale.normalized_canvas.Length < 4) {
            Debug.LogWarning("WorldGenerator.ApplyLayoutData received invalid site scale data.");
            return;
        }

        _canvasWidth = data.site_scale.normalized_canvas[2];
        _canvasHeight = data.site_scale.normalized_canvas[3];

        Debug.Log("Applying generated layout to world...");
        PaintTerrain(data);
        PlacePrefabs(data);
        CreateBoxBuildings(data);
    }

    public void CreateBoxBuildings(FullTerrainData data) {
        if (data.generated_objects == null || data.generated_objects.Count == 0) {
            Debug.Log("No generated objects found in layout data.");
            return;
        }

        if (targetTerrain == null) {
            Debug.LogWarning("WorldGenerator.CreateBuildings requires a targetTerrain.");
            return;
        }

        if (data.site_scale == null || data.site_scale.normalized_canvas == null || data.site_scale.normalized_canvas.Length < 4) {
            Debug.LogWarning("WorldGenerator.CreateBuildings received invalid site scale data.");
            return;
        }

        float canvasWidth = data.site_scale.normalized_canvas[2];
        float canvasHeight = data.site_scale.normalized_canvas[3];
        float siteWidthFt = data.site_scale.site_width_ft > 0f ? data.site_scale.site_width_ft : canvasWidth;
        float siteHeightFt = data.site_scale.site_height_ft > 0f ? data.site_scale.site_height_ft : canvasHeight;
        Vector3 terrainSize = targetTerrain.terrainData.size;

        Transform buildingRoot = GetOrCreateBuildingRoot();
        ClearChildren(buildingRoot);

        foreach (var building in data.generated_objects) {
            if (building == null || building.target_dimensions_ft == null || building.center_point == null || building.center_point.Length < 2) {
                continue;
            }

            float centerX = (building.center_point[0] / canvasWidth) * terrainSize.x;
            float centerZ = (building.center_point[1] / canvasHeight) * terrainSize.z;

            float terrainHeight = targetTerrain.SampleHeight(new Vector3(centerX, 0f, centerZ));
            float worldX = targetTerrain.transform.position.x + centerX;
            float worldY = targetTerrain.transform.position.y + terrainHeight;
            float worldZ = targetTerrain.transform.position.z + centerZ;

            float buildingWidth = (building.target_dimensions_ft.width_ft / siteWidthFt) * terrainSize.x;
            float buildingDepth = (building.target_dimensions_ft.depth_ft / siteHeightFt) * terrainSize.z;
            float buildingHeight = (building.target_dimensions_ft.height_ft / siteHeightFt) * terrainSize.x;

            GameObject cube = GameObject.CreatePrimitive(PrimitiveType.Cube);
            cube.name = string.IsNullOrWhiteSpace(building.area_name) ? "GeneratedBuilding" : building.area_name;
            cube.transform.SetParent(buildingRoot, true);
            cube.transform.position = new Vector3(worldX, worldY + (buildingHeight * 0.5f), worldZ);
            cube.transform.localScale = new Vector3(buildingWidth, buildingHeight, buildingDepth);

            if (building.object_type != null)
            {
                Debug.Log($"Created building cube: {cube.name} ({building.object_type})");
            }
        }
    }

    private Transform GetOrCreateBuildingRoot() {
        Transform existing = transform.Find("GeneratedBuildings");
        if (existing != null) {
            return existing;
        }

        GameObject root = new GameObject("GeneratedBuildings");
        root.transform.SetParent(transform, false);
        return root.transform;
    }

    private void ClearChildren(Transform root) {
        for (int i = root.childCount - 1; i >= 0; i--) {
            Transform child = root.GetChild(i);
            if (Application.isPlaying) {
                Destroy(child.gameObject);
            } else {
                DestroyImmediate(child.gameObject);
            }
        }
    }

    private void PaintTerrain(FullTerrainData data) {
        TerrainData tData = targetTerrain.terrainData;
        int res = tData.alphamapResolution;

        // 1. Define your layers explicitly or fetch from Registry
        // Order: 0 = Dirt, 1 = Grass, 2 = Pavement
        tData.terrainLayers = new TerrainLayer[] { 
            terrainRegistry.GetTerrainLayer("dirt"), 
            terrainRegistry.GetTerrainLayer("grass"), 
            terrainRegistry.GetTerrainLayer("pavement") 
        };

        int layerCount = tData.terrainLayers.Length;
        float[,,] map = new float[res, res, layerCount];

        // 2. INITIALIZE: Set everything to 100% Dirt (Index 0)
        for (int y = 0; y < res; y++) {
            for (int x = 0; x < res; x++) {
                map[y, x, 0] = 1f; // Dirt is the background
                for (int l = 1; l < layerCount; l++) {
                    map[y, x, l] = 0f;
                }
            }
        }

        // 3. PAINT ZONES: Overlay Grass and Pavement
        foreach (var zone in data.terrain_zones) {
            // Determine which index to use based on the JSON string
            int targetIndex = 0; 
            if (zone.terrain_type == "grass") targetIndex = 1;
            else if (zone.terrain_type == "pavement") targetIndex = 2;
            else continue; // Skip if it's unknown or "dirt" (already painted)

            // Map JSON 0-1000 coordinates to Alphamap 0-Res coordinates
            int xStart = Mathf.Clamp(Mathf.RoundToInt((zone.bounding_box[0] / 1000f) * res), 0, res);
            int yStart = Mathf.Clamp(Mathf.RoundToInt((zone.bounding_box[1] / 1000f) * res), 0, res);
            int xEnd   = Mathf.Clamp(Mathf.RoundToInt((zone.bounding_box[2] / 1000f) * res), 0, res);
            int yEnd   = Mathf.Clamp(Mathf.RoundToInt((zone.bounding_box[3] / 1000f) * res), 0, res);

            for (int y = yStart; y < yEnd; y++) {
                for (int x = xStart; x < xEnd; x++) {
                    // Wipe existing layers at this pixel
                    for (int l = 0; l < layerCount; l++) map[y, x, l] = 0f;
                    
                    // Set the specific zone color
                    map[y, x, targetIndex] = 1f;
                }
            }
        }

        tData.SetAlphamaps(0, 0, map);
    }
    private void PlacePrefabs(FullTerrainData data) {
        Vector3 terrainSize = targetTerrain.terrainData.size; // e.g., 500m
        
        foreach (var p in data.prefab_instances) {
            GameObject prefab = prefabRegistry.GetPrefab(p.prefab_type);
            if (!prefab) {
                Debug.Log($"missing prefab: {p.prefab_type}");
                continue;
            }

            float xPos = (p.center_point[0] / _canvasWidth) * terrainSize.x;
            float zPos = (p.center_point[1] / _canvasHeight) * terrainSize.z;
    
            // 1. Get the raw terrain height at this coordinate
            float terrainHeight = targetTerrain.SampleHeight(new Vector3(xPos, 0, zPos));

            Vector3 spawnPos = targetTerrain.transform.position + new Vector3(xPos, terrainHeight, zPos);
            GameObject instance = Instantiate(prefab, spawnPos, prefab.transform.rotation);

            // 2. Apply scale first (offset depends on scale!)
            instance.transform.localScale *= prefabScaleFactor;

            // 3. Calculate the Y offset based on the Bounding Box
            // We look for a Renderer to find the visual bottom of the object
            Renderer rend = instance.GetComponentInChildren<Renderer>();
            if (rend != null) {
                // Distance from the pivot (transform.position.y) to the bottom of the bounds
                float bottomOffset = instance.transform.position.y - rend.bounds.min.y;
        
                // Push the instance up by that offset
                instance.transform.position += new Vector3(0, bottomOffset, 0);
            }
        }
    }
}