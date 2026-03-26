using UnityEngine;
using System.Collections.Generic;

public class WorldGenerator : MonoBehaviour 
{
    [Header("References")]
    public Terrain targetTerrain;
    public PrefabRegistry prefabRegistry;
    public TerrainRegistry terrainRegistry;
    public int paintResolution = 1024;

    [Header("Input")] 
    public float prefabScaleFactor = 1;
    
    [TextArea(15, 30)]
    public string jsonInput;
    private float _canvasHeight;
    private float _canvasWidth;
    
    public void Start() {
        FullTerrainData data = JsonUtility.FromJson<FullTerrainData>(jsonInput);
        _canvasWidth = data.site_scale.normalized_canvas[2]; 
        _canvasHeight = data.site_scale.normalized_canvas[3];
        
        Debug.Log("JSON parsed!");
        
        // 1. PAINT TERRAIN
        PaintTerrain(data);
        
        // 2. PLACE PREFABS
        PlacePrefabs(data);
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
            if (!prefab) continue;

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