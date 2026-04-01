namespace PMXClean.Models;

/// <summary>
/// Represents a page stub file with its name and UI path.
/// </summary>
public sealed class PageInfo
{
    /// <summary>
    /// The name of the page (stub file name without extension).
    /// </summary>
    public required string Name { get; init; }

    /// <summary>
    /// The UI path to the page (folder structure from Base\UI\Pages\).
    /// </summary>
    public required string UIPath { get; init; }

    /// <summary>
    /// Display text combining name and path.
    /// </summary>
    public string DisplayText => $"{Name} ({UIPath})";
}
