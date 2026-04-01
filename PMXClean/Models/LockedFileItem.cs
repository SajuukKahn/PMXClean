namespace PMXClean.Models;

using System.Collections.ObjectModel;
using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Represents a locked file or folder in the tree view.
/// </summary>
public sealed partial class LockedFileItem : ObservableObject
{
    /// <summary>
    /// Name of the file or folder.
    /// </summary>
    public required string Name { get; init; }

    /// <summary>
    /// Full path to the file.
    /// </summary>
    public required string FullPath { get; init; }

    /// <summary>
    /// Relative path from the installation root.
    /// </summary>
    public required string RelativePath { get; init; }

    /// <summary>
    /// Indicates if this is a folder (true) or file (false).
    /// </summary>
    public required bool IsFolder { get; init; }

    /// <summary>
    /// The content of the locked file (first few lines or full content).
    /// </summary>
    public string? Content { get; init; }

    /// <summary>
    /// Child items (for folders).
    /// </summary>
    public ObservableCollection<LockedFileItem> Children { get; } = [];

    [ObservableProperty]
    public partial bool IsExpanded { get; set; }

    [ObservableProperty]
    public partial bool IsSelected { get; set; }
}
