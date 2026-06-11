using UnityEngine;

public class BuildingGenerator : MonoBehaviour
{
    [Header("Prefabs")]
    [SerializeField] private GameObject groundFloorPrefab;
    [SerializeField] private GameObject upperFloorPrefab;
    [SerializeField] private float upperFloorPrefabZOffset = 0.06f;
    
    [ContextMenu("Generate House")]
    
    public void Generate(Transform parent, Vector3 spawnPos, int baysWide, int baysDeep, int floors, float rotationY, string buildingName)
    {
        if (groundFloorPrefab == null)
        {
            Debug.Log("Ground floor prefab is null.");
            return;
        }
        
        if (upperFloorPrefab == null)
        {
            Debug.Log("Upper floor prefab is null.");
            return;
        }
        
        GameObject buildingRoot = new GameObject(string.IsNullOrEmpty(buildingName) ? "Building_Root" : buildingName);
        buildingRoot.transform.SetParent(parent);
        buildingRoot.transform.position = spawnPos;
        buildingRoot.transform.rotation = Quaternion.Euler(0, rotationY, 0);
        BoxCollider gCollider = groundFloorPrefab.GetComponentInChildren<BoxCollider>();
        BoxCollider uCollider = upperFloorPrefab.GetComponentInChildren<BoxCollider>();
        Vector3 gSize = Vector3.Scale(gCollider.size, groundFloorPrefab.transform.localScale);
        Debug.Log($"gCollider.size: {gCollider.size}");
        Debug.Log($"groundFloorPrefab.transform.localScale: {groundFloorPrefab.transform.localScale}");
        Debug.Log($"gSize: {gSize}");
        Vector3 uSize = Vector3.Scale(uCollider.size, upperFloorPrefab.transform.localScale);
        Debug.Log($"uCollider.size: {uCollider.size}");
        Debug.Log($"upperFloorPrefab.transform.localScale: {upperFloorPrefab.transform.localScale}");
        Debug.Log($"uSize: {uSize}");

        // 3. Calculate Centering Offset
        // We center based on the ground floor's footprint
        Vector3 originOffset = new Vector3(
            (baysWide - 1) * gSize.x * 0.5f,
            0,
            (baysDeep - 1) * gSize.z * 0.5f
        );

        for (int f = 0; f < floors; f++)
        {
            // 4. Create Floor Parent
            GameObject floorRoot = new GameObject($"Floor_{f}");
            floorRoot.transform.SetParent(buildingRoot.transform);
            floorRoot.transform.localPosition = Vector3.zero;
            floorRoot.transform.localRotation = Quaternion.identity;

            for (int w = 0; w < baysWide; w++)
            {
                for (int d = 0; d < baysDeep; d++)
                {
                    bool isGround = (f == 0);
                    GameObject prefab = isGround ? groundFloorPrefab : upperFloorPrefab;
                    
                    // Calculate X and Z based on the loop index and ground size
                    float xPos = w * gSize.x;
                    float zPos = d * gSize.z;
                    
                    // Calculate Y stack height
                    float yStack = isGround ? 0 : gSize.y + ((f - 1) * uSize.y);

                    // 5. Compute Local Position relative to Building Root
                    // We apply the originOffset here to center the building on the spawnPos
                    Vector3 localPos = new Vector3(xPos, yStack, zPos) - originOffset;

                    // Apply your specific Z-tweak for upper floors
                    if (!isGround)
                    {
                        Debug.Log($"original local pos.z: {localPos.z}");
                        localPos.z += upperFloorPrefabZOffset;
                        Debug.Log($"new local pos.z: {localPos.z}");
                    }

                    // 6. Instantiate as child of Floor Root
                    GameObject unit = Instantiate(prefab, floorRoot.transform);
                    unit.transform.localPosition = localPos;
                    // Manual offset so it's facing the right direction. Very much a placeholder!
                    unit.transform.localRotation = Quaternion.identity;
                }
            }
        }
    }
    
    public Renderer GetRenderer()
    {
        GameObject prefab = groundFloorPrefab;
        if (prefab == null) return null;
        Renderer rend = prefab.GetComponentInChildren<Renderer>();
        if (rend == null)
        {
            Debug.LogError($"Prefab {prefab.name} has no Renderer");
            return null;
        }
        Debug.Log($"rend exists n bounds r {rend.bounds.size.x}, {rend.bounds.size.z}");
        return rend;
    }


    public void ClearExisting()
    {
        for (int i = this.transform.childCount - 1; i >= 0; i--)
        {
            DestroyImmediate(this.transform.GetChild(i).gameObject);
        }
    }
}