namespace PMXClean.ViewModels;

using System.Collections.ObjectModel;
using System.IO;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using PMXClean.Models;
using PMXClean.Services;

/// <summary>
/// ViewModel for the Python file comparison feature.
/// </summary>
public sealed partial class ComparisonViewModel : ObservableObject
{
    private readonly PythonComparisonService _comparisonService = new();

    [ObservableProperty]
    private string _leftPath = string.Empty;

    [ObservableProperty]
    private string _rightPath = string.Empty;

    [ObservableProperty]
    private string _leftLabel = "Source";

    [ObservableProperty]
    private string _rightLabel = "Target";

    [ObservableProperty]
    private ObservableCollection<ComparisonItem> _comparisonItems = [];

    [ObservableProperty]
    private ComparisonItem? _selectedItem;

    [ObservableProperty]
    private FileComparisonResult? _currentFileComparison;

    [ObservableProperty]
    private bool _isComparing;

    [ObservableProperty]
    private string _statusMessage = "Select folders to compare";

    [ObservableProperty]
    private int _totalFiles;

    [ObservableProperty]
    private int _differentFiles;

    [ObservableProperty]
    private int _sameFiles;

    [ObservableProperty]
    private int _leftOnlyFiles;

    [ObservableProperty]
    private int _rightOnlyFiles;

    [ObservableProperty]
    private bool _showOnlyDifferences;

    partial void OnSelectedItemChanged(ComparisonItem? value)
    {
        if (value is null || value.IsFolder)
        {
            CurrentFileComparison = null;
            return;
        }

        // Compare the selected file
        CurrentFileComparison = _comparisonService.CompareFiles(
            value.LeftFullPath,
            value.RightFullPath,
            value.RelativePath);
    }

    partial void OnShowOnlyDifferencesChanged(bool value)
    {
        // Refresh display when filter changes
        if (!string.IsNullOrEmpty(LeftPath) && !string.IsNullOrEmpty(RightPath))
        {
            RefreshComparison();
        }
    }

    [RelayCommand]
    private async Task CompareAsync()
    {
        if (string.IsNullOrEmpty(LeftPath) || string.IsNullOrEmpty(RightPath))
        {
            StatusMessage = "Please select both folders to compare";
            return;
        }

        if (!Directory.Exists(LeftPath))
        {
            StatusMessage = $"Left folder does not exist: {LeftPath}";
            return;
        }

        if (!Directory.Exists(RightPath))
        {
            StatusMessage = $"Right folder does not exist: {RightPath}";
            return;
        }

        IsComparing = true;
        StatusMessage = "Comparing folders...";
        CurrentFileComparison = null;
        SelectedItem = null;

        try
        {
            var items = await Task.Run(() => _comparisonService.CompareDirectories(LeftPath, RightPath));

            ComparisonItems = items;

            // Calculate statistics
            CalculateStatistics(items);

            // Apply filter if needed
            if (ShowOnlyDifferences)
            {
                FilterToDifferencesOnly();
            }

            StatusMessage = $"Comparison complete: {TotalFiles} files ({DifferentFiles} different, {SameFiles} same, {LeftOnlyFiles} left only, {RightOnlyFiles} right only)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error during comparison: {ex.Message}";
        }
        finally
        {
            IsComparing = false;
        }
    }

    [RelayCommand]
    private void RefreshComparison()
    {
        if (!string.IsNullOrEmpty(LeftPath) && !string.IsNullOrEmpty(RightPath))
        {
            _ = CompareAsync();
        }
    }

    [RelayCommand]
    private void ExpandAll()
    {
        SetExpandedState(ComparisonItems, true);
    }

    [RelayCommand]
    private void CollapseAll()
    {
        SetExpandedState(ComparisonItems, false);
    }

    [RelayCommand]
    private void ExpandDifferencesOnly()
    {
        SetExpandedState(ComparisonItems, false);
        ExpandItemsWithDifferences(ComparisonItems);
    }

    private static void SetExpandedState(ObservableCollection<ComparisonItem> items, bool expanded)
    {
        foreach (var item in items)
        {
            if (item.IsFolder)
            {
                item.IsExpanded = expanded;
                SetExpandedState(item.Children, expanded);
            }
        }
    }

    private static void ExpandItemsWithDifferences(ObservableCollection<ComparisonItem> items)
    {
        foreach (var item in items)
        {
            if (item.IsFolder && item.Status == FileComparisonStatus.ContainsDifferences)
            {
                item.IsExpanded = true;
                ExpandItemsWithDifferences(item.Children);
            }
        }
    }

    private void CalculateStatistics(ObservableCollection<ComparisonItem> items)
    {
        int total = 0, different = 0, same = 0, leftOnly = 0, rightOnly = 0;
        CountFiles(items, ref total, ref different, ref same, ref leftOnly, ref rightOnly);

        TotalFiles = total;
        DifferentFiles = different;
        SameFiles = same;
        LeftOnlyFiles = leftOnly;
        RightOnlyFiles = rightOnly;
    }

    private static void CountFiles(ObservableCollection<ComparisonItem> items, 
        ref int total, ref int different, ref int same, ref int leftOnly, ref int rightOnly)
    {
        foreach (var item in items)
        {
            if (item.IsFolder)
            {
                CountFiles(item.Children, ref total, ref different, ref same, ref leftOnly, ref rightOnly);
            }
            else
            {
                total++;
                switch (item.Status)
                {
                    case FileComparisonStatus.Same:
                        same++;
                        break;
                    case FileComparisonStatus.Different:
                        different++;
                        break;
                    case FileComparisonStatus.LeftOnly:
                        leftOnly++;
                        break;
                    case FileComparisonStatus.RightOnly:
                        rightOnly++;
                        break;
                }
            }
        }
    }

    private void FilterToDifferencesOnly()
    {
        FilterItems(ComparisonItems);
    }

    private static void FilterItems(ObservableCollection<ComparisonItem> items)
    {
        // Remove items that are the same (but keep folders with differences)
        var toRemove = items.Where(i => !i.IsFolder && i.Status == FileComparisonStatus.Same).ToList();
        foreach (var item in toRemove)
        {
            items.Remove(item);
        }

        // Process folders
        foreach (var folder in items.Where(i => i.IsFolder).ToList())
        {
            FilterItems(folder.Children);

            // Remove empty folders
            if (folder.Children.Count == 0)
            {
                items.Remove(folder);
            }
        }
    }

    /// <summary>
    /// Sets up comparison between a version folder and installed path.
    /// </summary>
    public void SetupComparison(string leftPath, string rightPath, string leftLabel, string rightLabel)
    {
        LeftPath = leftPath;
        RightPath = rightPath;
        LeftLabel = leftLabel;
        RightLabel = rightLabel;
        ComparisonItems.Clear();
        CurrentFileComparison = null;
        SelectedItem = null;
        StatusMessage = "Ready to compare";
    }
}
