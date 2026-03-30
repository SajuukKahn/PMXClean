namespace PMXClean.Models;

using System.Diagnostics;
using System.IO;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;

/// <summary>
/// Represents a large file found during the file search operation.
/// </summary>
public sealed partial class LargeFileResult : ObservableObject
{
    public LargeFileResult(string fullPath, long sizeBytes)
    {
        FullPath = fullPath;
        FileName = Path.GetFileName(fullPath);
        DirectoryPath = Path.GetDirectoryName(fullPath) ?? string.Empty;
        SizeBytes = sizeBytes;
        SizeFormatted = FormatFileSize(sizeBytes);
    }

    /// <summary>
    /// Gets the file name without path.
    /// </summary>
    public string FileName { get; }

    /// <summary>
    /// Gets the full path to the file.
    /// </summary>
    public string FullPath { get; }

    /// <summary>
    /// Gets the directory containing the file.
    /// </summary>
    public string DirectoryPath { get; }

    /// <summary>
    /// Gets the file size in bytes.
    /// </summary>
    public long SizeBytes { get; }

    /// <summary>
    /// Gets the formatted file size (e.g., "250 MB").
    /// </summary>
    public string SizeFormatted { get; }

    /// <summary>
    /// Opens File Explorer to the folder containing this file.
    /// </summary>
    [RelayCommand]
    private void OpenFolder()
    {
        if (Directory.Exists(DirectoryPath))
        {
            Process.Start(new ProcessStartInfo
            {
                FileName = "explorer.exe",
                Arguments = $"/select,\"{FullPath}\"",
                UseShellExecute = true
            });
        }
    }

    private static string FormatFileSize(long bytes)
    {
        const long KB = 1024;
        const long MB = KB * 1024;
        const long GB = MB * 1024;

        return bytes switch
        {
            >= GB => $"{bytes / (double)GB:N2} GB",
            >= MB => $"{bytes / (double)MB:N2} MB",
            >= KB => $"{bytes / (double)KB:N2} KB",
            _ => $"{bytes} B"
        };
    }
}
