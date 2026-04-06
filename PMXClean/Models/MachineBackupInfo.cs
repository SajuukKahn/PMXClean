namespace PMXClean.Models;

/// <summary>
/// Information about a loaded .machine backup file.
/// </summary>
public sealed class MachineBackupInfo
{
    /// <summary>
    /// Original path to the .machine file.
    /// </summary>
    public required string FilePath { get; init; }

    /// <summary>
    /// File name of the .machine file.
    /// </summary>
    public required string FileName { get; init; }

    /// <summary>
    /// Path to the temporary extraction folder.
    /// </summary>
    public required string ExtractedPath { get; init; }

    /// <summary>
    /// Whether this is a full backup (contains IsFullBackup marker).
    /// </summary>
    public required bool IsFullBackup { get; init; }

    /// <summary>
    /// Version string extracted from Headers.data.
    /// </summary>
    public required string BackupVersion { get; init; }

    /// <summary>
    /// List of modules defined in Headers.data.
    /// </summary>
    public required List<BackupModuleInfo> Modules { get; init; }

    /// <summary>
    /// List of custom DLLs (starting with underscore) found in the backup.
    /// </summary>
    public required List<string> CustomDlls { get; init; }

    /// <summary>
    /// Display name for UI.
    /// </summary>
    public string DisplayName => $"{FileName} (v{BackupVersion})";

    /// <summary>
    /// Summary text for UI display.
    /// </summary>
    public string Summary => $"Version {BackupVersion} | {Modules.Count} modules | {(IsFullBackup ? "Full Backup" : "Regular Backup")}";

    /// <summary>
    /// Whether any custom DLLs were found.
    /// </summary>
    public bool HasCustomDlls => CustomDlls.Count > 0;
}

/// <summary>
/// Information about a module from Headers.data.
/// </summary>
public sealed class BackupModuleInfo
{
    /// <summary>
    /// Module name (e.g., "Triggers", "Process", "Core").
    /// </summary>
    public required string Name { get; init; }

    /// <summary>
    /// Module version (e.g., "1.2.0.1").
    /// </summary>
    public required string Version { get; init; }

    /// <summary>
    /// Relative path to the module folder (e.g., ".\Feature\Trigger").
    /// </summary>
    public required string RelativePath { get; init; }

    /// <summary>
    /// Normalized path without leading .\ for comparison.
    /// </summary>
    public string NormalizedPath => RelativePath.TrimStart('.', '\\', '/');
}
