using UnityEngine;
using UnityEngine.UI;
using TMPro;
using System.IO;

/// <summary>
/// Simple UI controller for testing the ModelRequester functionality
/// </summary>
public class ModelRequesterUI : MonoBehaviour
{
    [Header("UI References")]
    public Button healthCheckButton;
    public Button searchButton;
    public Button generateLayoutButton;
    public TMP_InputField searchInput;
    public TMP_Text statusText;
    public TMP_Text resultsText; // Shows current loaded model info
    
    [Header("Progress UI")]
    public TMP_Text progressText;
    public TMP_Text timerText; // To display the timer
    
    [Header("Model Requester")]
    public ModelRequester modelRequester;
    public WorldGenerator worldGenerator;
    
    private ModelRequester.SearchResult lastSearchResult;
    private string currentLoadedModel = "None";
    private float requestStartTime;
    private bool isRequestRunning = false;
    
    private void Start()
    {
        // Debug.Log("[ModelRequesterUI] Starting initialization...");
        
        // Find ModelRequester if not assigned
        if (modelRequester == null)
        {
            modelRequester = FindFirstObjectByType<ModelRequester>();
            Debug.Log($"[ModelRequesterUI] Found ModelRequester: {modelRequester != null}");
        }

        if (worldGenerator == null)
        {
            worldGenerator = FindFirstObjectByType<WorldGenerator>();
            Debug.Log($"[ModelRequesterUI] Found WorldGenerator: {worldGenerator != null}");
        }

        // Set up button listeners first
        if (healthCheckButton != null)
        {
            healthCheckButton.onClick.AddListener(OnHealthCheckClicked);
        }

        if (searchButton != null)
        {
            searchButton.onClick.AddListener(OnSearchClicked);
        }

        if (generateLayoutButton != null)
        {
            generateLayoutButton.onClick.AddListener(OnGenerateLayoutClicked);
        }
        
        // initialize text
        if (progressText != null)
        {
            progressText.text = "";
        }
        
        if (timerText != null)
        {
            timerText.text = "";
        }

        
        // Subscribe to events with null checks (after UI is set up)
        if (modelRequester != null)
        {
            if (modelRequester.OnSearchComplete != null)
                modelRequester.OnSearchComplete.AddListener(OnSearchResultsReceived);
            if (modelRequester.OnModelLoaded != null)
                modelRequester.OnModelLoaded.AddListener(OnModelLoaded);
            if (modelRequester.OnError != null)
                modelRequester.OnError.AddListener(OnErrorReceived);
            if (modelRequester.OnDownloadProgress != null)
                modelRequester.OnDownloadProgress.AddListener(OnDownloadProgress);
            if (modelRequester.OnHealthCheckComplete != null)
                modelRequester.OnHealthCheckComplete.AddListener(OnHealthCheckComplete);
            if (modelRequester.OnLayoutGenerated != null)
                modelRequester.OnLayoutGenerated.AddListener(OnLayoutGenerated);
            
            Debug.Log("[ModelRequesterUI] Successfully subscribed to ModelRequester events");
        }
        
        
        UpdateStatusText("Ready - Search a model or click 'Generate Layout' to run sketch prompting");
        UpdateResultsText($"Currently loaded model: {currentLoadedModel}");
        
        Debug.Log("[ModelRequesterUI] Initialization complete");
    }
    
    private void OnHealthCheckClicked()
    {
        UpdateStatusText("Testing server connection...");
        UpdateResultsText("Pinging server...");
        if (modelRequester != null)
        {
            modelRequester.TestServerConnectionButton();
        }
        else
        {
            UpdateStatusText("ERROR: ModelRequester not found!");
        }
    }
    
    private void OnHealthCheckComplete(bool success, string message)
    {
        if (success)
        {
            UpdateStatusText(message);
            UpdateResultsText("Server is responsive.");
        }
        else
        {
            UpdateStatusText($"Health Check Failed: {message}");
            UpdateResultsText("Server did not respond.");
        }
    }
    
    private void OnSearchClicked()
    {
        Debug.Log("OnSearchClicked");
        string query = searchInput != null ? searchInput.text.Trim() : "cat";
        
        if (string.IsNullOrEmpty(query))
        {
            UpdateStatusText("ERROR: Please enter a search term!");
            return;
        }
        
        UpdateStatusText($"Searching and loading: {query}...");
        UpdateResultsText("Searching for model...");
        
        if (modelRequester != null)
        {
            Debug.Log("progress should be visible here?");
            isRequestRunning = true;
            requestStartTime = Time.time;
            modelRequester.SearchAndLoadModel(query);
        }
        else
        {
            UpdateStatusText("ERROR: ModelRequester not found!");
        }
    }

    public void OnGenerateLayoutClicked()
    {
        UpdateStatusText("Generating layout - select a sketch in the Python file picker...");
        UpdateResultsText("Waiting for sketch selection and layout generation...");

        if (modelRequester != null)
        {
            UpdateProgress(0f, "Waiting for sketch selection...");
            isRequestRunning = true;
            requestStartTime = Time.time;
            modelRequester.GenerateLayoutFromSketchButton();
        }
        else
        {
            UpdateStatusText("ERROR: ModelRequester not found!");
        }
    }
    
    private void OnSearchResultsReceived(ModelRequester.SearchResult results)
    {
        lastSearchResult = results;
        
        if (results.count == 0)
        {
            UpdateStatusText($"No models found for '{results.query}'");
            UpdateResultsText($"No models found for '{results.query}'\\n\\nTry searching for: cat, dog, house, tree");
        }
        else
        {
            UpdateStatusText($"Found {results.count} models for '{results.query}' - Loading first result...");
            UpdateResultsText($"Loading: {results.models[0].name}...");
            UpdateProgress(0f, "Starting download...");
        }
    }
    
    private void OnDownloadProgress(float progress, string status)
    {
        UpdateProgress(progress, status);
        UpdateResultsText($"{status}...");
    }
    
    private void OnModelLoaded(string filePath)
    {
        string fileName = System.IO.Path.GetFileName(filePath);
        currentLoadedModel = fileName;
        
        isRequestRunning = false;
        UpdateResultsText($"Model Loaded: {fileName}\\nSaved to: {filePath}");
        UpdateStatusText($"Success! Model '{fileName}' is loaded and ready to use.");
    }

    private void OnLayoutGenerated(string responseJson)
    {
        isRequestRunning = false;
        try
        {
            LayoutResponseEnvelope response = JsonUtility.FromJson<LayoutResponseEnvelope>(responseJson);
            int terrainZoneCount = response.layout != null && response.layout.terrain_zones != null
                ? response.layout.terrain_zones.Count
                : 0;
            int prefabCount = response.layout != null && response.layout.prefab_instances != null
                ? response.layout.prefab_instances.Count
                : 0;

            if (worldGenerator != null && response.layout != null)
            {
                worldGenerator.ApplyLayoutData(response.layout);
				string filePath = Path.Combine(Application.persistentDataPath, "CurrentResponseLayout.txt");
        		// Write the string to the file
        		File.WriteAllText(filePath, responseJson);
        		Debug.Log($"Layout data successfully saved to: {filePath}");
            }
            else if (worldGenerator == null)
            {
                Debug.LogWarning("[ModelRequesterUI] WorldGenerator not found; skipping terrain and prefab placement.");
            }

            UpdateStatusText("Layout generation complete.");
            UpdateResultsText(
                $"Layout Generated\nTerrain Zones: {terrainZoneCount}\nPrefabs: {prefabCount}\nSketch: {response.selected_sketch}"
            );
        }
        catch (System.Exception e)
        {
            UpdateStatusText("Layout generated, but UI parsing failed.");
            Debug.LogError($"Raw response:\n{responseJson}");
			Debug.LogError($"Parse error: {e.Message}");
        }
    }
    
    private void OnErrorReceived(string errorMessage)
    {
        isRequestRunning = false;
        UpdateStatusText($"ERROR: {errorMessage}");
        UpdateResultsText($"Error: {errorMessage}\\n\\nCurrently loaded: {currentLoadedModel}");
    }
    
    private void UpdateProgress(float progress, string statusMessage)
    {
        if (progressText != null)
        {
            int percentage = Mathf.RoundToInt(progress * 100);
            progressText.text = $"{statusMessage} ({percentage}%)"; 
        }
    }
    
    private void UpdateStatusText(string message)
    {
        if (statusText != null)
        {
            statusText.text = $"[{System.DateTime.Now:HH:mm:ss}] {message}";
        }
        Debug.Log($"[ModelRequesterUI] {message}");
    }
    
    private void UpdateResultsText(string message)
    {
        if (resultsText != null)
        {
            resultsText.text = message;
        }
    }

    private void Update()
    {
        if (isRequestRunning)
        {
            float elapsedTime = Time.time - requestStartTime;
            if (timerText != null)
            {
                timerText.text = $"Time: {elapsedTime:F2}s";
            }
        }
    }

    [System.Serializable]
    private class LayoutResponseEnvelope
    {
        public string status;
        public string message;
        public string selected_sketch;
        public FullTerrainData layout;
    }
}