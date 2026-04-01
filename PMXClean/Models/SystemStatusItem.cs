namespace PMXClean.Models;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Represents a system diagnostic status item with visual indicator.
/// </summary>
public sealed partial class SystemStatusItem : ObservableObject
{
    /// <summary>
    /// Display name of the check (e.g., "Windows Defender", "Power Plan").
    /// </summary>
    [ObservableProperty]
    public partial string Name { get; set; } = string.Empty;

    /// <summary>
    /// Current status of the check.
    /// </summary>
    [ObservableProperty]
    public partial SystemStatus Status { get; set; } = SystemStatus.Unknown;

    /// <summary>
    /// Brief status text (e.g., "Enabled", "High Performance", "Healthy").
    /// </summary>
    [ObservableProperty]
    public partial string StatusText { get; set; } = string.Empty;

    /// <summary>
    /// Detailed information about the check.
    /// </summary>
    [ObservableProperty]
    public partial string Details { get; set; } = string.Empty;

    /// <summary>
    /// Category of the check (e.g., "Security", "Performance", "Hardware").
    /// </summary>
    [ObservableProperty]
    public partial string Category { get; set; } = string.Empty;
}

/// <summary>
/// Status levels for system diagnostics.
/// </summary>
public enum SystemStatus
{
    /// <summary>
    /// Status is good/optimal.
    /// </summary>
    Good,

    /// <summary>
    /// Warning - not critical but should be reviewed.
    /// </summary>
    Warning,

    /// <summary>
    /// Error/problem detected.
    /// </summary>
    Error,

    /// <summary>
    /// Status could not be determined.
    /// </summary>
    Unknown,

    /// <summary>
    /// Information only, no status judgment.
    /// </summary>
    Info
}
