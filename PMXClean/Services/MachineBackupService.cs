namespace PMXClean.Services;

using System.IO;
using System.IO.Compression;
using PMXClean.Models;

/// <summary>
/// Service for handling .machine backup files (ZIP archives with renamed extension).
/// </summary>
public static class MachineBackupService
{
    private const string HeadersFileName = "Headers.data";
    private const string FullBackupMarker = "IsFullBackup";
    private const string CustomDllPrefix = "_";

    /// <summary>
    /// Loads and extracts a .machine backup file asynchronously.
    /// </summary>
    /// <param name="machineFilePath">Path to the .machine file.</param>
    /// <param name="cancellationToken">Cancellation token.</param>
    /// <returns>Information about the loaded backup.</returns>
    public static async Task<MachineBackupInfo> LoadBackupAsync(string machineFilePath, CancellationToken cancellationToken = default)
    {
        if (!File.Exists(machineFilePath))
        {
            throw new FileNotFoundException("Machine backup file not found.", machineFilePath);
        }

        // Create unique temp folder for extraction
        string tempFolder = Path.Combine(
            Path.GetTempPath(),
            "PMXClean_Backup",
            Path.GetFileNameWithoutExtension(machineFilePath) + "_" + Guid.NewGuid().ToString("N")[..8]);

        Directory.CreateDirectory(tempFolder);

        try
        {
            // Extract the ZIP archive on a background thread
            await Task.Run(() => ZipFile.ExtractToDirectory(machineFilePath, tempFolder, overwriteFiles: true), cancellationToken).ConfigureAwait(false);

            // Parse backup information on a background thread
            var (modules, isFullBackup, customDlls) = await Task.Run(() =>
            {
                var mods = ParseHeadersData(tempFolder);
                bool isFull = File.Exists(Path.Combine(tempFolder, FullBackupMarker));
                var dlls = FindCustomDlls(tempFolder);
                return (mods, isFull, dlls);
            }, cancellationToken).ConfigureAwait(false);

            string backupVersion = modules.Count > 0 ? modules[0].Version : "Unknown";

            return new MachineBackupInfo
            {
                FilePath = machineFilePath,
                FileName = Path.GetFileName(machineFilePath),
                ExtractedPath = tempFolder,
                IsFullBackup = isFullBackup,
                BackupVersion = backupVersion,
                Modules = modules,
                CustomDlls = customDlls
            };
        }
        catch
        {
            // Clean up on failure
            await CleanupTempFolderAsync(tempFolder).ConfigureAwait(false);
            throw;
        }
    }

    /// <summary>
    /// Parses the Headers.data file to extract module information.
    /// Format: ModuleName|Version|RelativePath (pipe-delimited)
    /// </summary>
    private static List<BackupModuleInfo> ParseHeadersData(string extractedPath)
    {
        var modules = new List<BackupModuleInfo>();
        string headersPath = Path.Combine(extractedPath, HeadersFileName);

        if (!File.Exists(headersPath))
        {
            return modules;
        }

        foreach (var line in File.ReadAllLines(headersPath))
        {
            if (string.IsNullOrWhiteSpace(line))
            {
                continue;
            }

            var parts = line.Split('|');
            if (parts.Length >= 3)
            {
                modules.Add(new BackupModuleInfo
                {
                    Name = parts[0].Trim(),
                    Version = parts[1].Trim(),
                    RelativePath = parts[2].Trim()
                });
            }
        }

        return modules;
    }

    /// <summary>
    /// Finds all DLL files that start with an underscore (custom implementations).
    /// </summary>
    private static List<string> FindCustomDlls(string extractedPath)
    {
        var customDlls = new List<string>();

        try
        {
            var dllFiles = Directory.GetFiles(extractedPath, "*.dll", SearchOption.AllDirectories);
            foreach (var dll in dllFiles)
            {
                string fileName = Path.GetFileName(dll);
                if (fileName.StartsWith(CustomDllPrefix, StringComparison.OrdinalIgnoreCase))
                {
                    // Store relative path for display
                    customDlls.Add(Path.GetRelativePath(extractedPath, dll));
                }
            }
        }
        catch
        {
            // Ignore errors during DLL search
        }

        return customDlls;
    }

    /// <summary>
    /// Cleans up the temporary extraction folder asynchronously.
    /// </summary>
    public static async Task CleanupTempFolderAsync(string? tempFolder)
    {
        if (string.IsNullOrEmpty(tempFolder) || !Directory.Exists(tempFolder))
        {
            return;
        }

        try
        {
            await Task.Run(() => Directory.Delete(tempFolder, recursive: true)).ConfigureAwait(false);
        }
        catch
        {
            // Best effort cleanup - ignore errors
        }
    }

    /// <summary>
    /// Validates that a file is a valid .machine backup.
    /// </summary>
    public static bool IsValidMachineBackup(string filePath)
    {
        if (!File.Exists(filePath))
        {
            return false;
        }

        try
        {
            using var archive = ZipFile.OpenRead(filePath);
            // Check for Headers.data entry
            return archive.Entries.Any(e => 
                e.FullName.Equals(HeadersFileName, StringComparison.OrdinalIgnoreCase));
        }
        catch
        {
            return false;
        }
    }

    /// <summary>
    /// Gets a preview of the backup without full extraction.
    /// </summary>
    public static (string version, bool isFullBackup, int moduleCount)? PreviewBackup(string filePath)
    {
        if (!File.Exists(filePath))
        {
            return null;
        }

        try
        {
            using var archive = ZipFile.OpenRead(filePath);
            
            // Check for full backup marker
            bool isFullBackup = archive.Entries.Any(e => 
                e.FullName.Equals(FullBackupMarker, StringComparison.OrdinalIgnoreCase));

            // Read Headers.data
            var headersEntry = archive.Entries.FirstOrDefault(e => 
                e.FullName.Equals(HeadersFileName, StringComparison.OrdinalIgnoreCase));

            if (headersEntry is null)
            {
                return null;
            }

            string version = "Unknown";
            int moduleCount = 0;

            using var reader = new StreamReader(headersEntry.Open());
            string? firstLine = reader.ReadLine();
            if (!string.IsNullOrWhiteSpace(firstLine))
            {
                var parts = firstLine.Split('|');
                if (parts.Length >= 2)
                {
                    version = parts[1].Trim();
                }

                moduleCount = 1;
            }

            // Count remaining lines
            while (reader.ReadLine() is not null)
            {
                moduleCount++;
            }

            return (version, isFullBackup, moduleCount);
        }
        catch
        {
            return null;
        }
    }
}
