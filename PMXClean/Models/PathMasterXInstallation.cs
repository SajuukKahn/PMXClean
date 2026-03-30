namespace PMXClean.Models;

/// <summary>
/// Represents a discovered PathMasterX installation.
/// </summary>
public sealed class PathMasterXInstallation
{
    public required string Path { get; init; }
    public required string DisplayName { get; init; }
    public required InstallationType Type { get; init; }
}

/// <summary>
/// Indicates the type/source of a PathMasterX installation.
/// </summary>
public enum InstallationType
{
    ProgramFiles,
    UserDevelopment,
    Custom
}
