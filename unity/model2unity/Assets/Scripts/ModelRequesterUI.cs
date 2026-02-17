using UnityEngine;
using UnityEngine.UI;
using TMPro;

/// <summary>
/// Simple UI controller for testing the ModelRequester functionality
/// </summary>
public class ModelRequesterUI : MonoBehaviour
{
    [Header("UI References")]
    public Button healthCheckButton;
    public Button searchButton;
    public TMP_InputField searchInput;
    public TMP_Text statusText;
    public TMP_Text resultsText; // Shows current loaded model info
    
    [Header("Progress UI")]
    public Slider progressBar;
    public TMP_Text progressText;
    public GameObject progressContainer; // Optional container to show/hide progress UI
    
    [Header("Model Requester")]
    public ModelRequester modelRequester;
    
    private ModelRequester.SearchResult lastSearchResult;
    private string currentLoadedModel = "None";
    
    private void Start()
    {
        Debug.Log("[ModelRequesterUI] Starting initialization...");
        
        // Find ModelRequester if not assigned
        if (modelRequester == null)
        {
            modelRequester = FindFirstObjectByType<ModelRequester>();
            Debug.Log($"[ModelRequesterUI] Found ModelRequester: {modelRequester != null}");
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
            
            Debug.Log("[ModelRequesterUI] Successfully subscribed to ModelRequester events");
        }
        
        // Initialize progress UI
        SetProgressVisible(false);
        
        UpdateStatusText("Ready - Enter search term and click 'Search' to load a model");
        UpdateResultsText($"Currently loaded model: {currentLoadedModel}");
        
        Debug.Log("[ModelRequesterUI] Initialization complete");
    }
    
    private void OnHealthCheckClicked()
    {
        UpdateStatusText("Testing server connection...");
        if (modelRequester != null)
        {
            modelRequester.TestServerConnectionButton();
        }
        else
        {
            UpdateStatusText("ERROR: ModelRequester not found!");
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
            SetProgressVisible(true);
            modelRequester.SearchAndLoadModel(query);
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
            SetProgressVisible(false);
        }
        else
        {
            UpdateStatusText($"Found {results.count} models for '{results.query}' - Loading first result...");
            UpdateResultsText($"Loading: {results.models[0].name}...");
            SetProgressVisible(true);
            UpdateProgress(0f, "Starting download...");
        }
    }
    
    private void OnDownloadProgress(float progress, string status)
    {
        UpdateProgress(progress, status);
    }
    
    private void OnModelLoaded(string filePath)
    {
        string fileName = System.IO.Path.GetFileName(filePath);
        currentLoadedModel = fileName;
        
        SetProgressVisible(false);
        UpdateResultsText($"Model Loaded: {fileName}\\nSaved to: {filePath}");
        UpdateStatusText($"Success! Model '{fileName}' is loaded and ready to use.");
    }
    
    private void OnErrorReceived(string errorMessage)
    {
        SetProgressVisible(false);
        UpdateStatusText($"ERROR: {errorMessage}");
        UpdateResultsText($"Error: {errorMessage}\\n\\nCurrently loaded: {currentLoadedModel}");
    }
    
    private void SetProgressVisible(bool visible)
    {
        if (progressContainer != null)
        {
            progressContainer.SetActive(visible);
        }
        else
        {
            if (progressBar != null) progressBar.gameObject.SetActive(visible);
            if (progressText != null) progressText.gameObject.SetActive(visible);
        }
    }
    
    private void UpdateProgress(float progress, string statusMessage)
    {
        if (progressBar != null)
        {
            progressBar.value = progress;
        }
        
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
}