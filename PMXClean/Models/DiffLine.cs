namespace PMXClean.Models;

/// <summary>
/// Type of change for a diff line.
/// </summary>
public enum DiffLineType
{
    /// <summary>Line is unchanged in both files.</summary>
    Unchanged,

    /// <summary>Line was added (exists only in right/new file).</summary>
    Added,

    /// <summary>Line was removed (exists only in left/old file).</summary>
    Removed,

    /// <summary>Header/separator line for context.</summary>
    Header
}

/// <summary>
/// Represents a single line in a diff comparison.
/// </summary>
public sealed class DiffLine
{
    public DiffLineType Type { get; init; }
    public string Content { get; init; } = string.Empty;
    public int? LeftLineNumber { get; init; }
    public int? RightLineNumber { get; init; }
}
