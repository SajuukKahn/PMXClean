namespace PMXClean.Models;

/// <summary>
/// Status of a file or folder comparison.
/// </summary>
public enum FileComparisonStatus
{
    /// <summary>Files are identical.</summary>
    Same,

    /// <summary>Files exist in both locations but have different content.</summary>
    Different,

    /// <summary>File only exists on the left side (source/version).</summary>
    LeftOnly,

    /// <summary>File only exists on the right side (target/installed).</summary>
    RightOnly,

    /// <summary>Folder contains items with differences.</summary>
    ContainsDifferences
}
