namespace PMXClean.Models;

using System.Collections.ObjectModel;

/// <summary>
/// Result of comparing two files.
/// </summary>
public sealed class FileComparisonResult
{
    public string LeftPath { get; init; } = string.Empty;
    public string RightPath { get; init; } = string.Empty;
    public string RelativePath { get; init; } = string.Empty;
    public FileComparisonStatus Status { get; init; }
    public bool IsLeftLocked { get; init; }
    public bool IsRightLocked { get; init; }
    public ObservableCollection<DiffLine> DiffLines { get; init; } = [];
    public int AddedLines { get; init; }
    public int RemovedLines { get; init; }
    public int UnchangedLines { get; init; }
}
