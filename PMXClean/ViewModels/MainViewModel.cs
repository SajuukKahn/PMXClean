namespace PMXClean.ViewModels;

using System.Collections.ObjectModel;
using System.Diagnostics;
using System.IO;
using System.Net.NetworkInformation;
using System.Reflection;
using System.Text;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using PMXClean.Models;

/// <summary>
/// Main ViewModel for the PMXClean application.
/// </summary>
public sealed partial class MainViewModel : ObservableObject
{
    private readonly string _appBaseDirectory;
    private readonly string _backupsRootDirectory;
    private readonly string _comparisonTempDirectory;
    private readonly string _winMergePath;

    public MainViewModel()
    {
        _appBaseDirectory = AppDomain.CurrentDomain.BaseDirectory;
        _backupsRootDirectory = Path.Combine(_appBaseDirectory, "Backups");
        _comparisonTempDirectory = Path.Combine(Path.GetTempPath(), "PMXClean_Compare");
        _winMergePath = Path.Combine(_appBaseDirectory, @"WinMergePortable\App\WinMerge64\WinMergeU.exe");

        Installations = [];
        AvailableVersions = [];
        BackupInstances = [];

        Initialize();
    }

    #region Observable Properties

    [ObservableProperty]
    private string _statusMessage = "Ready";

    [ObservableProperty]
    private string _fileVersionText = string.Empty;

    [ObservableProperty]
    private string _versionInfoText = string.Empty;

    [ObservableProperty]
    private string _backupInfoText = "No backup selected. Create a new backup to begin.";

    [ObservableProperty]
    private string _utilityOutput = string.Empty;

    [ObservableProperty]
    private string _networkUtilityOutput = string.Empty;

    [ObservableProperty]
    private PathMasterXInstallation? _selectedInstallation;

    [ObservableProperty]
    private string? _selectedVersion;

    [ObservableProperty]
    private string? _selectedBackup;

    [ObservableProperty]
    private bool _isBackupRenaming;

    [ObservableProperty]
    private bool _isBackupCreating;

    [ObservableProperty]
    private string _backupEditName = string.Empty;

    // PMX Launcher properties
    [ObservableProperty]
    private bool _offlineMode;

    [ObservableProperty]
    private bool _autoAdvance;

    [ObservableProperty]
    private bool _softwareRendering;

    [ObservableProperty]
    private bool _freeWindow;

    [ObservableProperty]
    private string _startPage = string.Empty;

    [ObservableProperty]
    private string _windowWidth = string.Empty;

    [ObservableProperty]
    private string _windowHeight = string.Empty;

    [ObservableProperty]
    private string _windowX = string.Empty;

    [ObservableProperty]
    private string _windowY = string.Empty;

    [ObservableProperty]
    private bool _visionDebug;

    [ObservableProperty]
    private bool _visionTrace;

    [ObservableProperty]
    private bool _recordOnStartup;

    [ObservableProperty]
    private bool _recordHighQuality;

    [ObservableProperty]
    private bool _recordHighFramerate;

    [ObservableProperty]
    private bool _recordMicrophone;

    [ObservableProperty]
    private bool _recordWebcam;

    [ObservableProperty]
    private string _maxSegments = string.Empty;

    #endregion

    #region Collections

        public ObservableCollection<PathMasterXInstallation> Installations { get; }
        public ObservableCollection<string> AvailableVersions { get; }
        public ObservableCollection<string> BackupInstances { get; }
        public ObservableCollection<LargeFileResult> LargeFiles { get; } = [];

        #endregion

    #region Property Changed Handlers

    partial void OnSelectedInstallationChanged(PathMasterXInstallation? value)
    {
        if (value is not null)
        {
            StatusMessage = $"Selected: {value.DisplayName}";
            UpdateFileVersionDisplay();
        }
    }

    partial void OnSelectedVersionChanged(string? value)
    {
        UpdateVersionInfo();
    }

    partial void OnSelectedBackupChanged(string? value)
    {
        UpdateBackupInfo();
    }

    #endregion

    #region Initialization

    private void Initialize()
    {
        ValidateWinMerge();
        DiscoverInstallations();
        LoadAvailableVersions();
        LoadBackupInstances();
    }

    private void ValidateWinMerge()
    {
        if (!File.Exists(_winMergePath))
        {
            StatusMessage = "Warning: WinMerge not found - Python comparison features will not work";
        }
    }

    #endregion

    #region Installation Discovery

    [RelayCommand]
    private void RefreshPaths()
    {
        var previousPath = SelectedInstallation?.Path;
        DiscoverInstallations();

        if (!string.IsNullOrEmpty(previousPath))
        {
            SelectedInstallation = Installations.FirstOrDefault(i =>
                i.Path.Equals(previousPath, StringComparison.OrdinalIgnoreCase));
        }

        StatusMessage = $"Refresh complete - Found {Installations.Count} installation(s)";
    }

    private void DiscoverInstallations()
    {
        StatusMessage = "Discovering PathMasterX installations...";
        Installations.Clear();

        SearchProgramFiles();
        SearchUserRepositories();

        // Sort: Production first, then Development
        var sorted = Installations
            .OrderBy(i => i.Type == InstallationType.ProgramFiles ? 0 : 1)
            .ThenBy(i => i.DisplayName)
            .ToList();

        Installations.Clear();
        foreach (var installation in sorted)
        {
            Installations.Add(installation);
        }

        if (Installations.Count == 0)
        {
            StatusMessage = "Warning: No PathMasterX installations found - Application will have limited functionality";
        }
        else
        {
            StatusMessage = $"Found {Installations.Count} PathMasterX installation(s)";
            SelectedInstallation = Installations.FirstOrDefault();
        }
    }

    private void SearchProgramFiles()
    {
        string[] programFilesPaths =
        [
            Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles),
            Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86)
        ];

        foreach (var programFilesPath in programFilesPaths)
        {
            if (string.IsNullOrEmpty(programFilesPath) || !Directory.Exists(programFilesPath))
            {
                continue;
            }

            try
            {
                SearchForExecutable(programFilesPath, InstallationType.ProgramFiles, maxDepth: 4);
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error searching {programFilesPath}: {ex.Message}");
            }
        }
    }

    private void SearchUserRepositories()
    {
        try
        {
            const string usersPath = @"C:\Users";
            if (!Directory.Exists(usersPath))
            {
                return;
            }

            foreach (var userDir in Directory.GetDirectories(usersPath))
            {
                try
                {
                    var userDirInfo = new DirectoryInfo(userDir);

                    if (userDirInfo.Name.Equals("Public", StringComparison.OrdinalIgnoreCase) ||
                        userDirInfo.Name.Equals("Default", StringComparison.OrdinalIgnoreCase) ||
                        userDirInfo.Name.Equals("Default User", StringComparison.OrdinalIgnoreCase) ||
                        userDirInfo.Name.Equals("All Users", StringComparison.OrdinalIgnoreCase))
                    {
                        continue;
                    }

                    string reposPath = Path.Combine(userDir, "source", "repos");
                    if (Directory.Exists(reposPath))
                    {
                        SearchForExecutable(reposPath, InstallationType.UserDevelopment, maxDepth: 16);
                    }

                    string docsReposPath = Path.Combine(userDir, "Documents", "repos");
                    if (Directory.Exists(docsReposPath))
                    {
                        SearchForExecutable(docsReposPath, InstallationType.UserDevelopment, maxDepth: 16);
                    }
                }
                catch (UnauthorizedAccessException)
                {
                    continue;
                }
                catch (Exception ex)
                {
                    Debug.WriteLine($"Error searching user directory {userDir}: {ex.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error searching user repositories: {ex.Message}");
        }
    }

    private void SearchForExecutable(string searchPath, InstallationType installType, int maxDepth, int currentDepth = 0)
    {
        if (currentDepth > maxDepth)
        {
            return;
        }

        try
        {
            string exePath = Path.Combine(searchPath, "PVA.PathMasterX.exe");
            if (File.Exists(exePath))
            {
                var directory = Path.GetDirectoryName(exePath);
                if (!string.IsNullOrEmpty(directory) && !Installations.Any(i =>
                    i.Path.Equals(directory, StringComparison.OrdinalIgnoreCase)))
                {
                    Installations.Add(new PathMasterXInstallation
                    {
                        Path = directory,
                        DisplayName = GenerateDisplayName(directory, installType),
                        Type = installType
                    });
                }

                return;
            }

            foreach (var subDir in Directory.GetDirectories(searchPath))
            {
                SearchForExecutable(subDir, installType, maxDepth, currentDepth + 1);
            }
        }
        catch (UnauthorizedAccessException)
        {
            // Skip directories we don't have access to
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error searching {searchPath}: {ex.Message}");
        }
    }

    private static string GenerateDisplayName(string path, InstallationType type)
    {
        try
        {
            return type switch
            {
                InstallationType.ProgramFiles => $"[Production] {path}",
                InstallationType.UserDevelopment => GenerateDevDisplayName(path),
                _ => path
            };
        }
        catch
        {
            return path;
        }
    }

    private static string GenerateDevDisplayName(string path)
    {
        var parts = path.Split(Path.DirectorySeparatorChar);
        var relevantParts = new List<string>();

        for (int i = parts.Length - 1; i >= 0; i--)
        {
            relevantParts.Insert(0, parts[i]);
            if (parts[i].Equals("bin", StringComparison.OrdinalIgnoreCase))
            {
                if (i > 0)
                {
                    relevantParts.Insert(0, parts[i - 1]);
                }

                break;
            }

            if (relevantParts.Count > 3)
            {
                break;
            }
        }

        var shortPath = string.Join("\\", relevantParts);
        return $"[Dev] {shortPath}";
    }

    private void UpdateFileVersionDisplay()
    {
        if (SelectedInstallation is null)
        {
            FileVersionText = string.Empty;
            return;
        }

        try
        {
            string exePath = Path.Combine(SelectedInstallation.Path, "PVA.PathMasterX.exe");

            if (File.Exists(exePath))
            {
                var versionInfo = FileVersionInfo.GetVersionInfo(exePath);
                string version = versionInfo.FileVersion ?? "Unknown";
                FileVersionText = $"Application Version: {version}";
            }
            else
            {
                FileVersionText = "Executable not found";
            }
        }
        catch
        {
            FileVersionText = $"Error reading version";
        }
    }

    [RelayCommand]
    private void OpenTargetFolder()
    {
        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: No target path selected";
            return;
        }

        if (!Directory.Exists(SelectedInstallation.Path))
        {
            StatusMessage = "Error: Target directory does not exist";
            return;
        }

        try
        {
            Process.Start(new ProcessStartInfo
            {
                FileName = "explorer.exe",
                Arguments = SelectedInstallation.Path,
                UseShellExecute = true
            });

            StatusMessage = $"Opened folder: {SelectedInstallation.Path}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error opening folder: {ex.Message}";
        }
    }

    #endregion

    #region Python Comparison

    private void LoadAvailableVersions()
    {
        AvailableVersions.Clear();

        var assembly = Assembly.GetExecutingAssembly();
        var resourceNames = assembly.GetManifestResourceNames();

        var versions = resourceNames
            .Where(name => name.StartsWith("PMXVersions\\", StringComparison.OrdinalIgnoreCase))
            .Select(name =>
            {
                var parts = name.Split('\\');
                return parts.Length >= 2 ? parts[1] : null;
            })
            .Where(v => v is not null)
            .Distinct()
            .OrderByDescending(v => v == "master" ? "zzzz" : v)
            .ToList();

        foreach (var version in versions)
        {
            if (version is not null)
            {
                AvailableVersions.Add(version);
            }
        }

        if (AvailableVersions.Count > 0)
        {
            SelectedVersion = AvailableVersions.First();
        }

        StatusMessage = $"Loaded {AvailableVersions.Count} available version(s)";
    }

    private void UpdateVersionInfo()
    {
        if (string.IsNullOrEmpty(SelectedVersion))
        {
            VersionInfoText = string.Empty;
            return;
        }

        var assembly = Assembly.GetExecutingAssembly();
        var resourceNames = assembly.GetManifestResourceNames();

        var fileCount = resourceNames
            .Count(name => name.StartsWith($"PMXVersions\\{SelectedVersion}\\", StringComparison.OrdinalIgnoreCase));

        VersionInfoText = $"Source: {SelectedVersion} ({fileCount} Python files embedded)";
    }

    [RelayCommand]
    private void AutoMatchVersion()
    {
        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: No target installation selected";
            return;
        }

        try
        {
            string exePath = Path.Combine(SelectedInstallation.Path, "PVA.PathMasterX.exe");
            if (!File.Exists(exePath))
            {
                StatusMessage = "Error: Target executable not found";
                return;
            }

            var versionInfo = FileVersionInfo.GetVersionInfo(exePath);
            string? fileVersion = versionInfo.FileVersion;

            if (string.IsNullOrEmpty(fileVersion))
            {
                StatusMessage = "Error: Could not read version from executable";
                return;
            }

            var matchedVersion = AvailableVersions.FirstOrDefault(v =>
                v.Equals(fileVersion, StringComparison.OrdinalIgnoreCase));

            if (matchedVersion is null)
            {
                matchedVersion = AvailableVersions.FirstOrDefault(v =>
                    fileVersion.StartsWith(v, StringComparison.OrdinalIgnoreCase) ||
                    v.StartsWith(fileVersion, StringComparison.OrdinalIgnoreCase));
            }

            if (matchedVersion is not null)
            {
                SelectedVersion = matchedVersion;
                StatusMessage = $"Auto-matched to version: {matchedVersion}";
            }
            else
            {
                StatusMessage = $"No matching version found for {fileVersion}. Using 'master' if available.";
                var masterVersion = AvailableVersions.FirstOrDefault(v => v == "master");
                if (masterVersion is not null)
                {
                    SelectedVersion = masterVersion;
                }
            }
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error auto-matching version: {ex.Message}";
        }
    }

    [RelayCommand]
    private void CompareWithWinMerge()
    {
        if (string.IsNullOrEmpty(SelectedVersion))
        {
            StatusMessage = "Error: Please select a source version to compare";
            return;
        }

        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: Please select a target installation";
            return;
        }

        if (!File.Exists(_winMergePath))
        {
            StatusMessage = "Error: WinMerge not found - Please ensure WinMergePortable is included";
            return;
        }

        try
        {
            StatusMessage = "Preparing files for comparison...";

            string sourceDir = Path.Combine(_comparisonTempDirectory, "source");
            string targetDir = Path.Combine(_comparisonTempDirectory, "target");

            CleanAndCreateDirectory(sourceDir);
            CleanAndCreateDirectory(targetDir);

            StatusMessage = $"Extracting {SelectedVersion} Python files...";
            int extractedCount = ExtractEmbeddedVersionFiles(SelectedVersion, sourceDir);

            if (extractedCount == 0)
            {
                StatusMessage = $"Error: No files found for version {SelectedVersion}";
                return;
            }

            StatusMessage = "Copying target installation files...";
            CopyPythonFilesExcludingLib(SelectedInstallation.Path, targetDir);

            StatusMessage = "Starting WinMerge...";
            Process.Start(new ProcessStartInfo
            {
                FileName = _winMergePath,
                Arguments = $"/r /f *.py /u /wl /dl \"{SelectedVersion}\" /dr \"Installed\" \"{sourceDir}\" \"{targetDir}\"",
                UseShellExecute = true
            });

            StatusMessage = $"WinMerge launched - comparing {SelectedVersion} vs installed";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error during comparison: {ex.Message}";
        }
    }

    private static void CleanAndCreateDirectory(string path)
    {
        if (Directory.Exists(path))
        {
            Directory.Delete(path, true);
        }

        Directory.CreateDirectory(path);
    }

    private static int ExtractEmbeddedVersionFiles(string version, string targetDir)
    {
        var assembly = Assembly.GetExecutingAssembly();
        var resourceNames = assembly.GetManifestResourceNames();
        var prefix = $"PMXVersions\\{version}\\";
        int count = 0;

        foreach (var resourceName in resourceNames.Where(n => n.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)))
        {
            try
            {
                var relativePath = resourceName[prefix.Length..];
                var targetPath = Path.Combine(targetDir, relativePath);

                var targetFileDir = Path.GetDirectoryName(targetPath);
                if (!string.IsNullOrEmpty(targetFileDir) && !Directory.Exists(targetFileDir))
                {
                    Directory.CreateDirectory(targetFileDir);
                }

                using var stream = assembly.GetManifestResourceStream(resourceName);
                if (stream is not null)
                {
                    using var fileStream = File.Create(targetPath);
                    stream.CopyTo(fileStream);
                    count++;
                }
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error extracting {resourceName}: {ex.Message}");
            }
        }

        return count;
    }

    private static void CopyPythonFilesExcludingLib(string sourceDir, string targetDir)
    {
        foreach (string file in Directory.GetFiles(sourceDir, "*.py", SearchOption.AllDirectories))
        {
            string relativePath = Path.GetRelativePath(sourceDir, file);

            if (relativePath.StartsWith("lib\\", StringComparison.OrdinalIgnoreCase) ||
                relativePath.StartsWith("lib/", StringComparison.OrdinalIgnoreCase) ||
                relativePath.Contains("\\lib\\", StringComparison.OrdinalIgnoreCase) ||
                relativePath.Contains("/lib/", StringComparison.OrdinalIgnoreCase))
            {
                continue;
            }

            string targetFile = Path.Combine(targetDir, relativePath);

            string? targetFileDir = Path.GetDirectoryName(targetFile);
            if (!string.IsNullOrEmpty(targetFileDir) && !Directory.Exists(targetFileDir))
            {
                Directory.CreateDirectory(targetFileDir);
            }

            File.Copy(file, targetFile, true);
        }
    }

    #endregion

    #region Backup Management

    private void LoadBackupInstances()
    {
        BackupInstances.Clear();

        if (!Directory.Exists(_backupsRootDirectory))
        {
            Directory.CreateDirectory(_backupsRootDirectory);
        }

        var backupDirs = Directory.GetDirectories(_backupsRootDirectory)
            .Select(d => new DirectoryInfo(d))
            .OrderByDescending(d => d.LastWriteTime)
            .ToList();

        foreach (var dir in backupDirs)
        {
            BackupInstances.Add(dir.Name);
        }

        if (BackupInstances.Count > 0)
        {
            SelectedBackup = BackupInstances.First();
        }
        else
        {
            UpdateBackupInfo();
        }
    }

    private void UpdateBackupInfo()
    {
        if (string.IsNullOrEmpty(SelectedBackup))
        {
            BackupInfoText = "No backup selected. Create a new backup to begin.";
            return;
        }

        string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);

        if (!Directory.Exists(backupPath))
        {
            BackupInfoText = "No backup selected. Create a new backup to begin.";
            return;
        }

        try
        {
            var dirInfo = new DirectoryInfo(backupPath);
            var files = Directory.GetFiles(backupPath, "*", SearchOption.AllDirectories);
            var fileCount = files.Length;
            var totalSize = files.Sum(f => new FileInfo(f).Length);
            var sizeMB = totalSize / 1024.0 / 1024.0;

            BackupInfoText = $"Created: {dirInfo.CreationTime:g}\n" +
                            $"Modified: {dirInfo.LastWriteTime:g}\n" +
                            $"Files: {fileCount:N0} ({sizeMB:N2} MB)";
        }
        catch (Exception ex)
        {
            BackupInfoText = $"Error reading backup info: {ex.Message}";
        }
    }

    [RelayCommand]
    private void StartNewBackup()
    {
        BackupEditName = $"Backup_{DateTime.Now:yyyyMMdd_HHmmss}";
        IsBackupCreating = true;
        IsBackupRenaming = false;
        StatusMessage = "Enter backup name and press Enter or Esc to cancel";
    }

    [RelayCommand]
    private void StartRenameBackup()
    {
        if (string.IsNullOrEmpty(SelectedBackup))
        {
            StatusMessage = "Error: Please select a backup to rename";
            return;
        }

        BackupEditName = SelectedBackup;
        IsBackupRenaming = true;
        IsBackupCreating = false;
        StatusMessage = "Enter new backup name and press Enter or Esc to cancel";
    }

    [RelayCommand]
    private void ConfirmBackupEdit()
    {
        if (IsBackupCreating)
        {
            CreateNewBackup(BackupEditName);
        }
        else if (IsBackupRenaming && !string.IsNullOrEmpty(SelectedBackup))
        {
            RenameBackup(SelectedBackup, BackupEditName);
        }

        CancelBackupEdit();
    }

    [RelayCommand]
    private void CancelBackupEdit()
    {
        IsBackupCreating = false;
        IsBackupRenaming = false;
        BackupEditName = string.Empty;

        if (IsBackupCreating || IsBackupRenaming)
        {
            StatusMessage = IsBackupCreating ? "Backup creation cancelled" : "Rename cancelled";
        }
    }

    private void CreateNewBackup(string backupName)
    {
        if (string.IsNullOrWhiteSpace(backupName))
        {
            StatusMessage = "Error: Backup name cannot be empty";
            return;
        }

        backupName = SanitizeFileName(backupName);
        string newBackupPath = Path.Combine(_backupsRootDirectory, backupName);

        if (Directory.Exists(newBackupPath))
        {
            StatusMessage = $"Error: Backup '{backupName}' already exists";
            return;
        }

        try
        {
            Directory.CreateDirectory(newBackupPath);
            LoadBackupInstances();
            SelectedBackup = backupName;
            StatusMessage = $"Created new backup: {backupName}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error creating backup: {ex.Message}";
        }
    }

    private void RenameBackup(string oldName, string newName)
    {
        if (string.IsNullOrWhiteSpace(newName))
        {
            StatusMessage = "Error: Backup name cannot be empty";
            return;
        }

        newName = SanitizeFileName(newName);
        string oldPath = Path.Combine(_backupsRootDirectory, oldName);
        string newPath = Path.Combine(_backupsRootDirectory, newName);

        if (Directory.Exists(newPath))
        {
            StatusMessage = $"Error: Backup '{newName}' already exists";
            return;
        }

        try
        {
            Directory.Move(oldPath, newPath);
            LoadBackupInstances();
            SelectedBackup = newName;
            StatusMessage = $"Renamed backup to: {newName}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error renaming backup: {ex.Message}";
        }
    }

    [RelayCommand]
    private void DeleteBackup()
    {
        if (string.IsNullOrEmpty(SelectedBackup))
        {
            StatusMessage = "Error: Please select a backup to delete";
            return;
        }

        string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);

        try
        {
            Directory.Delete(backupPath, true);
            StatusMessage = $"Deleted backup: {SelectedBackup}";
            LoadBackupInstances();
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error deleting backup: {ex.Message}";
        }
    }

    private static string SanitizeFileName(string name)
    {
        foreach (char c in Path.GetInvalidFileNameChars())
        {
            name = name.Replace(c, '_');
        }

        return name;
    }

    #endregion

    #region Backup Operations

    [RelayCommand]
    private void BackupAllFiles()
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        try
        {
            StatusMessage = "Backing up all files...";
            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup!);

            CopyDirectoryStructure(SelectedInstallation!.Path, backupPath);
            CopyDirectoryRecursive(SelectedInstallation.Path, backupPath);

            UpdateBackupInfo();
            StatusMessage = "All files backup complete";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error backing up all files: {ex.Message}";
        }
    }

    [RelayCommand]
    private void BackupJson() => BackupFilesByPattern("*.json", "JSON");

    [RelayCommand]
    private void BackupRetention() => BackupFilesByPattern("*.retention", "Retention");

    [RelayCommand]
    private void BackupPython() => BackupFilesByPattern("*.py", "Python");

    [RelayCommand]
    private void BackupDlls() => BackupFilesByPattern("*.DLL", "DLLs");

    [RelayCommand]
    private void BackupStubs() => BackupFilesByPattern("*.stub", "Page Stubs");

    [RelayCommand]
    private void BackupCameraFiles()
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        try
        {
            StatusMessage = "Backing up Camera files...";
            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup!);
            string cameraSourcePath = Path.Combine(SelectedInstallation!.Path, "Device", "Camera");

            if (!Directory.Exists(cameraSourcePath))
            {
                StatusMessage = "Camera folder not found in target installation";
                return;
            }

            if (!Directory.Exists(backupPath))
            {
                Directory.CreateDirectory(backupPath);
            }

            // Copy all files from Device\Camera that are NOT .dll, .json, or .py
            string[] excludedExtensions = [".dll", ".json", ".py"];
            int copiedCount = 0;

            foreach (string file in Directory.GetFiles(cameraSourcePath, "*", SearchOption.AllDirectories))
            {
                string extension = Path.GetExtension(file).ToLowerInvariant();
                if (!excludedExtensions.Contains(extension))
                {
                    string relativePath = Path.GetRelativePath(SelectedInstallation.Path, file);
                    string targetFile = Path.Combine(backupPath, relativePath);

                    string? targetFileDir = Path.GetDirectoryName(targetFile);
                    if (targetFileDir is not null && !Directory.Exists(targetFileDir))
                    {
                        Directory.CreateDirectory(targetFileDir);
                    }

                    File.Copy(file, targetFile, true);
                    copiedCount++;
                }
            }

            UpdateBackupInfo();
            StatusMessage = $"Camera files backup complete ({copiedCount} files)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error backing up Camera files: {ex.Message}";
        }
    }

    #region Copy to Destination Commands

    [RelayCommand]
    private void CopyJsonToDestination() => CopyToDestinationByPattern("*.json", "JSON");

    [RelayCommand]
    private void CopyRetentionToDestination() => CopyToDestinationByPattern("*.retention", "Retention");

    [RelayCommand]
    private void CopyPythonToDestination() => CopyToDestinationByPattern("*.py", "Python");

    [RelayCommand]
    private void CopyDllsToDestination() => CopyToDestinationByPattern("*.DLL", "DLLs");

    [RelayCommand]
    private void CopyStubsToDestination() => CopyToDestinationByPattern("*.stub", "Page Stubs");

    [RelayCommand]
    private void CopyCameraFilesToDestination()
    {
        if (string.IsNullOrEmpty(SelectedBackup))
        {
            StatusMessage = "Error: Please select a backup first";
            return;
        }

        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: Please select a target installation";
            return;
        }

        try
        {
            StatusMessage = "Copying Camera files to destination...";
            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);
            string cameraBackupPath = Path.Combine(backupPath, "Device", "Camera");

            if (!Directory.Exists(cameraBackupPath))
            {
                StatusMessage = "No Camera files found in backup";
                return;
            }

            // Copy all files from backup Device\Camera that are NOT .dll, .json, or .py
            string[] excludedExtensions = [".dll", ".json", ".py"];
            int copiedCount = 0;

            foreach (string file in Directory.GetFiles(cameraBackupPath, "*", SearchOption.AllDirectories))
            {
                string extension = Path.GetExtension(file).ToLowerInvariant();
                if (!excludedExtensions.Contains(extension))
                {
                    string relativePath = Path.GetRelativePath(backupPath, file);
                    string targetFile = Path.Combine(SelectedInstallation.Path, relativePath);

                    string? targetFileDir = Path.GetDirectoryName(targetFile);
                    if (targetFileDir is not null && !Directory.Exists(targetFileDir))
                    {
                        Directory.CreateDirectory(targetFileDir);
                    }

                    File.Copy(file, targetFile, true);
                    copiedCount++;
                }
            }

            StatusMessage = $"Camera files copied to destination ({copiedCount} files)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error copying Camera files: {ex.Message}";
        }
    }

    private void CopyToDestinationByPattern(string pattern, string fileType)
    {
        if (string.IsNullOrEmpty(SelectedBackup))
        {
            StatusMessage = "Error: Please select a backup first";
            return;
        }

        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: Please select a target installation";
            return;
        }

        try
        {
            StatusMessage = $"Copying {fileType} to destination...";
            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);

            if (!Directory.Exists(backupPath))
            {
                StatusMessage = $"Error: Backup folder does not exist";
                return;
            }

            CopyFilesByPattern(backupPath, SelectedInstallation.Path, pattern);
            StatusMessage = $"{fileType} copied to destination";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error copying {fileType}: {ex.Message}";
        }
    }

    #endregion

    private void BackupFilesByPattern(string pattern, string fileType)
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        try
        {
            StatusMessage = $"Backing up {fileType}...";
            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup!);

            if (!Directory.Exists(backupPath))
            {
                Directory.CreateDirectory(backupPath);
            }

            CopyDirectoryStructure(SelectedInstallation!.Path, backupPath);
            CopyFilesByPattern(SelectedInstallation.Path, backupPath, pattern);

            UpdateBackupInfo();
            StatusMessage = $"{fileType} backup complete";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error backing up {fileType}: {ex.Message}";
        }
    }

    [RelayCommand]
    private void RestoreBackup()
    {
        if (string.IsNullOrEmpty(SelectedBackup))
        {
            StatusMessage = "Error: Please select a backup to restore";
            return;
        }

        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: Please select a target installation";
            return;
        }

        string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);

        try
        {
            StatusMessage = $"Restoring backup '{SelectedBackup}' to target...";

            if (!Directory.Exists(backupPath))
            {
                StatusMessage = "Error: Backup folder does not exist";
                return;
            }

            CopyDirectoryRecursive(backupPath, SelectedInstallation.Path);
            StatusMessage = "Restore complete";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error restoring backup: {ex.Message}";
        }
    }

    private bool ValidateBackupSelected()
    {
        if (string.IsNullOrEmpty(SelectedBackup))
        {
            StatusMessage = "Error: Please select or create a backup first";
            return false;
        }

        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: Please select a target installation";
            return false;
        }

        return true;
    }

    #endregion

    #region Cleanup Operations

        [RelayCommand]
        private void DeleteAll()
        {
            if (SelectedInstallation is null)
            {
                StatusMessage = "Error: Please select a target installation";
                return;
            }

            try
            {
                StatusMessage = "Deleting all data files...";

                string[] patterns = ["*.json", "*.retention", "*.py", "*.stub"];
                int totalCount = 0;

                foreach (var pattern in patterns)
                {
                    foreach (string file in Directory.GetFiles(SelectedInstallation.Path, pattern, SearchOption.AllDirectories))
                    {
                        File.Delete(file);
                        totalCount++;
                    }
                }

                StatusMessage = $"All data files deletion complete ({totalCount} files)";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error deleting files: {ex.Message}";
            }
        }

        [RelayCommand]
        private void DeleteJson() => DeleteFilesByPattern("*.json", "JSON");

        [RelayCommand]
        private void DeleteRetention() => DeleteFilesByPattern("*.retention", "Retention");

        [RelayCommand]
        private void DeletePython() => DeleteFilesByPattern("*.py", "Python");

        [RelayCommand]
        private void DeletePageStubs() => DeleteFilesByPattern("*.stub", "Page Stubs");

    private void DeleteFilesByPattern(string pattern, string fileType)
    {
        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: Please select a target installation";
            return;
        }

        try
        {
            StatusMessage = $"Deleting {fileType}...";

            int count = 0;
            foreach (string file in Directory.GetFiles(SelectedInstallation.Path, pattern, SearchOption.AllDirectories))
            {
                File.Delete(file);
                count++;
            }

            StatusMessage = $"{fileType} deletion complete ({count} files)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error deleting {fileType}: {ex.Message}";
        }
    }

    #endregion

    #region Utility Operations

    [RelayCommand]
    private async Task CheckNetworkAsync()
    {
        try
        {
            StatusMessage = "Checking network settings...";
            var output = new StringBuilder();
            output.AppendLine("=== Network Configuration ===\n");

            await Task.Run(() =>
            {
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = "powershell.exe",
                        Arguments = @"-ExecutionPolicy Bypass -Command ""Get-NetIPConfiguration | Format-Table -Property 'InterfaceAlias','IPv4Address' | Out-String""",
                        RedirectStandardOutput = true,
                        UseShellExecute = false,
                        CreateNoWindow = true
                    };

                    using var process = Process.Start(psi);
                    if (process is not null)
                    {
                        string result = process.StandardOutput.ReadToEnd();
                        process.WaitForExit();
                        output.AppendLine(result);
                    }
                }
                catch (Exception ex)
                {
                    output.AppendLine($"Error getting network config: {ex.Message}");
                }
            });

            output.AppendLine("\n=== Ping Tests ===\n");

            output.AppendLine("Pinging Galil (100.100.100.101)...");
            bool galilOnline = await PingHostAsync("100.100.100.101");
            output.AppendLine(galilOnline ? "    Status: Online" : "    Status: Offline");

            output.AppendLine("\nPinging Modbus I/O (100.100.100.110)...");
            bool modbusOnline = await PingHostAsync("100.100.100.110");
            output.AppendLine(modbusOnline ? "    Status: Online" : "    Status: Offline");

            output.AppendLine("\nPinging Camera (200.200.200.201)...");
            bool cameraOnline = await PingHostAsync("200.200.200.201");
            output.AppendLine(cameraOnline ? "    Status: Online" : "    Status: Offline");

            NetworkUtilityOutput = output.ToString();
            StatusMessage = "Network check complete";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error: {ex.Message}";
        }
    }

    private static async Task<bool> PingHostAsync(string host)
    {
        try
        {
            using var ping = new Ping();
            var reply = await ping.SendPingAsync(host, 500);
            return reply.Status == IPStatus.Success;
        }
        catch
        {
            return false;
        }
    }

    [RelayCommand]
    private async Task CheckLargeFilesAsync()
    {
        try
        {
            StatusMessage = "Searching for large files...";
            UtilityOutput = "Searching for files larger than 200MB...\nThis may take a while...\n";
            LargeFiles.Clear();

            var foundFiles = new List<LargeFileResult>();

            await Task.Run(() =>
            {
                string userPath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                const long sizeThreshold = 209715200; // 200MB
                SearchLargeFiles(userPath, sizeThreshold, foundFiles);
            });

            foreach (var file in foundFiles.OrderByDescending(f => f.SizeBytes))
            {
                LargeFiles.Add(file);
            }

            UtilityOutput = $"Found {LargeFiles.Count} files larger than 200MB.\nUse the buttons to open their locations.";
            StatusMessage = $"Large file search complete - Found {LargeFiles.Count} files";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error searching for large files: {ex.Message}";
        }
    }

    private static void SearchLargeFiles(string path, long sizeThreshold, List<LargeFileResult> results)
    {
        try
        {
            foreach (string file in Directory.GetFiles(path))
            {
                try
                {
                    var fileInfo = new FileInfo(file);
                    if (fileInfo.Length > sizeThreshold)
                    {
                        results.Add(new LargeFileResult(fileInfo.FullName, fileInfo.Length));
                    }
                }
                catch
                {
                    // Ignore individual file errors
                }
            }

            foreach (string dir in Directory.GetDirectories(path))
            {
                try
                {
                    SearchLargeFiles(dir, sizeThreshold, results);
                }
                catch
                {
                    // Ignore directory access errors
                }
            }
        }
        catch
        {
            // Ignore top-level errors
        }
    }

    #endregion

    #region PMX Launcher

    [RelayCommand]
    private void LaunchPmx()
    {
        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: Please select a target installation";
            return;
        }

        try
        {
            StatusMessage = "Launching PMX...";

            var args = new List<string>();

            if (OfflineMode)
            {
                args.Add("-offline");
            }

            if (AutoAdvance)
            {
                args.Add("-autoAdvance");
            }

            if (SoftwareRendering)
            {
                args.Add("-software");
            }

            if (FreeWindow)
            {
                args.Add("-freeWindow");
            }

            if (!string.IsNullOrWhiteSpace(StartPage))
            {
                args.Add($"-page:{StartPage}");
            }

            if (!string.IsNullOrWhiteSpace(WindowWidth) && !string.IsNullOrWhiteSpace(WindowHeight))
            {
                if (int.TryParse(WindowWidth, out int width) && int.TryParse(WindowHeight, out int height))
                {
                    args.Add($"-size:{width}:{height}");
                }
                else
                {
                    StatusMessage = "Error: Window size must be valid numbers";
                    return;
                }
            }

            if (!string.IsNullOrWhiteSpace(WindowX) && !string.IsNullOrWhiteSpace(WindowY))
            {
                if (int.TryParse(WindowX, out int x) && int.TryParse(WindowY, out int y))
                {
                    args.Add($"-position:{x}:{y}");
                }
                else
                {
                    StatusMessage = "Error: Window position must be valid numbers";
                    return;
                }
            }

            if (VisionDebug)
            {
                args.Add("-visionDebug");
            }

            if (VisionTrace)
            {
                args.Add("-visionTrace");
            }

            if (RecordOnStartup)
            {
                args.Add("-recordOnStartup");
            }

            if (RecordHighQuality)
            {
                args.Add("-recordHighQuality");
            }

            if (RecordHighFramerate)
            {
                args.Add("-recordHighFramerate");
            }

            if (RecordMicrophone)
            {
                args.Add("-recordMicrophone");
            }

            if (RecordWebcam)
            {
                args.Add("-recordWebcam");
            }

            if (!string.IsNullOrWhiteSpace(MaxSegments))
            {
                if (int.TryParse(MaxSegments, out int maxSegments))
                {
                    args.Add($"-recordMaxSegments:{maxSegments}");
                }
                else
                {
                    StatusMessage = "Error: Max segments must be a valid number";
                    return;
                }
            }

            string exePath = Path.Combine(SelectedInstallation.Path, "PVA.PathMasterX.exe");

            if (!File.Exists(exePath))
            {
                StatusMessage = $"Error: PMX executable not found at {exePath}";
                return;
            }

            Process.Start(new ProcessStartInfo
            {
                FileName = exePath,
                Arguments = string.Join(" ", args),
                WorkingDirectory = SelectedInstallation.Path,
                UseShellExecute = true
            });

            StatusMessage = $"PMX launched with arguments: {string.Join(" ", args)}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error launching PMX: {ex.Message}";
        }
    }

    #endregion

    #region File Operations Helper Methods

    private static void CopyDirectoryStructure(string sourceDir, string targetDir)
    {
        foreach (string dir in Directory.GetDirectories(sourceDir, "*", SearchOption.AllDirectories))
        {
            string relativePath = Path.GetRelativePath(sourceDir, dir);
            string newDir = Path.Combine(targetDir, relativePath);
            Directory.CreateDirectory(newDir);
        }
    }

    private static void CopyFilesByPattern(string sourceDir, string targetDir, string pattern)
    {
        foreach (string file in Directory.GetFiles(sourceDir, pattern, SearchOption.AllDirectories))
        {
            string relativePath = Path.GetRelativePath(sourceDir, file);
            string targetFile = Path.Combine(targetDir, relativePath);

            string? targetFileDir = Path.GetDirectoryName(targetFile);
            if (targetFileDir is not null && !Directory.Exists(targetFileDir))
            {
                Directory.CreateDirectory(targetFileDir);
            }

            File.Copy(file, targetFile, true);
        }
    }

    private static void CopyDirectoryRecursive(string sourceDir, string targetDir)
    {
        foreach (string file in Directory.GetFiles(sourceDir, "*", SearchOption.AllDirectories))
        {
            string relativePath = Path.GetRelativePath(sourceDir, file);
            string targetFile = Path.Combine(targetDir, relativePath);

            string? targetFileDir = Path.GetDirectoryName(targetFile);
            if (targetFileDir is not null && !Directory.Exists(targetFileDir))
            {
                Directory.CreateDirectory(targetFileDir);
            }

            File.Copy(file, targetFile, true);
        }
    }

    #endregion
}
