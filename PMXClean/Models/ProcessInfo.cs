namespace PMXClean.Models;

using System.Diagnostics;
using System.IO;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

/// <summary>
/// Represents information about a running process.
/// </summary>
public sealed partial class ProcessInfo : ObservableObject
{
    /// <summary>
    /// Gets the process ID.
    /// </summary>
    [ObservableProperty]
    public partial int ProcessId { get; set; }

    /// <summary>
    /// Gets the process name.
    /// </summary>
    [ObservableProperty]
    public partial string Name { get; set; } = string.Empty;

    /// <summary>
    /// Gets the working set memory in kilobytes.
    /// </summary>
    [ObservableProperty]
    public partial long MemoryKB { get; set; }

    /// <summary>
    /// Gets the formatted memory size (e.g., "125 MB").
    /// </summary>
    public string MemoryFormatted => FormatMemory(MemoryKB);

    /// <summary>
    /// Gets the full path to the executable.
    /// </summary>
    [ObservableProperty]
    public partial string Path { get; set; } = string.Empty;

    /// <summary>
    /// Opens File Explorer to the folder containing the executable.
    /// </summary>
    [RelayCommand]
    private void OpenFolder()
    {
        if (string.IsNullOrEmpty(Path))
        {
            return;
        }

        string? directory = System.IO.Path.GetDirectoryName(Path);
        if (!string.IsNullOrEmpty(directory) && Directory.Exists(directory))
        {
            Process.Start(new ProcessStartInfo
            {
                FileName = "explorer.exe",
                Arguments = $"/select,\"{Path}\"",
                UseShellExecute = true
            });
        }
    }

    private static string FormatMemory(long memoryKB)
    {
        if (memoryKB >= 1_048_576) // >= 1 GB
        {
            return $"{memoryKB / 1_048_576.0:F2} GB";
        }

        if (memoryKB >= 1024) // >= 1 MB
        {
            return $"{memoryKB / 1024.0:F1} MB";
        }

        return $"{memoryKB} KB";
    }
}
