using UnityEngine;
using UnityEngine.Networking;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine.Events;
using Dummiesman;

public class ModelRequester : MonoBehaviour
{
    [Header("Server Configuration")]
    public string serverBaseUrl = "http://localhost:5002";
    
    [Header("Debug Options")]
    public bool testOnStart = true;
    public bool enableDebugLogs = true;
    
    [Header("Model Import Options")]
    public bool autoImportOBJ = true;
    public Transform modelParent; // Optional parent transform for imported models
    
    // Events for UI updates
    [System.NonSerialized]
    public UnityEvent<SearchResult> OnSearchComplete;
    [System.NonSerialized] 
    public UnityEvent<string> OnModelLoaded; // Changed from OnDownloadComplete
    [System.NonSerialized]
    public UnityEvent<string> OnError;
    [System.NonSerialized]
    public UnityEvent<float, string> OnDownloadProgress; // Progress (0-1), status message
    
    private void Awake()
    {
        // Initialize events early to avoid null reference exceptions
        if (OnSearchComplete == null) OnSearchComplete = new UnityEvent<SearchResult>();
        if (OnModelLoaded == null) OnModelLoaded = new UnityEvent<string>();
        if (OnError == null) OnError = new UnityEvent<string>();
        if (OnDownloadProgress == null) OnDownloadProgress = new UnityEvent<float, string>();
    }
    
    private void Start()
    {
        if (testOnStart)
        {
            Log("ModelRequester starting - testing server connection...");
            StartCoroutine(TestServerConnection());
        }
    }
    
    /// <summary>
    /// Test the server health check endpoint
    /// </summary>
    [ContextMenu("Test Server Connection")]
    public void TestServerConnectionButton()
    {
        StartCoroutine(TestServerConnection());
    }
    
    private IEnumerator TestServerConnection()
    {
        string healthUrl = $"{serverBaseUrl}/health";
        Log($"Requesting health check from: {healthUrl}");
        
        using (UnityWebRequest request = UnityWebRequest.Get(healthUrl))
        {
            // Set timeout to 10 seconds
            request.timeout = 10;
            
            // Send the request and wait for response
            yield return request.SendWebRequest();
            
            // Check for errors
            if (request.result == UnityWebRequest.Result.Success)
            {
                // Parse the response
                string responseText = request.downloadHandler.text;
                Log($"✅ Server Health Check SUCCESS!");
                Log($"Response: {responseText}");
                
                // Try to parse as JSON for better display
                try
                {
                    var healthData = JsonUtility.FromJson<HealthResponse>(responseText);
                    Log($"Server Status: {healthData.status}");
                    Log($"Server Message: {healthData.message}");
                    Log($"Server Version: {healthData.version}");
                }
                catch (System.Exception e)
                {
                    Log($"Could not parse JSON response: {e.Message}");
                }
            }
            else
            {
                // Handle errors
                LogError($"❌ Server Health Check FAILED!");
                LogError($"Error: {request.error}");
                LogError($"Response Code: {request.responseCode}");
                
                if (request.result == UnityWebRequest.Result.ConnectionError)
                {
                    LogError("Connection Error - Is the server running?");
                }
                else if (request.result == UnityWebRequest.Result.ProtocolError)
                {
                    LogError($"Protocol Error - Server returned: {request.responseCode}");
                }
            }
        }
    }
    
    /// <summary>
    /// Request list of all available models from server
    /// </summary>
    [ContextMenu("Get Model List")]
    public void GetModelList()
    {
        Log("GetModelList");
        StartCoroutine(RequestModelList());
    }
    
    private IEnumerator RequestModelList()
    {
        Log("RequestModelList");
        string listUrl = $"{serverBaseUrl}/api/list";
        Log($"Requesting model list from: {listUrl}");
        
        using (UnityWebRequest request = UnityWebRequest.Get(listUrl))
        {
            request.timeout = 10;
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                string responseText = request.downloadHandler.text;
                Log($"Model List SUCCESS!");
                Log($"Available Models Response: {responseText}");
            }
            else
            {
                LogError($"Model List Request FAILED!");
                LogError($"Error: {request.error}");
            }
        }
    }
    
    /// <summary>
    /// Search for models by query and automatically load the first result
    /// </summary>
    public void SearchAndLoadModel(string query)
    {
        Log("SearchAndLoadModel");
        StartCoroutine(RequestModelSearchAndLoad(query));
    }
    
    // Keep old method for compatibility
    public void SearchModels(string query)
    {
        SearchAndLoadModel(query);
    }
    
    private IEnumerator RequestModelSearchAndLoad(string query)
    {
        Log("RequestModelSearchAndLoad");
        string searchUrl = $"{serverBaseUrl}/api/search";
        Log($"Searching for models with query: '{query}'");
        
        // Create JSON payload
        SearchRequest searchData = new SearchRequest { query = query };
        string jsonPayload = JsonUtility.ToJson(searchData);
        
        using (UnityWebRequest request = UnityWebRequest.PostWwwForm(searchUrl, ""))
        {
            // Set the request body to JSON
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(jsonPayload);
            request.uploadHandler = new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = new DownloadHandlerBuffer();
            request.SetRequestHeader("Content-Type", "application/json");
            request.timeout = 10;
            
            yield return request.SendWebRequest();
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                string responseText = request.downloadHandler.text;
                Log($"✅ Model Search SUCCESS!");
                
                // Parse search results
                try
                {
                    SearchResult searchResult = JsonUtility.FromJson<SearchResult>(responseText);
                    Log($"Found {searchResult.count} models for query '{searchResult.query}'");
                    
                    // Notify UI of search results
                    OnSearchComplete?.Invoke(searchResult);
                    
                    if (searchResult.count == 0)
                    {
                        Log($"No models found for '{query}'. Try: cat, dog, house, tree");
                        OnError?.Invoke($"No models found for '{query}'");
                    }
                    else
                    {
                        // Always load the first result
                        string selectedModel = searchResult.models[0].name;
                        Log($"Loading first result: {selectedModel}");
                        StartCoroutine(DownloadAndLoadModel(selectedModel));
                    }
                }
                catch (System.Exception e)
                {
                    LogError($"Failed to parse search results: {e.Message}");
                    OnError?.Invoke($"Search failed: {e.Message}");
                }
            }
            else
            {
                LogError($"❌ Model Search FAILED!");
                LogError($"Error: {request.error}");
                OnError?.Invoke($"Search failed: {request.error}");
            }
        }
    }
    
    /// <summary>
    /// Download and load a specific model file
    /// </summary>
    private IEnumerator DownloadAndLoadModel(string filename)
    {
        string downloadUrl = $"{serverBaseUrl}/api/download/{filename}";
        Log($"Downloading and loading model: {filename}");
        
        OnDownloadProgress?.Invoke(0f, "Starting download...");
        
        using (UnityWebRequest request = UnityWebRequest.Get(downloadUrl))
        {
            request.timeout = 60; // Longer timeout for file downloads
            
            var asyncOp = request.SendWebRequest();
            
            // Track download progress
            while (!asyncOp.isDone)
            {
                float progress = request.downloadProgress;
                OnDownloadProgress?.Invoke(progress, "Downloading model...");
                yield return null;
            }
            
            if (request.result == UnityWebRequest.Result.Success)
            {
                OnDownloadProgress?.Invoke(1f, "Processing file...");
                
                // Save to persistent data path
                string saveDirectory = Path.Combine(Application.persistentDataPath, "models");
                if (!Directory.Exists(saveDirectory))
                {
                    Directory.CreateDirectory(saveDirectory);
                }
                
                string savePath = Path.Combine(saveDirectory, filename);
                
                try
                {
                    File.WriteAllBytes(savePath, request.downloadHandler.data);
                    Log($"✅ Model '{filename}' loaded successfully!");
                    Log($"File saved to: {savePath}");
                    Log($"File size: {request.downloadHandler.data.Length} bytes");
                    
                    // Auto-import OBJ files if enabled
                    if (autoImportOBJ && Path.GetExtension(filename).ToLower() == ".obj")
                    {
                        OnDownloadProgress?.Invoke(1f, "Importing model...");
                        ImportOBJModel(savePath, filename);
                    }
                    
                    OnModelLoaded?.Invoke(savePath);
                }
                catch (System.Exception e)
                {
                    LogError($"Failed to save model: {e.Message}");
                    OnError?.Invoke($"Failed to save model: {e.Message}");
                }
            }
            else
            {
                LogError($"❌ Model Download FAILED!");
                LogError($"Error: {request.error}");
                LogError($"Response Code: {request.responseCode}");
                OnError?.Invoke($"Download failed: {request.error}");
            }
        }
    }
    
    private void Log(string message)
    {
        if (enableDebugLogs)
        {
            Debug.Log($"[ModelRequester] {message}");
        }
    }
    
    private void LogError(string message)
    {
        Debug.LogError($"[ModelRequester] {message}");
    }
    
    /// <summary>
    /// Import an OBJ file into the Unity scene using Runtime OBJ Importer
    /// </summary>
    private void ImportOBJModel(string filePath, string filename)
    {
        try
        {
            Log($"Importing OBJ model: {filename}");
            
            // Create OBJ loader and load the model
            var objLoader = new OBJLoader();
            GameObject importedModel = objLoader.Load(filePath);
            
            if (importedModel != null)
            {
                // Set the name to be more user-friendly
                string modelName = Path.GetFileNameWithoutExtension(filename);
                importedModel.name = $"ImportedModel_{modelName}";
                
                // Position the model at the origin initially
                importedModel.transform.position = Vector3.zero;
                
                // If a parent transform is specified, parent the model to it
                if (modelParent != null)
                {
                    importedModel.transform.SetParent(modelParent);
                    importedModel.transform.localPosition = Vector3.zero;
                }
                
                // Center the model by adjusting its position based on bounds
                CenterModel(importedModel);
                
                Log($"✅ Successfully imported OBJ model '{modelName}' into scene!");
                Log($"Model position: {importedModel.transform.position}");
                
                // You can add additional setup here, such as:
                // - Adding colliders
                // - Setting up materials
                // - Scaling the model
                
            }
            else
            {
                LogError("Failed to import OBJ model - loader returned null");
                OnError?.Invoke("Failed to import OBJ model");
            }
        }
        catch (System.Exception e)
        {
            LogError($"Exception while importing OBJ model: {e.Message}");
            OnError?.Invoke($"Import failed: {e.Message}");
        }
    }
    
    /// <summary>
    /// Center the imported model based on its bounds
    /// </summary>
    private void CenterModel(GameObject model)
    {
        try
        {
            // Get all renderers in the model hierarchy
            Renderer[] renderers = model.GetComponentsInChildren<Renderer>();
            
            if (renderers.Length > 0)
            {
                // Calculate combined bounds
                Bounds combinedBounds = renderers[0].bounds;
                
                for (int i = 1; i < renderers.Length; i++)
                {
                    combinedBounds.Encapsulate(renderers[i].bounds);
                }
                
                // Center the model by offsetting it
                Vector3 centerOffset = -combinedBounds.center;
                model.transform.position += centerOffset;
                
                Log($"Model centered. Bounds: {combinedBounds}, Offset applied: {centerOffset}");
            }
        }
        catch (System.Exception e)
        {
            LogError($"Failed to center model: {e.Message}");
        }
    }
    
    // Data classes for JSON serialization
    [System.Serializable]
    public class HealthResponse
    {
        public string status;
        public string message;
        public string version;
    }
    
    [System.Serializable]
    public class SearchRequest
    {
        public string query;
    }
    
    [System.Serializable]
    public class SearchResult
    {
        public string status;
        public string query;
        public string models_directory;
        public int count;
        public ModelInfo[] models;
    }
    
    [System.Serializable]
    public class ModelInfo
    {
        public string name;
        public string path;
        public long size;
        public string extension;
        public float modified;
    }
}
