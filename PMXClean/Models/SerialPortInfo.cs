namespace PMXClean.Models;

using System;
using CommunityToolkit.Mvvm.ComponentModel;

/// <summary>
/// Represents information about a serial port (COM device).
/// </summary>
public sealed partial class SerialPortInfo : ObservableObject
{
    /// <summary>
    /// Gets the device name (e.g., "USB Serial Port (COM3)").
    /// </summary>
    [ObservableProperty]
    public partial string Name { get; set; } = string.Empty;

    /// <summary>
    /// Gets the device status (e.g., "OK", "Error").
    /// </summary>
    [ObservableProperty]
    public partial string Status { get; set; } = string.Empty;

    /// <summary>
    /// Gets the driver INF filename.
    /// </summary>
    [ObservableProperty]
    public partial string DriverFileName { get; set; } = string.Empty;

    /// <summary>
    /// Gets the driver date.
    /// </summary>
    [ObservableProperty]
    public partial DateTime? DriverDate { get; set; }

    /// <summary>
    /// Gets the formatted driver date string.
    /// </summary>
    public string DriverDateFormatted => DriverDate?.ToString("d") ?? "Unknown";

    /// <summary>
    /// Gets the driver version.
    /// </summary>
    [ObservableProperty]
    public partial string DriverVersion { get; set; } = string.Empty;

    /// <summary>
    /// Determines if the device status is OK.
    /// </summary>
    public bool IsOk => Status.Equals("OK", StringComparison.OrdinalIgnoreCase);
}
