namespace PMXClean.Models;

/// <summary>
/// Represents a discovered PathMasterX installation or loaded backup.
/// </summary>
public sealed class PathMasterXInstallation
{
    public required string Path { get; init; }
    public required string DisplayName { get; init; }
    public required InstallationType Type { get; init; }

    /// <summary>
    /// Associated backup info when Type is MachineBackup.
    /// </summary>
    public MachineBackupInfo? BackupInfo { get; init; }

    /// <summary>
    /// Whether this installation is from a .machine backup file.
    /// </summary>
    public bool IsBackup => Type == InstallationType.MachineBackup;

    /// <summary>
    /// Whether this backup is a full backup (only applicable when IsBackup is true).
    /// </summary>
    public bool IsFullBackup => BackupInfo?.IsFullBackup ?? false;

    /// <summary>
    /// Whether this backup contains custom DLLs (only applicable when IsBackup is true).
    /// </summary>
    public bool HasCustomDlls => BackupInfo?.HasCustomDlls ?? false;

    /// <summary>
    /// List of custom DLLs in this backup.
    /// </summary>
    public IReadOnlyList<string> CustomDlls => BackupInfo?.CustomDlls ?? [];
}

/// <summary>
/// Indicates the type/source of a PathMasterX installation.
/// </summary>
public enum InstallationType
{
    ProgramFiles,
    UserDevelopment,
    Custom,
    MachineBackup
}
