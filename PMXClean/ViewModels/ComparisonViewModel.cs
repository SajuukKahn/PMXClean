namespace PMXClean.ViewModels;

using System.Collections.ObjectModel;
using System.IO;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using PMXClean.Models;
using PMXClean.Services;

/// <summary>
/// ViewModel for the file comparison feature (Python and JSON files).
/// </summary>
public sealed partial class ComparisonViewModel : ObservableObject
{
    /// <summary>
    /// Action to invoke when a comparison is started.
    /// </summary>
    public Action? OnComparisonStarted { get; set; }

    [ObservableProperty]
    public partial string LeftPath { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string RightPath { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string LeftLabel { get; set; } = "Source";

    [ObservableProperty]
    public partial string RightLabel { get; set; } = "Target";

    [ObservableProperty]
    public partial ObservableCollection<ComparisonItem> ComparisonItems { get; set; } = [];

    [ObservableProperty]
    public partial ComparisonItem? SelectedItem { get; set; }

    [ObservableProperty]
    public partial FileComparisonResult? CurrentFileComparison { get; set; }

    [ObservableProperty]
    public partial bool IsComparing { get; set; }

    [ObservableProperty]
    public partial string StatusMessage { get; set; } = "Select folders to compare";

    [ObservableProperty]
    public partial int TotalFiles { get; set; }

    [ObservableProperty]
    public partial int DifferentFiles { get; set; }

    [ObservableProperty]
    public partial int SameFiles { get; set; }

    [ObservableProperty]
    public partial int LeftOnlyFiles { get; set; }

    [ObservableProperty]
    public partial int RightOnlyFiles { get; set; }

    [ObservableProperty]
    public partial bool ShowOnlyDifferences { get; set; }

    partial void OnSelectedItemChanged(ComparisonItem? value)
    {
        if (value is null || value.IsFolder)
        {
            CurrentFileComparison = null;
            return;
        }

        // Compare the selected file
        CurrentFileComparison = FileComparisonService.CompareFiles(
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

        // Notify that comparison has started
        OnComparisonStarted?.Invoke();

        try
        {
            var items = await Task.Run(() => FileComparisonService.CompareDirectories(LeftPath, RightPath));

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

    #region Backup-to-Backup Comparison

    /// <summary>
    /// Left backup for backup-to-backup comparison.
    /// </summary>
    [ObservableProperty]
    public partial MachineBackupInfo? LeftBackup { get; set; }

    /// <summary>
    /// Right backup for backup-to-backup comparison.
    /// </summary>
    [ObservableProperty]
    public partial MachineBackupInfo? RightBackup { get; set; }

    /// <summary>
    /// Whether we're in backup comparison mode (vs version comparison mode).
    /// </summary>
    public bool IsBackupComparisonMode => LeftBackup is not null && RightBackup is not null;

    /// <summary>
    /// Whether both backups are loaded and ready for comparison.
    /// </summary>
    public bool CanCompareBackups => LeftBackup is not null && RightBackup is not null;

    /// <summary>
    /// Whether the left backup can be swapped with the right backup.
    /// </summary>
    public bool CanSwapBackups => LeftBackup is not null || RightBackup is not null;

    partial void OnLeftBackupChanged(MachineBackupInfo? value)
    {
        OnPropertyChanged(nameof(IsBackupComparisonMode));
        OnPropertyChanged(nameof(CanCompareBackups));
        OnPropertyChanged(nameof(CanSwapBackups));
        CompareBackupsCommand.NotifyCanExecuteChanged();
        SwapBackupsCommand.NotifyCanExecuteChanged();

        if (value is not null)
        {
            LeftLabel = value.DisplayName;
            LeftPath = value.ExtractedPath;
        }
    }

    partial void OnRightBackupChanged(MachineBackupInfo? value)
    {
        OnPropertyChanged(nameof(IsBackupComparisonMode));
        OnPropertyChanged(nameof(CanCompareBackups));
        OnPropertyChanged(nameof(CanSwapBackups));
        CompareBackupsCommand.NotifyCanExecuteChanged();
        SwapBackupsCommand.NotifyCanExecuteChanged();

        if (value is not null)
        {
            RightLabel = value.DisplayName;
            RightPath = value.ExtractedPath;
        }
    }

    /// <summary>
    /// Loads a .machine backup as the left comparison source.
    /// </summary>
    [RelayCommand]
    private async Task LoadLeftBackupAsync()
    {
        var dialog = new Microsoft.Win32.OpenFileDialog
        {
            Title = "Select Left Backup",
            Filter = "Machine Backup Files (*.machine)|*.machine|All Files (*.*)|*.*",
            FilterIndex = 1
        };

        if (dialog.ShowDialog() == true)
        {
            await LoadLeftBackupFromPathAsync(dialog.FileName);
        }
    }

    /// <summary>
    /// Loads a .machine backup as the right comparison source.
    /// </summary>
    [RelayCommand]
    private async Task LoadRightBackupAsync()
    {
        var dialog = new Microsoft.Win32.OpenFileDialog
        {
            Title = "Select Right Backup",
            Filter = "Machine Backup Files (*.machine)|*.machine|All Files (*.*)|*.*",
            FilterIndex = 1
        };

        if (dialog.ShowDialog() == true)
        {
            await LoadRightBackupFromPathAsync(dialog.FileName);
        }
    }

    /// <summary>
    /// Loads a backup from path as the left source.
    /// </summary>
    public async Task LoadLeftBackupFromPathAsync(string filePath)
    {
        if (string.IsNullOrEmpty(filePath) || !File.Exists(filePath))
        {
            StatusMessage = "Error: Invalid backup file path";
            return;
        }

        try
        {
            StatusMessage = "Loading left backup...";

            // Clean up existing left backup
            if (LeftBackup is not null)
            {
                await MachineBackupService.CleanupTempFolderAsync(LeftBackup.ExtractedPath);
            }

            LeftBackup = await MachineBackupService.LoadBackupAsync(filePath);
            StatusMessage = $"Left backup loaded: {LeftBackup.DisplayName}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error loading left backup: {ex.Message}";
        }
    }

    /// <summary>
    /// Loads a backup from path as the right source.
    /// </summary>
    public async Task LoadRightBackupFromPathAsync(string filePath)
    {
        if (string.IsNullOrEmpty(filePath) || !File.Exists(filePath))
        {
            StatusMessage = "Error: Invalid backup file path";
            return;
        }

        try
        {
            StatusMessage = "Loading right backup...";

            // Clean up existing right backup
            if (RightBackup is not null)
            {
                await MachineBackupService.CleanupTempFolderAsync(RightBackup.ExtractedPath);
            }

            RightBackup = await MachineBackupService.LoadBackupAsync(filePath);
            StatusMessage = $"Right backup loaded: {RightBackup.DisplayName}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error loading right backup: {ex.Message}";
        }
    }

    /// <summary>
    /// Compares the two loaded backups.
    /// </summary>
    [RelayCommand(CanExecute = nameof(CanCompareBackups))]
    private async Task CompareBackupsAsync()
    {
        if (LeftBackup is null || RightBackup is null)
        {
            StatusMessage = "Please load both backups to compare";
            return;
        }

        // Set up paths and run comparison
        LeftPath = LeftBackup.ExtractedPath;
        RightPath = RightBackup.ExtractedPath;
        LeftLabel = LeftBackup.DisplayName;
        RightLabel = RightBackup.DisplayName;

        await CompareAsync();
    }

    /// <summary>
    /// Swaps the left and right backups.
    /// </summary>
    [RelayCommand(CanExecute = nameof(CanSwapBackups))]
    private void SwapBackups()
    {
        (LeftBackup, RightBackup) = (RightBackup, LeftBackup);
        (LeftPath, RightPath) = (RightPath, LeftPath);
        (LeftLabel, RightLabel) = (RightLabel, LeftLabel);

        StatusMessage = "Backups swapped";
    }

    /// <summary>
    /// Clears both loaded backups and cleans up temp folders.
    /// </summary>
    [RelayCommand]
    private async Task ClearBackupsAsync()
    {
        if (LeftBackup is not null)
        {
            await MachineBackupService.CleanupTempFolderAsync(LeftBackup.ExtractedPath);
            LeftBackup = null;
        }

        if (RightBackup is not null)
        {
            await MachineBackupService.CleanupTempFolderAsync(RightBackup.ExtractedPath);
            RightBackup = null;
        }

        LeftPath = string.Empty;
        RightPath = string.Empty;
        LeftLabel = "Left";
        RightLabel = "Right";
        ComparisonItems.Clear();
        CurrentFileComparison = null;
        StatusMessage = "Backups cleared";
    }

    /// <summary>
    /// Cleans up both backup temp folders. Should be called when the comparison is closed.
    /// </summary>
    public async Task CleanupBackupsAsync()
    {
        if (LeftBackup is not null)
        {
            await MachineBackupService.CleanupTempFolderAsync(LeftBackup.ExtractedPath);
            LeftBackup = null;
        }

        if (RightBackup is not null)
        {
            await MachineBackupService.CleanupTempFolderAsync(RightBackup.ExtractedPath);
            RightBackup = null;
        }
    }

    #endregion
}
