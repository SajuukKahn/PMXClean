namespace PMXClean.Models;

using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

/// <summary>
/// Represents a file or folder in the comparison tree.
/// </summary>
public sealed partial class ComparisonItem : ObservableObject
{
    [ObservableProperty]
    private string _name = string.Empty;

    [ObservableProperty]
    private string _relativePath = string.Empty;

    [ObservableProperty]
    private string? _leftFullPath;

    [ObservableProperty]
    private string? _rightFullPath;

    [ObservableProperty]
    private bool _isFolder;

    [ObservableProperty]
    private bool _isExpanded;

    [ObservableProperty]
    private bool _isSelected;

    [ObservableProperty]
    private FileComparisonStatus _status = FileComparisonStatus.Same;

    [ObservableProperty]
    private bool _isLocked;

    [ObservableProperty]
    private bool _isLockedRight;

    public ObservableCollection<ComparisonItem> Children { get; } = [];

    /// <summary>
    /// Gets whether this item or any children have differences.
    /// </summary>
    public bool HasDifferences => Status != FileComparisonStatus.Same || 
        Children.Any(c => c.HasDifferences);
}
