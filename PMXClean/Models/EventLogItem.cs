namespace PMXClean.Models;

using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Represents an event from the Windows Event Viewer related to PathMasterX.
/// </summary>
public sealed partial class EventLogItem : ObservableObject
{
    /// <summary>
    /// Display name/title of the event (typically the source).
    /// </summary>
    [ObservableProperty]
    public partial string Name { get; set; } = string.Empty;

    /// <summary>
    /// The severity level of the event.
    /// </summary>
    [ObservableProperty]
    public partial EventLogLevel Level { get; set; } = EventLogLevel.Information;

    /// <summary>
    /// Brief status text showing the event type (Error, Warning, Information).
    /// </summary>
    [ObservableProperty]
    public partial string StatusText { get; set; } = string.Empty;

    /// <summary>
    /// The full event message/description.
    /// </summary>
    [ObservableProperty]
    public partial string Details { get; set; } = string.Empty;

    /// <summary>
    /// Category/grouping for the event (e.g., the log name: Application, System).
    /// </summary>
    [ObservableProperty]
    public partial string Category { get; set; } = string.Empty;

    /// <summary>
    /// The event ID from the event log.
    /// </summary>
    [ObservableProperty]
    public partial long EventId { get; set; }

    /// <summary>
    /// When the event was recorded.
    /// </summary>
    [ObservableProperty]
    public partial DateTime TimeCreated { get; set; }

    /// <summary>
    /// User-friendly display of the time.
    /// </summary>
    public string TimeDisplay => TimeCreated.ToString("yyyy-MM-dd HH:mm:ss");
}

/// <summary>
/// Severity levels for event log entries, matching Windows Event Log levels.
/// </summary>
public enum EventLogLevel
{
    /// <summary>
    /// Critical error that caused application failure.
    /// </summary>
    Critical = 1,

    /// <summary>
    /// Error that may cause issues.
    /// </summary>
    Error = 2,

    /// <summary>
    /// Warning that should be reviewed.
    /// </summary>
    Warning = 3,

    /// <summary>
    /// Informational event.
    /// </summary>
    Information = 4,

    /// <summary>
    /// Verbose/debug level event.
    /// </summary>
    Verbose = 5
}
