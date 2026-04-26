using UnityEngine;

public class BuildingGenerator : MonoBehaviour
{
    [Header("Prefabs")]
    public GameObject groundFloorPrefab;
    public GameObject upperFloorPrefab;
    public float upperFloorPrefabZOffset = 0.06f;

    [Header("Dimensions")]
    [Range(1, 10)] public int width = 3;   // n units
    [Range(1, 10)] public int floors = 2;  // m floors

    [ContextMenu("Generate House")]

    void Start()
    {
        Generate();
    }

    public void Generate()
    {
        ClearExisting();

        if (groundFloorPrefab == null || upperFloorPrefab == null) return;

        BoxCollider gCollider = groundFloorPrefab.GetComponentInChildren<BoxCollider>();
        BoxCollider uCollider = upperFloorPrefab.GetComponentInChildren<BoxCollider>();
        Vector3 gSize = Vector3.Scale(gCollider.size, groundFloorPrefab.transform.localScale);
        Vector3 uSize = Vector3.Scale(uCollider.size, upperFloorPrefab.transform.localScale);

        for (int f = 0; f < floors; f++)
        {
            for (int w = 0; w < width; w++)
            {
                GameObject prefab = (f == 0) ? groundFloorPrefab : upperFloorPrefab;
                Vector3 currentSize = (f == 0) ? gSize : uSize;

                float xPos = w * gSize.x;
                float yStack = (f == 0) ? 0 : gSize.y + ((f - 1) * uSize.y);
                
                Vector3 spawnPos = transform.position + new Vector3(xPos, yStack, (f==0) ? 0 : upperFloorPrefabZOffset);

                GameObject unit = Instantiate(prefab, spawnPos, Quaternion.identity);
                unit.transform.parent = this.transform;
            }
        }
    }

    public void ClearExisting()
    {
        for (int i = this.transform.childCount - 1; i >= 0; i--)
        {
            DestroyImmediate(this.transform.GetChild(i).gameObject);
        }
    }
}