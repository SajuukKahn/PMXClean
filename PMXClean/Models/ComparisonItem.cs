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
    public partial string Name { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string RelativePath { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string? LeftFullPath { get; set; }

    [ObservableProperty]
    public partial string? RightFullPath { get; set; }

    [ObservableProperty]
    public partial bool IsFolder { get; set; }

    [ObservableProperty]
    public partial bool IsPythonScript { get; set; }

    [ObservableProperty]
    public partial bool IsExpanded { get; set; }

    [ObservableProperty]
    public partial bool IsSelected { get; set; }

    [ObservableProperty]
    public partial FileComparisonStatus Status { get; set; } = FileComparisonStatus.Same;

    [ObservableProperty]
    public partial bool IsLocked { get; set; }

    [ObservableProperty]
    public partial bool IsLockedRight { get; set; }
    public ObservableCollection<ComparisonItem> Children { get; } = [];

    /// <summary>
    /// Gets whether this item or any children have differences.
    /// </summary>
    public bool HasDifferences => Status != FileComparisonStatus.Same || 
        Children.Any(c => c.HasDifferences);
}
