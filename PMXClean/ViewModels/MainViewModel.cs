namespace PMXClean.ViewModels;

using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Net.NetworkInformation;
using System.Reflection;
using System.Text;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using PMXClean.Models;
using PMXClean.Services;

/// <summary>
/// Main ViewModel for the PMXClean application.
/// </summary>
public sealed partial class MainViewModel : ObservableObject
{
    private readonly string _appBaseDirectory;
    private readonly string _backupsRootDirectory;
    private readonly string _comparisonTempDirectory;

    public MainViewModel()
    {
        _appBaseDirectory = AppDomain.CurrentDomain.BaseDirectory;
        _backupsRootDirectory = Path.Combine(_appBaseDirectory, "Backups");
        _comparisonTempDirectory = Path.Combine(Path.GetTempPath(), "PMXClean_Compare");

        Installations = [];
        AvailableVersions = [];
        BackupInstances = [];

        ComparisonViewModel = new ComparisonViewModel
        {
            OnComparisonStarted = () => IsComparisonVisible = true
        };

        Initialize();
    }

    #region Observable Properties

    [ObservableProperty]
    public partial string StatusMessage { get; set; } = "Ready";

    [ObservableProperty]
    public partial string FileVersionText { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string VersionInfoText { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string BackupInfoText { get; set; } = "No backup selected. Create a new backup to begin.";

    [ObservableProperty]
    public partial string UtilityOutput { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string EventSearchStatus { get; set; } = string.Empty;

    [ObservableProperty]
    public partial PathMasterXInstallation? SelectedInstallation { get; set; }

    [ObservableProperty]
    public partial string? SelectedVersion { get; set; }

    [ObservableProperty]
    public partial string? SelectedBackup { get; set; }

    [ObservableProperty]
    public partial bool IsBackupRenaming { get; set; }

    [ObservableProperty]
    public partial bool IsBackupCreating { get; set; }

    [ObservableProperty]
    public partial string BackupEditName { get; set; } = string.Empty;

    // PMX Launcher properties
    [ObservableProperty]
    public partial bool OfflineMode { get; set; }

    [ObservableProperty]
    public partial bool AutoAdvance { get; set; }

    [ObservableProperty]
    public partial bool SoftwareRendering { get; set; }

    [ObservableProperty]
    public partial bool FreeWindow { get; set; }

    [ObservableProperty]
    public partial string StartPage { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string WindowWidth { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string WindowHeight { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string WindowX { get; set; } = string.Empty;

    [ObservableProperty]
    public partial string WindowY { get; set; } = string.Empty;

    [ObservableProperty]
    public partial bool VisionDebug { get; set; }

    [ObservableProperty]
    public partial bool VisionTrace { get; set; }

    [ObservableProperty]
    public partial bool RecordOnStartup { get; set; }

    [ObservableProperty]
    public partial bool RecordHighQuality { get; set; }

    [ObservableProperty]
    public partial bool RecordHighFramerate { get; set; }

    [ObservableProperty]
    public partial bool RecordMicrophone { get; set; }

    [ObservableProperty]
    public partial bool RecordWebcam { get; set; }

    [ObservableProperty]
    public partial string MaxSegments { get; set; } = string.Empty;

    [ObservableProperty]
    public partial int LockedFileCount { get; set; }

    [ObservableProperty]
    public partial bool IsComparisonVisible { get; set; }

    [ObservableProperty]
    public partial LockedFileItem? SelectedLockedFile { get; set; }

    [ObservableProperty]
    public partial string SelectedLockedFileContent { get; set; } = string.Empty;

    /// <summary>
    /// Comparison result for the selected locked file when comparing against a version.
    /// </summary>
    [ObservableProperty]
    public partial FileComparisonResult? LockedFileComparisonResult { get; set; }

    /// <summary>
    /// The version being compared against for the locked file comparison.
    /// </summary>
    [ObservableProperty]
    public partial string? LockedFileComparisonVersion { get; set; }

    /// <summary>
    /// Whether the locked file viewer is showing a comparison.
    /// </summary>
    public bool IsLockedFileComparisonActive => LockedFileComparisonResult is not null;

    /// <summary>
    /// Currently loaded .machine backup info (displayed in header).
    /// </summary>
    [ObservableProperty]
    public partial MachineBackupInfo? LoadedMachineBackup { get; set; }

    /// <summary>
    /// Whether a .machine backup is currently loaded as an installation target.
    /// </summary>
    public bool IsBackupLoaded => LoadedMachineBackup is not null;

    /// <summary>
    /// Whether the selected installation is a backup (deletion should be disabled).
    /// </summary>
    public bool IsSelectedInstallationABackup => SelectedInstallation?.IsBackup ?? false;

    #endregion

    #region Collections

    public ObservableCollection<PathMasterXInstallation> Installations { get; }
        public ObservableCollection<string> AvailableVersions { get; }
        public ObservableCollection<string> BackupInstances { get; }
        public ObservableCollection<LargeFileResult> LargeFiles { get; } = [];
        public ObservableCollection<LockedFileItem> LockedFiles { get; } = [];
        public ObservableCollection<PageInfo> AvailablePages { get; } = [];
        public ObservableCollection<SystemStatusItem> SystemStatusItems { get; } = [];
        public ObservableCollection<SystemStatusItem> NetworkStatusItems { get; } = [];
        public ObservableCollection<EventLogItem> EventLogItems { get; } = [];

        /// <summary>
        /// ViewModel for the built-in Python comparison feature.
        /// </summary>
        public ComparisonViewModel ComparisonViewModel { get; }

        #endregion

    #region Property Changed Handlers

    partial void OnSelectedInstallationChanged(PathMasterXInstallation? value)
    {
        if (value is not null)
        {
            StatusMessage = $"Selected: {value.DisplayName}";
            UpdateFileVersionDisplay();
            LoadAvailablePages();
            ScanForLockedFiles();
        }
        else
        {
            LockedFileCount = 0;
        }

        // Clear locked file selection when target changes
        SelectedLockedFile = null;
        SelectedLockedFileContent = string.Empty;

        // Notify backup-related property changes
        OnPropertyChanged(nameof(IsSelectedInstallationABackup));

        NotifyBackupAndCopyCommandsCanExecuteChanged();
        SetupComparisonPaths();
    }

    partial void OnSelectedVersionChanged(string? value)
    {
        UpdateVersionInfo();
        SetupComparisonPaths();
    }

    partial void OnSelectedBackupChanged(string? value)
    {
        UpdateBackupInfo();
        NotifyRemoveCommandsCanExecuteChanged();
        NotifyBackupAndCopyCommandsCanExecuteChanged();
    }

    partial void OnLoadedMachineBackupChanged(MachineBackupInfo? value)
    {
        OnPropertyChanged(nameof(IsBackupLoaded));
    }

    #endregion

    #region Initialization

    private void Initialize()
    {
        DiscoverInstallations();
        LoadAvailableVersions();
        LoadBackupInstances();
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

        // Preserve any loaded backup installation
        var backupInstallation = Installations.FirstOrDefault(i => i.IsBackup);

        Installations.Clear();

        SearchProgramFiles();
        SearchUserRepositories();

        // Sort: Production first, then Development, then Backup
        var sorted = Installations
            .OrderBy(i => i.Type switch
            {
                InstallationType.ProgramFiles => 0,
                InstallationType.UserDevelopment => 1,
                InstallationType.Custom => 2,
                InstallationType.MachineBackup => 3,
                _ => 4
            })
            .ThenBy(i => i.DisplayName)
            .ToList();

        Installations.Clear();
        foreach (var installation in sorted)
        {
            Installations.Add(installation);
        }

        // Re-add the backup installation if one was loaded
        if (backupInstallation is not null)
        {
            Installations.Add(backupInstallation);
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
                InstallationType.MachineBackup => $"[Backup] {path}",
                _ => $"[Dev] {path}"
            };
        }
        catch
        {
            return path;
        }
    }

    private void UpdateFileVersionDisplay()
    {
        if (SelectedInstallation is null)
        {
            FileVersionText = string.Empty;
            return;
        }

        // For backup installations, show version from Headers.data
        if (SelectedInstallation.IsBackup && SelectedInstallation.BackupInfo is not null)
        {
            var backup = SelectedInstallation.BackupInfo;
            string backupType = backup.IsFullBackup ? "Full Backup" : "Regular Backup";
            FileVersionText = $"Backup Version: {backup.BackupVersion} ({backupType})";
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

    #region Machine Backup Loading

    /// <summary>
    /// Loads a .machine backup file and adds it to the installations list.
    /// </summary>
    [RelayCommand]
    private async Task LoadMachineBackupAsync()
    {
        var dialog = new Microsoft.Win32.OpenFileDialog
        {
            Title = "Select Machine Backup",
            Filter = "Machine Backup Files (*.machine)|*.machine|All Files (*.*)|*.*",
            FilterIndex = 1
        };

        if (dialog.ShowDialog() == true)
        {
            await LoadMachineBackupFromPathAsync(dialog.FileName);
        }
    }

    /// <summary>
    /// Loads a .machine backup from a specific file path asynchronously.
    /// </summary>
    public async Task LoadMachineBackupFromPathAsync(string filePath)
    {
        if (string.IsNullOrEmpty(filePath) || !File.Exists(filePath))
        {
            StatusMessage = "Error: Invalid backup file path";
            return;
        }

        try
        {
            StatusMessage = "Loading machine backup...";

            // Validate the file
            if (!MachineBackupService.IsValidMachineBackup(filePath))
            {
                StatusMessage = "Error: Invalid .machine backup file (missing Headers.data)";
                return;
            }

            // Unload any existing backup first
            await UnloadCurrentMachineBackupAsync();

            // Load the backup asynchronously
            var backupInfo = await MachineBackupService.LoadBackupAsync(filePath);
            LoadedMachineBackup = backupInfo;

            // Create installation entry for the backup
            var backupInstallation = new PathMasterXInstallation
            {
                Path = backupInfo.ExtractedPath,
                DisplayName = $"[Backup] {backupInfo.FileName} (v{backupInfo.BackupVersion})",
                Type = InstallationType.MachineBackup,
                BackupInfo = backupInfo
            };

            // Add to installations and select it
            Installations.Add(backupInstallation);
            SelectedInstallation = backupInstallation;

            string backupType = backupInfo.IsFullBackup ? "Full Backup" : "Regular Backup";
            string customDllWarning = backupInfo.HasCustomDlls 
                ? $" - Contains {backupInfo.CustomDlls.Count} custom DLL(s)" 
                : "";

            StatusMessage = $"Loaded {backupType}: {backupInfo.FileName} (v{backupInfo.BackupVersion}){customDllWarning}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error loading backup: {ex.Message}";
        }
    }

    /// <summary>
    /// Unloads the current machine backup and cleans up temporary files.
    /// </summary>
    [RelayCommand(CanExecute = nameof(CanUnloadMachineBackup))]
    private async Task UnloadMachineBackupAsync()
    {
        await UnloadCurrentMachineBackupAsync();
        StatusMessage = "Machine backup unloaded";
    }

    private bool CanUnloadMachineBackup() => LoadedMachineBackup is not null;

    private async Task UnloadCurrentMachineBackupAsync()
    {
        if (LoadedMachineBackup is null)
        {
            return;
        }

        // If the backup installation is selected, clear selection
        if (SelectedInstallation?.IsBackup == true && 
            SelectedInstallation.BackupInfo == LoadedMachineBackup)
        {
            SelectedInstallation = Installations.FirstOrDefault(i => !i.IsBackup);
        }

        // Remove backup from installations list
        var backupInstallation = Installations.FirstOrDefault(i => i.BackupInfo == LoadedMachineBackup);
        if (backupInstallation is not null)
        {
            Installations.Remove(backupInstallation);
        }

        // Dispose and clean up temp files asynchronously
        var tempPath = LoadedMachineBackup.ExtractedPath;
        LoadedMachineBackup = null;
        await MachineBackupService.CleanupTempFolderAsync(tempPath);
    }

    /// <summary>
    /// Handles drag-and-drop of .machine files asynchronously.
    /// </summary>
    public async Task HandleFileDropAsync(string[] files)
    {
        var machineFile = files.FirstOrDefault(f => 
            f.EndsWith(".machine", StringComparison.OrdinalIgnoreCase));

        if (machineFile is not null)
        {
            await LoadMachineBackupFromPathAsync(machineFile);
        }
        else
        {
            StatusMessage = "Error: No .machine backup file found in dropped items";
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

        VersionInfoText = $"{fileCount} Python files";
    }

    /// <summary>
    /// Sets up the comparison paths when version or installation changes.
    /// Extracts the embedded version files to a temp directory and configures the ComparisonViewModel.
    /// </summary>
    private void SetupComparisonPaths()
    {
        if (string.IsNullOrEmpty(SelectedVersion) || SelectedInstallation is null)
        {
            return;
        }

        try
        {
            string sourceDir = Path.Combine(_comparisonTempDirectory, "source");
            CleanAndCreateDirectory(sourceDir);
            int extractedCount = ExtractEmbeddedVersionFiles(SelectedVersion, sourceDir);

            if (extractedCount == 0)
            {
                StatusMessage = $"No files found for version {SelectedVersion}";
                return;
            }

            // Determine the right label based on whether target is a backup
            string targetLabel = SelectedInstallation.IsBackup 
                ? $"Backup ({SelectedInstallation.BackupInfo?.BackupVersion ?? "?"})"
                : "Installed";

            ComparisonViewModel.SetupComparison(
                sourceDir,
                SelectedInstallation.Path,
                SelectedVersion,
                targetLabel);
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error setting up comparison: {ex.Message}";
        }
    }

    /// <summary>
    /// Command to select a comparison item from the file tree.
    /// </summary>
    [RelayCommand]
    private void SelectComparisonItem(ComparisonItem? item)
    {
        ComparisonViewModel.SelectedItem = item;
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
            string? fileVersion = null;

            // No machine backup loaded for comparison, match the executable version directly from the target path
            if (!SelectedInstallation.IsBackup)
            {
                string exePath = Path.Combine(SelectedInstallation.Path, "PVA.PathMasterX.exe");
                if (!File.Exists(exePath))
                {
                    StatusMessage = "Error: Target executable not found";
                    return;
                }

                var versionInfo = FileVersionInfo.GetVersionInfo(exePath);
                fileVersion = versionInfo.FileVersion;

                if (string.IsNullOrEmpty(fileVersion))
                {
                    StatusMessage = "Error: Could not read version from executable";
                    return;
                }
            }

            // a machine backup is loaded, extract the version from Headers.data
            else
            {
                if (SelectedInstallation.BackupInfo is not null)
                {
                    fileVersion = SelectedInstallation.BackupInfo.BackupVersion;
                }
                else
                {
                    StatusMessage = "Error: Backup information is missing";
                    return;
                }
            }

            var matchedVersion = AvailableVersions.FirstOrDefault(v =>
                v.Equals(fileVersion, StringComparison.OrdinalIgnoreCase));

            matchedVersion ??= AvailableVersions.FirstOrDefault(v => fileVersion.StartsWith(v, StringComparison.OrdinalIgnoreCase) || v.StartsWith(fileVersion, StringComparison.OrdinalIgnoreCase));

            if (matchedVersion is not null)
            {
                SelectedVersion = matchedVersion;
                StatusMessage = $"Auto-matched to version: {matchedVersion}";
            }
            else
            {
                StatusMessage = $"No matching version found for {fileVersion}";
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

    #endregion

    #region Page Discovery

    /// <summary>
    /// Scans the selected installation's Base\UI\Pages\ directory for *.stub files
    /// and builds a collection of available pages with their UI paths.
    /// </summary>
    private void LoadAvailablePages()
    {
        AvailablePages.Clear();

        if (SelectedInstallation is null)
        {
            return;
        }

        try
        {
            string pagesPath = Path.Combine(SelectedInstallation.Path, "Base", "UI", "Pages");

            if (!Directory.Exists(pagesPath))
            {
                Debug.WriteLine($"Pages directory not found: {pagesPath}");
                return;
            }

            var stubFiles = Directory.GetFiles(pagesPath, "*.stub", SearchOption.AllDirectories);

            foreach (var stubFile in stubFiles)
            {
                try
                {
                    // Get the relative path from the Pages directory
                    string relativePath = Path.GetRelativePath(pagesPath, stubFile);

                    // Remove the .stub extension
                    string pathWithoutExtension = relativePath[.. ^Path.GetFileName(relativePath).Length]; // Remove ".stub"

                    // Get just the filename without extension for the name
                    string name = Path.GetFileNameWithoutExtension(stubFile);

                    // The UI path is the relative path with backslashes, without the extension
                    string uiPath = pathWithoutExtension.Replace(Path.DirectorySeparatorChar, '\\');

                    AvailablePages.Add(new PageInfo
                    {
                        Name = name,
                        UIPath = uiPath
                    });
                }
                catch (Exception ex)
                {
                    Debug.WriteLine($"Error processing stub file {stubFile}: {ex.Message}");
                }
            }

            // Sort by UI path for easier navigation
            var sortedPages = AvailablePages.OrderBy(p => p.UIPath).ToList();
            AvailablePages.Clear();
            foreach (var page in sortedPages)
            {
                AvailablePages.Add(page);
            }

            Debug.WriteLine($"Loaded {AvailablePages.Count} page(s) from {pagesPath}");
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error loading available pages: {ex.Message}");
        }
    }

    /// <summary>
    /// Selects a page from the available pages and sets it as the StartPage.
    /// </summary>
    [RelayCommand]
    private void SelectPage(PageInfo? page)
    {
        if (page is not null)
        {
            StartPage = page.Name;
            StatusMessage = $"Selected startup page: {page.UIPath}{page.Name}";
        }
    }

    #endregion

    #region Locked File Detection

    /// <summary>
    /// Scans the selected installation for Python files with #lock in the first line
    /// and builds a hierarchical tree structure.
    /// </summary>
    private void ScanForLockedFiles()
    {
        LockedFiles.Clear();
        LockedFileCount = 0;

        if (SelectedInstallation is null)
        {
            return;
        }

        try
        {
            var pythonFiles = Directory.GetFiles(SelectedInstallation.Path, "*.py", SearchOption.AllDirectories);
            var lockedFilePaths = new List<string>();

            foreach (var file in pythonFiles)
            {
                try
                {
                    // Read only the first line of the file
                    using var reader = new StreamReader(file);
                    string? firstLine = reader.ReadLine();

                    if (firstLine is not null && firstLine.Contains("#lock", StringComparison.OrdinalIgnoreCase))
                    {
                        lockedFilePaths.Add(file);
                    }
                }
                catch (Exception ex)
                {
                    Debug.WriteLine($"Error reading file {file}: {ex.Message}");
                }
            }

            LockedFileCount = lockedFilePaths.Count;

            // Build tree structure
            if (lockedFilePaths.Count > 0)
            {
                BuildLockedFileTree(lockedFilePaths);
            }

            Debug.WriteLine($"Found {lockedFilePaths.Count} locked Python file(s) in {SelectedInstallation.Path}");
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error scanning for locked files: {ex.Message}");
            LockedFileCount = 0;
        }
    }

    /// <summary>
    /// Builds a hierarchical tree structure from locked file paths.
    /// </summary>
    private void BuildLockedFileTree(List<string> filePaths)
    {
        var root = new Dictionary<string, LockedFileItem>();

        foreach (var filePath in filePaths)
        {
            string relativePath = Path.GetRelativePath(SelectedInstallation!.Path, filePath);
            string[] parts = relativePath.Split(Path.DirectorySeparatorChar);

            var currentLevel = root;
            LockedFileItem? currentParent = null;
            string currentPath = string.Empty;

            for (int i = 0; i < parts.Length; i++)
            {
                string part = parts[i];
                currentPath = string.IsNullOrEmpty(currentPath) ? part : Path.Combine(currentPath, part);
                bool isFile = i == parts.Length - 1;

                if (!currentLevel.TryGetValue(part, out LockedFileItem? value))
                {
                    var item = new LockedFileItem
                    {
                        Name = part,
                        FullPath = isFile ? filePath : Path.Combine(SelectedInstallation.Path, currentPath),
                        RelativePath = currentPath,
                        IsFolder = !isFile,
                        Content = null
                    };
                    value = item;
                    currentLevel[part] = value;

                    if (currentParent is null)
                    {
                        LockedFiles.Add(item);
                    }
                    else
                    {
                        currentParent.Children.Add(item);
                    }
                }

                if (!isFile)
                {
                    currentParent = value;
                    // Create a child level if it doesn't exist
                    var childLevel = new Dictionary<string, LockedFileItem>();
                    foreach (var child in currentParent.Children)
                    {
                        childLevel[child.Name] = child;
                    }

                    currentLevel = childLevel;
                }
            }
        }
    }

    /// <summary>
    /// Selects a locked file and loads its content for display.
    /// </summary>
    [RelayCommand]
    private void SelectLockedFile(LockedFileItem? item)
    {
        if (item is null || item.IsFolder)
        {
            return;
        }

        SelectedLockedFile = item;
    }

    /// <summary>
    /// Handles selection change to load file content.
    /// </summary>
    partial void OnSelectedLockedFileChanged(LockedFileItem? value)
    {
        // Clear any active comparison when file selection changes
        LockedFileComparisonResult = null;
        LockedFileComparisonVersion = null;
        OnPropertyChanged(nameof(IsLockedFileComparisonActive));

        if (value is null || value.IsFolder)
        {
            SelectedLockedFileContent = string.Empty;
            return;
        }

        try
        {
            // Load file content
            SelectedLockedFileContent = File.ReadAllText(value.FullPath);
        }
        catch (Exception ex)
        {
            SelectedLockedFileContent = $"Error loading file: {ex.Message}";
        }
    }

    /// <summary>
    /// Opens the selected locked file in File Explorer and selects it.
    /// </summary>
    [RelayCommand]
    private void OpenLockedFileInExplorer()
    {
        if (SelectedLockedFile is null || SelectedLockedFile.IsFolder)
        {
            StatusMessage = "Error: No file selected";
            return;
        }

        if (!File.Exists(SelectedLockedFile.FullPath))
        {
            StatusMessage = "Error: File does not exist";
            return;
        }

        try
        {
            Process.Start(new ProcessStartInfo
            {
                FileName = "explorer.exe",
                Arguments = $"/select,\"{SelectedLockedFile.FullPath}\"",
                UseShellExecute = true
            });

            StatusMessage = $"Opened file in Explorer: {SelectedLockedFile.Name}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error opening file in Explorer: {ex.Message}";
        }
    }

    [RelayCommand]
    private void ClearSelectedLockedFile()
    {
        SelectedLockedFile = null;
        ClearLockedFileComparison();
    }

    /// <summary>
    /// Compares the selected locked file against a specific version from embedded resources.
    /// </summary>
    [RelayCommand]
    private void CompareLockedFileAgainstVersion(string? version)
    {
        if (string.IsNullOrEmpty(version))
        {
            StatusMessage = "Error: No version specified for comparison";
            return;
        }

        if (SelectedLockedFile is null || SelectedLockedFile.IsFolder)
        {
            StatusMessage = "Error: Please select a file (not a folder) to compare";
            return;
        }

        if (SelectedInstallation is null)
        {
            StatusMessage = "Error: No installation selected";
            return;
        }

        try
        {
            StatusMessage = $"Comparing {SelectedLockedFile.Name} against version {version}...";

            // Get the relative path of the file from the installation root
            string relativePath = SelectedLockedFile.RelativePath;

            // Build the embedded resource name for this file in the specified version
            string resourceName = $"PMXVersions\\{version}\\{relativePath}";

            // Extract the version file to a temp location for comparison
            string? versionFilePath = ExtractEmbeddedFileForComparison(resourceName, version, relativePath);

            // Perform the comparison
            LockedFileComparisonResult = PythonComparisonService.CompareFiles(
                versionFilePath,
                SelectedLockedFile.FullPath,
                relativePath);

            LockedFileComparisonVersion = version;
            OnPropertyChanged(nameof(IsLockedFileComparisonActive));

            string statusDesc = LockedFileComparisonResult.Status switch
            {
                FileComparisonStatus.Same => "Files are identical",
                FileComparisonStatus.Different => $"Files differ ({LockedFileComparisonResult.AddedLines} added, {LockedFileComparisonResult.RemovedLines} removed)",
                FileComparisonStatus.LeftOnly => "File only exists in version (not in installation)",
                FileComparisonStatus.RightOnly => "File only exists in installation (not in version)",
                _ => "Comparison complete"
            };

            StatusMessage = $"Compared {SelectedLockedFile.Name} vs {version}: {statusDesc}";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error comparing file: {ex.Message}";
            LockedFileComparisonResult = null;
            LockedFileComparisonVersion = null;
            OnPropertyChanged(nameof(IsLockedFileComparisonActive));
        }
    }

    /// <summary>
    /// Extracts an embedded resource file to a temporary location for comparison.
    /// </summary>
    private string? ExtractEmbeddedFileForComparison(string resourceName, string version, string relativePath)
    {
        var assembly = Assembly.GetExecutingAssembly();
        var resourceNames = assembly.GetManifestResourceNames();

        // Find a matching resource (case-insensitive)
        string? matchingResource = resourceNames.FirstOrDefault(r =>
            r.Equals(resourceName, StringComparison.OrdinalIgnoreCase));

        if (matchingResource is null)
        {
            // File doesn't exist in the version - return null
            return null;
        }

        // Create temp file path
        string tempDir = Path.Combine(Path.GetTempPath(), "PMXClean_Compare", "locked_file_compare", version);
        Directory.CreateDirectory(Path.GetDirectoryName(Path.Combine(tempDir, relativePath))!);
        string tempFilePath = Path.Combine(tempDir, relativePath);

        // Extract the resource
        using var stream = assembly.GetManifestResourceStream(matchingResource);
        if (stream is null)
        {
            return null;
        }

        using var fileStream = File.Create(tempFilePath);
        stream.CopyTo(fileStream);

        return tempFilePath;
    }

    /// <summary>
    /// Clears the locked file comparison and returns to plain content view.
    /// </summary>
    [RelayCommand]
    private void ClearLockedFileComparison()
    {
        LockedFileComparisonResult = null;
        LockedFileComparisonVersion = null;
        OnPropertyChanged(nameof(IsLockedFileComparisonActive));
    }

    /// <summary>
    /// Closes the comparison view and returns to locked file browser.
    /// </summary>
    [RelayCommand]
    private void CloseComparison()
    {
        IsComparisonVisible = false;
        StatusMessage = "Comparison closed";
    }

    /// <summary>
    /// Expands all locked file tree items.
    /// </summary>
    [RelayCommand]
    private void ExpandAllLockedFiles()
    {
        SetLockedFilesExpandedState(LockedFiles, true);
    }

    /// <summary>
    /// Collapses all locked file tree items.
    /// </summary>
    [RelayCommand]
    private void CollapseAllLockedFiles()
    {
        SetLockedFilesExpandedState(LockedFiles, false);
    }

    /// <summary>
    /// Recursively sets the expanded state of locked file tree items.
    /// </summary>
    private static void SetLockedFilesExpandedState(ObservableCollection<LockedFileItem> items, bool expanded)
    {
        foreach (var item in items)
        {
            if (item.IsFolder)
            {
                item.IsExpanded = expanded;
                SetLockedFilesExpandedState(item.Children, expanded);
            }
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
        IsBackupRenaming = false;
        BackupEditName = $"Backup_{DateTime.Now:yyyyMMdd_HHmmss}";
        CreateNewBackup(BackupEditName);
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
        if (IsBackupRenaming && !string.IsNullOrEmpty(SelectedBackup))
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
        private void OpenBackupFolder()
        {
            if (string.IsNullOrEmpty(SelectedBackup))
            {
                // Open the root backups directory if no backup selected
                if (!Directory.Exists(_backupsRootDirectory))
                {
                    Directory.CreateDirectory(_backupsRootDirectory);
                }

                Process.Start(new ProcessStartInfo
                {
                    FileName = "explorer.exe",
                    Arguments = _backupsRootDirectory,
                    UseShellExecute = true
                });
                StatusMessage = "Opened backups root folder";
                return;
            }

            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);

            if (!Directory.Exists(backupPath))
            {
                StatusMessage = "Error: Backup folder does not exist";
                return;
            }

            try
            {
                Process.Start(new ProcessStartInfo
                {
                    FileName = "explorer.exe",
                    Arguments = backupPath,
                    UseShellExecute = true
                });
                StatusMessage = $"Opened backup folder: {SelectedBackup}";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error opening backup folder: {ex.Message}";
            }
        }

        [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
        private async Task BackupAllFilesAsync()
        {
            if (!ValidateBackupSelected())
            {
                return;
            }

            try
            {
                StatusMessage = "Backing up all files...";

                // Call each individual backup method
                await BackupFilesByPatternAsync("*.json", "JSON");
                await BackupFilesByPatternAsync("*.retention", "Retention");
                await BackupFilesByPatternAsync("*.py", "Python");
                await BackupFilesByPatternAsync("*.stub", "Page Stubs");
                await BackupCameraFilesCoreAsync();
                await BackupFeatureFolderAsync("Program", "Program");
                await BackupFeatureFolderAsync("Inspection", "Inspection");
                await BackupFilesByPatternAsync("*.DLL", "DLLs");

                UpdateBackupInfo();
                NotifyRemoveCommandsCanExecuteChanged();
                StatusMessage = "All files backup complete";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error backing up all files: {ex.Message}";
            }
        }

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task BackupJsonAsync() => await BackupFilesByPatternAsync("*.json", "JSON");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task BackupRetentionAsync() => await BackupFilesByPatternAsync("*.retention", "Retention");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task BackupPythonAsync() => await BackupFilesByPatternAsync("*.py", "Python");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task BackupDllsAsync() => await BackupFilesByPatternAsync("*.DLL", "DLLs");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task BackupStubsAsync() => await BackupFilesByPatternAsync("*.stub", "Page Stubs");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task BackupCameraFilesAsync()
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        await BackupCameraFilesCoreAsync();
    }

    private async Task BackupCameraFilesCoreAsync()
    {
        try
        {
            StatusMessage = "Backing up Camera files...";
            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup!);
            string cameraSourcePath = Path.Combine(SelectedInstallation!.Path, "Device", "Camera", "Drivers");

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

            await Task.Run(() =>
            {
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
            });

            UpdateBackupInfo();
            NotifyRemoveCommandsCanExecuteChanged();
            StatusMessage = $"Camera files backup complete ({copiedCount} files)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error backing up Camera files: {ex.Message}";
        }
    }

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task BackupProgramFilesAsync()
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        await BackupFeatureFolderAsync("Program", "Program");
    }

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task BackupInspectionFilesAsync()
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        await BackupFeatureFolderAsync("Inspection", "Inspection");
    }

    private async Task BackupFeatureFolderAsync(string folderName, string displayName)
    {
        try
        {
            StatusMessage = $"Backing up {displayName} files...";
            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup!);
            string featureSourcePath = Path.Combine(SelectedInstallation!.Path, "Feature", folderName);

            if (!Directory.Exists(featureSourcePath))
            {
                StatusMessage = $"{displayName} folder not found in target installation";
                return;
            }

            if (!Directory.Exists(backupPath))
            {
                Directory.CreateDirectory(backupPath);
            }

            // Excluded: .dll files, Localization folder, Functions folder
            string[] excludedFolders = ["Localization", "Functions"];
            int copiedCount = 0;

            await Task.Run(() =>
            {
                foreach (string file in Directory.GetFiles(featureSourcePath, "*", SearchOption.AllDirectories))
                {
                    // Skip .dll files
                    if (Path.GetExtension(file).Equals(".dll", StringComparison.OrdinalIgnoreCase))
                    {
                        continue;
                    }

                    // Skip files in excluded folders
                    string? directory = Path.GetDirectoryName(file);
                    if (directory is not null && excludedFolders.Any(ef =>
                        directory.Contains(Path.DirectorySeparatorChar + ef + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase) ||
                        directory.EndsWith(Path.DirectorySeparatorChar + ef, StringComparison.OrdinalIgnoreCase)))
                    {
                        continue;
                    }

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
            });

            UpdateBackupInfo();
            NotifyRemoveCommandsCanExecuteChanged();
            StatusMessage = $"{displayName} files backup complete ({copiedCount} files)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error backing up {displayName} files: {ex.Message}";
        }
    }

    #region Copy to Destination Commands

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task CopyJsonToDestinationAsync() => await CopyToDestinationByPatternAsync("*.json", "JSON");

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task CopyRetentionToDestinationAsync() => await CopyToDestinationByPatternAsync("*.retention", "Retention");

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task CopyPythonToDestinationAsync() => await CopyToDestinationByPatternAsync("*.py", "Python");

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task CopyDllsToDestinationAsync() => await CopyToDestinationByPatternAsync("*.DLL", "DLLs");

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task CopyStubsToDestinationAsync() => await CopyToDestinationByPatternAsync("*.stub", "Page Stubs");

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task CopyCameraFilesToDestinationAsync()
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

            await Task.Run(() =>
            {
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
            });

            StatusMessage = $"Camera files copied to destination ({copiedCount} files)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error copying Camera files: {ex.Message}";
        }
    }

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task CopyProgramFilesToDestinationAsync()
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        await CopyFeatureFolderToDestinationAsync("Program", "Program");
    }

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task CopyInspectionFilesToDestinationAsync()
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        await CopyFeatureFolderToDestinationAsync("Inspection", "Inspection");
    }

    private async Task CopyFeatureFolderToDestinationAsync(string folderName, string displayName)
    {
        try
        {
            StatusMessage = $"Copying {displayName} files to destination...";
            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup!);
            string featureBackupPath = Path.Combine(backupPath, "Feature", folderName);

            if (!Directory.Exists(featureBackupPath))
            {
                StatusMessage = $"No {displayName} files found in backup";
                return;
            }

            int copiedCount = 0;

            await Task.Run(() =>
            {
                foreach (string file in Directory.GetFiles(featureBackupPath, "*", SearchOption.AllDirectories))
                {
                    string relativePath = Path.GetRelativePath(backupPath, file);
                    string targetFile = Path.Combine(SelectedInstallation!.Path, relativePath);

                    string? targetFileDir = Path.GetDirectoryName(targetFile);
                    if (targetFileDir is not null && !Directory.Exists(targetFileDir))
                    {
                        Directory.CreateDirectory(targetFileDir);
                    }

                    File.Copy(file, targetFile, true);
                    copiedCount++;
                }
            });

            StatusMessage = $"{displayName} files copied to destination ({copiedCount} files)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error copying {displayName} files: {ex.Message}";
        }
    }

        private async Task CopyToDestinationByPatternAsync(string pattern, string fileType)
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

                bool anyFilesCopied = await CopyFilesByPatternAsync(backupPath, SelectedInstallation.Path, pattern);
                if (anyFilesCopied)
                {
                    StatusMessage = $"{fileType} copied to destination";
                }
                else
                {
                    StatusMessage = $"No {fileType} files found to copy";
                }
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error copying {fileType}: {ex.Message}";
            }
        }

        #endregion

        #region Remove from Backup Commands

        [RelayCommand(CanExecute = nameof(CanRemoveJsonFromBackup))]
        private async Task RemoveJsonFromBackupAsync() => await RemoveFromBackupByPatternAsync("*.json", "JSON");

        [RelayCommand(CanExecute = nameof(CanRemoveRetentionFromBackup))]
        private async Task RemoveRetentionFromBackupAsync() => await RemoveFromBackupByPatternAsync("*.retention", "Retention");

        [RelayCommand(CanExecute = nameof(CanRemovePythonFromBackup))]
        private async Task RemovePythonFromBackupAsync() => await RemoveFromBackupByPatternAsync("*.py", "Python");

        [RelayCommand(CanExecute = nameof(CanRemoveDllsFromBackup))]
        private async Task RemoveDllsFromBackupAsync() => await RemoveFromBackupByPatternAsync("*.DLL", "DLLs");

        [RelayCommand(CanExecute = nameof(CanRemoveStubsFromBackup))]
        private async Task RemoveStubsFromBackupAsync() => await RemoveFromBackupByPatternAsync("*.stub", "Page Stubs");

        [RelayCommand(CanExecute = nameof(CanRemoveCameraFilesFromBackup))]
        private async Task RemoveCameraFilesFromBackupAsync()
        {
            if (string.IsNullOrEmpty(SelectedBackup))
            {
                StatusMessage = "Error: Please select a backup first";
                return;
            }

            try
            {
                StatusMessage = "Removing Camera files from backup...";
                string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);
                string cameraBackupPath = Path.Combine(backupPath, "Device", "Camera");

                if (!Directory.Exists(cameraBackupPath))
                {
                    StatusMessage = "No Camera files found in backup";
                    return;
                }

                string[] excludedExtensions = [".dll", ".json", ".py"];
                int deletedCount = 0;

                await Task.Run(() =>
                {
                    foreach (string file in Directory.GetFiles(cameraBackupPath, "*", SearchOption.AllDirectories))
                    {
                        string extension = Path.GetExtension(file).ToLowerInvariant();
                        if (!excludedExtensions.Contains(extension))
                        {
                            File.Delete(file);
                            deletedCount++;
                        }
                    }

                    // Clean up empty directories
                    CleanupEmptyDirectories(cameraBackupPath);
                });

                UpdateBackupInfo();
                NotifyRemoveCommandsCanExecuteChanged();
                StatusMessage = $"Removed {deletedCount} Camera files from backup";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error removing Camera files from backup: {ex.Message}";
            }
        }

        [RelayCommand(CanExecute = nameof(CanRemoveProgramFilesFromBackup))]
        private async Task RemoveProgramFilesFromBackupAsync()
        {
            await RemoveFeatureFolderFromBackupAsync("Program", "Program");
        }

        [RelayCommand(CanExecute = nameof(CanRemoveInspectionFilesFromBackup))]
        private async Task RemoveInspectionFilesFromBackupAsync()
        {
            await RemoveFeatureFolderFromBackupAsync("Inspection", "Inspection");
        }

        private async Task RemoveFeatureFolderFromBackupAsync(string folderName, string displayName)
        {
            if (string.IsNullOrEmpty(SelectedBackup))
            {
                StatusMessage = "Error: Please select a backup first";
                return;
            }

            try
            {
                StatusMessage = $"Removing {displayName} files from backup...";
                string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);
                string featureBackupPath = Path.Combine(backupPath, "Feature", folderName);

                if (!Directory.Exists(featureBackupPath))
                {
                    StatusMessage = $"No {displayName} files found in backup";
                    return;
                }

                int deletedCount = 0;

                await Task.Run(() =>
                {
                    foreach (string file in Directory.GetFiles(featureBackupPath, "*", SearchOption.AllDirectories))
                    {
                        File.Delete(file);
                        deletedCount++;
                    }

                    // Clean up empty directories
                    CleanupEmptyDirectories(featureBackupPath);
                });

                UpdateBackupInfo();
                NotifyRemoveCommandsCanExecuteChanged();
                StatusMessage = $"Removed {deletedCount} {displayName} files from backup";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error removing {displayName} files from backup: {ex.Message}";
            }
        }

        private bool CanRemoveJsonFromBackup() => BackupHasFilesOfPattern("*.json");
        private bool CanRemoveRetentionFromBackup() => BackupHasFilesOfPattern("*.retention");
        private bool CanRemovePythonFromBackup() => BackupHasFilesOfPattern("*.py");
        private bool CanRemoveDllsFromBackup() => BackupHasFilesOfPattern("*.DLL");
        private bool CanRemoveStubsFromBackup() => BackupHasFilesOfPattern("*.stub");
        private bool CanRemoveCameraFilesFromBackup() => BackupHasCameraFiles();
        private bool CanRemoveProgramFilesFromBackup() => BackupHasFeatureFolder("Program");
        private bool CanRemoveInspectionFilesFromBackup() => BackupHasFeatureFolder("Inspection");

        private bool BackupHasFilesOfPattern(string pattern)
        {
            if (string.IsNullOrEmpty(SelectedBackup))
            {
                return false;
            }

            string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);

            if (!Directory.Exists(backupPath))
            {
                return false;
            }

            try
            {
                return Directory.GetFiles(backupPath, pattern, SearchOption.AllDirectories).Length > 0;
            }
            catch
            {
                return false;
            }
        }

        private bool BackupHasCameraFiles()
        {
            if (string.IsNullOrEmpty(SelectedBackup))
            {
                return false;
            }

            string cameraBackupPath = Path.Combine(_backupsRootDirectory, SelectedBackup, "Device", "Camera", "Drivers");

            if (!Directory.Exists(cameraBackupPath))
            {
                return false;
            }

            try
            {
                return Directory.GetFiles(cameraBackupPath, "*.MPAT", SearchOption.AllDirectories).Length > 0 ||
                Directory.GetFiles(cameraBackupPath, "*.mca", SearchOption.AllDirectories).Length > 0 ||
                Directory.GetFiles(cameraBackupPath, "*.tiff", SearchOption.AllDirectories).Length > 0 ||
                Directory.GetFiles(cameraBackupPath, "*.mim", SearchOption.AllDirectories).Length > 0;
            }
            catch
            {
                return false;
            }
        }

        private bool BackupHasFeatureFolder(string folderName)
        {
            if (string.IsNullOrEmpty(SelectedBackup))
            {
                return false;
            }

            string featureBackupPath = Path.Combine(_backupsRootDirectory, SelectedBackup, "Feature", folderName);

            if (!Directory.Exists(featureBackupPath))
            {
                return false;
            }

            try
            {
                return Directory.GetFiles(featureBackupPath, "*.program", SearchOption.AllDirectories).Length > 0;
            }
            catch
            {
                return false;
            }
        }

        private async Task RemoveFromBackupByPatternAsync(string pattern, string fileType)
        {
            if (string.IsNullOrEmpty(SelectedBackup))
            {
                StatusMessage = "Error: Please select a backup first";
                return;
            }

            try
            {
                StatusMessage = $"Removing {fileType} from backup...";
                string backupPath = Path.Combine(_backupsRootDirectory, SelectedBackup);

                if (!Directory.Exists(backupPath))
                {
                    StatusMessage = "Error: Backup folder does not exist";
                    return;
                }

                int deletedCount = 0;
                await Task.Run(() =>
                {
                    foreach (string file in Directory.GetFiles(backupPath, pattern, SearchOption.AllDirectories))
                    {
                        File.Delete(file);
                        deletedCount++;
                    }

                    // Clean up empty directories
                    CleanupEmptyDirectories(backupPath);
                });

                UpdateBackupInfo();
                NotifyRemoveCommandsCanExecuteChanged();
                StatusMessage = $"Removed {deletedCount} {fileType} files from backup";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error removing {fileType} from backup: {ex.Message}";
            }
        }

        private static void CleanupEmptyDirectories(string rootPath)
        {
            if (!Directory.Exists(rootPath))
            {
                return;
            }

            foreach (string dir in Directory.GetDirectories(rootPath, "*", SearchOption.AllDirectories)
                .OrderByDescending(d => d.Length))
            {
                try
                {
                    if (Directory.Exists(dir) && !Directory.EnumerateFileSystemEntries(dir).Any())
                    {
                        Directory.Delete(dir);
                    }
                }
                catch
                {
                    // Ignore errors when cleaning up empty directories
                }
            }
        }

        private void NotifyRemoveCommandsCanExecuteChanged()
        {
            RemoveJsonFromBackupCommand.NotifyCanExecuteChanged();
            RemoveRetentionFromBackupCommand.NotifyCanExecuteChanged();
            RemovePythonFromBackupCommand.NotifyCanExecuteChanged();
            RemoveDllsFromBackupCommand.NotifyCanExecuteChanged();
            RemoveStubsFromBackupCommand.NotifyCanExecuteChanged();
            RemoveCameraFilesFromBackupCommand.NotifyCanExecuteChanged();
            RemoveProgramFilesFromBackupCommand.NotifyCanExecuteChanged();
            RemoveInspectionFilesFromBackupCommand.NotifyCanExecuteChanged();
        }

        #endregion

    private async Task BackupFilesByPatternAsync(string pattern, string fileType)
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

            bool anyFilesCopied = false;
            await Task.Run(() =>
            {
                CopyDirectoryStructure(SelectedInstallation!.Path, backupPath);
                anyFilesCopied = CopyFilesByPattern(SelectedInstallation.Path, backupPath, pattern);
            });

            UpdateBackupInfo();
            NotifyRemoveCommandsCanExecuteChanged();
            if (anyFilesCopied)
            {
                StatusMessage = $"{fileType} backup complete";
            }
            else
            {
                StatusMessage = $"No {fileType} files found to backup";
            }
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error backing up {fileType}: {ex.Message}";
        }
    }

    /// <summary>
    /// Determines whether backup or copy-to-destination operations can execute.
    /// </summary>
    private bool CanBackupOrCopy() => !string.IsNullOrEmpty(SelectedBackup) && SelectedInstallation is not null;

    /// <summary>
    /// Determines whether copy-to-destination (write) operations can execute.
    /// Disabled when target is a .machine backup (read-only).
    /// </summary>
    private bool CanCopyToDestination() => CanBackupOrCopy() && !IsSelectedInstallationABackup;

    /// <summary>
    /// Notifies all backup and copy-to-destination commands to re-evaluate their CanExecute state.
    /// </summary>
    private void NotifyBackupAndCopyCommandsCanExecuteChanged()
    {
        BackupAllFilesCommand.NotifyCanExecuteChanged();
        BackupJsonCommand.NotifyCanExecuteChanged();
        BackupRetentionCommand.NotifyCanExecuteChanged();
        BackupPythonCommand.NotifyCanExecuteChanged();
        BackupDllsCommand.NotifyCanExecuteChanged();
        BackupStubsCommand.NotifyCanExecuteChanged();
        BackupCameraFilesCommand.NotifyCanExecuteChanged();
        BackupProgramFilesCommand.NotifyCanExecuteChanged();
        BackupInspectionFilesCommand.NotifyCanExecuteChanged();
        CopyJsonToDestinationCommand.NotifyCanExecuteChanged();
        CopyRetentionToDestinationCommand.NotifyCanExecuteChanged();
        CopyPythonToDestinationCommand.NotifyCanExecuteChanged();
        CopyDllsToDestinationCommand.NotifyCanExecuteChanged();
        CopyStubsToDestinationCommand.NotifyCanExecuteChanged();
        CopyCameraFilesToDestinationCommand.NotifyCanExecuteChanged();
        CopyProgramFilesToDestinationCommand.NotifyCanExecuteChanged();
        CopyInspectionFilesToDestinationCommand.NotifyCanExecuteChanged();
        RestoreBackupCommand.NotifyCanExecuteChanged();
        UnloadMachineBackupCommand.NotifyCanExecuteChanged();
    }

    [RelayCommand(CanExecute = nameof(CanCopyToDestination))]
    private async Task RestoreBackupAsync()
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

            await CopyDirectoryRecursiveAsync(backupPath, SelectedInstallation.Path);
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
        private async Task DeleteAllAsync()
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

                await Task.Run(() =>
                {
                    foreach (var pattern in patterns)
                    {
                        foreach (string file in Directory.GetFiles(SelectedInstallation.Path, pattern, SearchOption.AllDirectories))
                        {
                            File.Delete(file);
                            totalCount++;
                        }
                    }
                });

                StatusMessage = $"All data files deletion complete ({totalCount} files)";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Error deleting files: {ex.Message}";
            }
        }

        [RelayCommand]
        private async Task DeleteJsonAsync() => await DeleteFilesByPatternAsync("*.json", "JSON");

        [RelayCommand]
        private async Task DeleteRetentionAsync() => await DeleteFilesByPatternAsync("*.retention", "Retention");

        [RelayCommand]
        private async Task DeletePythonAsync() => await DeleteFilesByPatternAsync("*.py", "Python");

        [RelayCommand]
        private async Task DeletePageStubsAsync() => await DeleteFilesByPatternAsync("*.stub", "Page Stubs");

    private async Task DeleteFilesByPatternAsync(string pattern, string fileType)
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
            await Task.Run(() =>
            {
                foreach (string file in Directory.GetFiles(SelectedInstallation.Path, pattern, SearchOption.AllDirectories))
                {
                    File.Delete(file);
                    count++;
                }
            });

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
            NetworkStatusItems.Clear();

            await GetNetworkAdaptersAsync();
            await CheckNetworkDevicesAsync();

            StatusMessage = "Network check complete";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error: {ex.Message}";
        }
    }

    private async Task GetNetworkAdaptersAsync()
    {
        var items = new List<SystemStatusItem>();

        await Task.Run(() =>
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    Arguments = @"-ExecutionPolicy Bypass -Command ""
                        $adapters = Get-NetAdapter | Where-Object { 
                            $_.Status -eq 'Up' -and 
                            $_.Name -notlike 'WAN Miniport*' -and
                            $_.InterfaceDescription -notlike 'WAN Miniport*'
                        };
                        foreach ($adapter in $adapters) {
                            $name = $adapter.Name;
                            $status = $adapter.Status;
                            $ipv4 = '';
                            $gateway = '';
                            $dns = '';
                            $jumbo = '';
                            $description = $adapter.InterfaceDescription;

                            $ipConfig = Get-NetIPConfiguration -InterfaceAlias $adapter.Name -ErrorAction SilentlyContinue;
                            if ($ipConfig) {
                                if ($ipConfig.IPv4Address) { $ipv4 = $ipConfig.IPv4Address.IPAddress; }
                                if ($ipConfig.IPv4DefaultGateway) { $gateway = $ipConfig.IPv4DefaultGateway.NextHop; }
                                if ($ipConfig.DNSServer) {
                                    $dns = ($ipConfig.DNSServer | Where-Object { $_.AddressFamily -eq 2 } | Select-Object -ExpandProperty ServerAddresses) -join ', ';
                                }
                            }

                            if ($adapter.PhysicalMediaType -like '*802.3*') {
                                $props = Get-NetAdapterAdvancedProperty -Name $adapter.Name -ErrorAction SilentlyContinue;
                                $jumboVal = $props | Where-Object { $_.RegistryKeyword -eq '*JumboPacket' } | Select-Object -ExpandProperty DisplayValue -ErrorAction SilentlyContinue;
                                if ($jumboVal) { $jumbo = $jumboVal; }
                            }

                            Write-Output ('ADAPTER:' + $name + '|' + $status + '|' + $ipv4 + '|' + $gateway + '|' + $dns + '|' + $jumbo + '|' + $description);
                        }
                    """,
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(psi);
                if (process is not null)
                {
                    string result = process.StandardOutput.ReadToEnd();
                    process.WaitForExit();

                    var lines = result.Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
                    foreach (var line in lines)
                    {
                        if (line.StartsWith("ADAPTER:"))
                        {
                            var parts = line[8..].Split('|');
                            if (parts.Length >= 7)
                            {
                                string name = parts[0];
                                string status = parts[1];
                                string ipv4 = parts[2];
                                string gateway = parts[3];
                                string dns = parts[4];
                                string jumbo = parts[5];
                                string description = parts[6];

                                var details = new StringBuilder();
                                details.AppendLine($"Interface: {description}");
                                if (!string.IsNullOrEmpty(ipv4))
                                {
                                    details.AppendLine($"IPv4: {ipv4}");
                                }

                                if (!string.IsNullOrEmpty(gateway))
                                {
                                    details.AppendLine($"Gateway: {gateway}");
                                }

                                if (!string.IsNullOrEmpty(dns))
                                {
                                    details.AppendLine($"DNS: {dns}");
                                }

                                if (!string.IsNullOrEmpty(jumbo))
                                {
                                    details.AppendLine($"Jumbo Frames: {jumbo}");
                                }

                                items.Add(new SystemStatusItem
                                {
                                    Name = name,
                                    Category = "Adapter",
                                    Status = status == "Up" ? SystemStatus.Good : SystemStatus.Warning,
                                    StatusText = !string.IsNullOrEmpty(ipv4) ? ipv4 : status,
                                    Details = details.ToString().TrimEnd()
                                });
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                items.Add(new SystemStatusItem
                {
                    Name = "Network Adapters",
                    Category = "Adapter",
                    Status = SystemStatus.Unknown,
                    StatusText = "Error",
                    Details = $"Failed to query: {ex.Message}"
                });
            }
        });

        foreach (var item in items)
        {
            NetworkStatusItems.Add(item);
        }
    }

    private async Task CheckNetworkDevicesAsync()
    {
        var devices = new (string Name, string IP, string Description)[]
        {
            ("Galil Motion Controller", "100.100.100.101", "Primary motion controller for axis control"),
            ("Modbus I/O Module", "100.100.100.110", "Digital and analog I/O interface"),
            ("Camera", "200.200.200.201", "Vision system camera for inspection")
        };

        foreach (var (Name, IP, Description) in devices)
        {
            bool online = await PingHostAsync(IP);
            NetworkStatusItems.Add(new SystemStatusItem
            {
                Name = Name,
                Category = "Device",
                Status = online ? SystemStatus.Good : SystemStatus.Error,
                StatusText = online ? "Online" : "Offline",
                Details = $"IP: {IP}\n{Description}"
            });
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
            UtilityOutput = "Searching for files larger than 200MB...";
            LargeFiles.Clear();

            await Task.Run(() =>
            {
                string userPath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                const long sizeThreshold = 209715200; // 200MB
                SearchLargeFiles(userPath, sizeThreshold);
            });

            UtilityOutput = $"Found {LargeFiles.Count} files larger than 200MB";
            StatusMessage = $"Large file search complete - Found {LargeFiles.Count} files";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error searching for large files: {ex.Message}";
        }
    }

    private void SearchLargeFiles(string path, long sizeThreshold)
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
                        var result = new LargeFileResult(fileInfo.FullName, fileInfo.Length);

                        // Add to collection on UI thread, inserting in sorted order (largest first)
                        System.Windows.Application.Current.Dispatcher.InvokeAsync(() =>
                        {
                            int insertIndex = 0;
                            for (int i = 0; i < LargeFiles.Count; i++)
                            {
                                if (result.SizeBytes > LargeFiles[i].SizeBytes)
                                {
                                    insertIndex = i;
                                    break;
                                }

                                insertIndex = i + 1;
                            }

                            LargeFiles.Insert(insertIndex, result);
                            UtilityOutput = $"Found {LargeFiles.Count} files larger than 200MB...";
                        });
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
                    SearchLargeFiles(dir, sizeThreshold);
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

    [RelayCommand]
    private async Task SearchEventLogsAsync()
    {
        try
        {
            StatusMessage = "Searching Event Viewer for PathMasterX events...";
            EventSearchStatus = "Searching Application, System, and Windows Error Reporting logs...";
            EventLogItems.Clear();

            var searchTerms = new[]
            {
                "PVA.PathMasterX",
                "PathMasterX",
                "PathMaster X",
                "PathMaster"
            };

            var logNames = new[] { "Application", "System" };

            await Task.Run(() =>
            {
                foreach (var logName in logNames)
                {
                    SearchEventLog(logName, searchTerms);
                }

                // Also search Windows Error Reporting logs
                SearchWerLogs(searchTerms);
            });

            EventSearchStatus = $"Found {EventLogItems.Count} events related to PathMasterX";
            StatusMessage = $"Event search complete - Found {EventLogItems.Count} events";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error searching event logs: {ex.Message}";
            EventSearchStatus = $"Error: {ex.Message}";
        }
    }

    private void SearchEventLog(string logName, string[] searchTerms)
    {
        try
        {
            using var eventLog = new System.Diagnostics.EventLog(logName);
            var entries = eventLog.Entries.Cast<System.Diagnostics.EventLogEntry>()
                .OrderByDescending(e => e.TimeGenerated)
                .Take(10000); // Limit to recent entries for performance

            foreach (var entry in entries)
            {
                try
                {
                    string message = entry.Message ?? string.Empty;
                    string source = entry.Source ?? string.Empty;

                    bool isMatch = searchTerms.Any(term =>
                        message.Contains(term, StringComparison.OrdinalIgnoreCase) ||
                        source.Contains(term, StringComparison.OrdinalIgnoreCase));

                    if (isMatch)
                    {
                        var logItem = new EventLogItem
                        {
                            Name = source,
                            EventId = entry.InstanceId,
                            Level = ConvertToEventLogLevel(entry.EntryType),
                            StatusText = $"{entry.EntryType} - {entry.TimeGenerated:g}",
                            Details = message,
                            Category = logName,
                            TimeCreated = entry.TimeGenerated
                        };

                        System.Windows.Application.Current.Dispatcher.InvokeAsync(() =>
                        {
                            // Insert in sorted order by time (newest first)
                            int insertIndex = 0;
                            for (int i = 0; i < EventLogItems.Count; i++)
                            {
                                if (logItem.TimeCreated > EventLogItems[i].TimeCreated)
                                {
                                    insertIndex = i;
                                    break;
                                }

                                insertIndex = i + 1;
                            }

                            EventLogItems.Insert(insertIndex, logItem);
                            EventSearchStatus = $"Found {EventLogItems.Count} events...";
                        });
                    }
                }
                catch
                {
                    // Skip entries that can't be read
                }
            }
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error reading {logName} log: {ex.Message}");
        }
    }

    private void SearchWerLogs(string[] searchTerms)
    {
        try
        {
            // Search Windows Error Reporting with EventLogReader for better performance
            var query = new System.Diagnostics.Eventing.Reader.EventLogQuery(
                "Application",
                System.Diagnostics.Eventing.Reader.PathType.LogName,
                "*[System[Provider[@Name='Windows Error Reporting']]]");

            using var reader = new System.Diagnostics.Eventing.Reader.EventLogReader(query);

            System.Diagnostics.Eventing.Reader.EventRecord? record;
            while ((record = reader.ReadEvent()) is not null)
            {
                try
                {
                    string? description = record.FormatDescription();
                    if (description is null)
                    {
                        continue;
                    }

                    bool isMatch = searchTerms.Any(term =>
                        description.Contains(term, StringComparison.OrdinalIgnoreCase));

                    if (isMatch)
                    {
                        var logItem = new EventLogItem
                        {
                            Name = record.ProviderName ?? "Windows Error Reporting",
                            EventId = record.Id,
                            Level = ConvertReaderLevelToEventLogLevel(record.Level),
                            StatusText = $"WER Event - {record.TimeCreated:g}",
                            Details = description,
                            Category = "WER",
                            TimeCreated = record.TimeCreated ?? DateTime.MinValue
                        };

                        System.Windows.Application.Current.Dispatcher.InvokeAsync(() =>
                        {
                            int insertIndex = 0;
                            for (int i = 0; i < EventLogItems.Count; i++)
                            {
                                if (logItem.TimeCreated > EventLogItems[i].TimeCreated)
                                {
                                    insertIndex = i;
                                    break;
                                }

                                insertIndex = i + 1;
                            }

                            EventLogItems.Insert(insertIndex, logItem);
                            EventSearchStatus = $"Found {EventLogItems.Count} events...";
                        });
                    }
                }
                catch
                {
                    // Skip records that can't be read
                }
                finally
                {
                    record.Dispose();
                }
            }
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error reading WER logs: {ex.Message}");
        }
    }

    private static EventLogLevel ConvertToEventLogLevel(System.Diagnostics.EventLogEntryType entryType)
    {
        return entryType switch
        {
            System.Diagnostics.EventLogEntryType.Error => EventLogLevel.Error,
            System.Diagnostics.EventLogEntryType.Warning => EventLogLevel.Warning,
            System.Diagnostics.EventLogEntryType.Information => EventLogLevel.Information,
            System.Diagnostics.EventLogEntryType.SuccessAudit => EventLogLevel.Information,
            System.Diagnostics.EventLogEntryType.FailureAudit => EventLogLevel.Warning,
            _ => EventLogLevel.Information
        };
    }

    private static EventLogLevel ConvertReaderLevelToEventLogLevel(byte? level)
    {
        return level switch
        {
            1 => EventLogLevel.Critical,
            2 => EventLogLevel.Error,
            3 => EventLogLevel.Warning,
            4 => EventLogLevel.Information,
            5 => EventLogLevel.Verbose,
            _ => EventLogLevel.Information
        };
    }

    [RelayCommand]
    private async Task CheckSystemAsync()
    {
        try
        {
            StatusMessage = "Checking system diagnostics...";
            SystemStatusItems.Clear();

            await CheckWindowsDefenderAsync();
            await CheckPowerSettingsAsync();
            await CheckMemoryAndDiskAsync();
            await CheckPCIeDevicesAsync();

            StatusMessage = "System diagnostics complete";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error: {ex.Message}";
        }
    }

    private async Task CheckWindowsDefenderAsync()
    {
        var items = new List<SystemStatusItem>();

        await Task.Run(() =>
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    Arguments = @"-ExecutionPolicy Bypass -Command ""
                        $defender = Get-MpComputerStatus -ErrorAction SilentlyContinue;
                        if ($defender) {
                            Write-Output ($defender.RealTimeProtectionEnabled);
                            Write-Output ($defender.AntivirusEnabled);
                            Write-Output ($defender.BehaviorMonitorEnabled);
                            Write-Output ($defender.IoavProtectionEnabled);
                            if ($defender.QuickScanStartTime) {
                                Write-Output ($defender.QuickScanStartTime);
                            } else {
                                Write-Output 'Never';
                            }
                            if ($defender.FullScanStartTime) {
                                Write-Output ($defender.FullScanStartTime);
                            } else {
                                Write-Output 'Never';
                            }
                        } else {
                            Write-Output 'N/A';Write-Output 'N/A';Write-Output 'N/A';Write-Output 'N/A';Write-Output 'N/A';Write-Output 'N/A';
                        }

                        # Exploit Protection
                        $expProtect = Get-ProcessMitigation -System -ErrorAction SilentlyContinue;
                        if ($expProtect) {
                            Write-Output ($expProtect.DEP.Enable);
                            Write-Output ($expProtect.ASLR.Enable);
                            Write-Output ($expProtect.CFG.Enable);
                        } else {
                            Write-Output 'N/A';Write-Output 'N/A';Write-Output 'N/A';
                        }
                    """,
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(psi);
                if (process is not null)
                {
                    string result = process.StandardOutput.ReadToEnd();
                    process.WaitForExit();

                    var lines = result.Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
                    if (lines.Length >= 9)
                    {
                        // Real-Time Protection
                        bool rtpEnabled = lines[0].Equals("True", StringComparison.OrdinalIgnoreCase);
                        items.Add(new SystemStatusItem
                        {
                            Name = "Real-Time Protection",
                            Category = "Security",
                            Status = rtpEnabled ? SystemStatus.Good : SystemStatus.Error,
                            StatusText = rtpEnabled ? "Enabled" : "Disabled",
                            Details = "Windows Defender real-time protection monitors your system for malware and threats."
                        });

                        // Antivirus
                        bool avEnabled = lines[1].Equals("True", StringComparison.OrdinalIgnoreCase);
                        items.Add(new SystemStatusItem
                        {
                            Name = "Antivirus Engine",
                            Category = "Security",
                            Status = avEnabled ? SystemStatus.Good : SystemStatus.Error,
                            StatusText = avEnabled ? "Active" : "Inactive",
                            Details = "Core antivirus engine for threat detection and removal."
                        });

                        // Behavior Monitor
                        bool behaviorEnabled = lines[2].Equals("True", StringComparison.OrdinalIgnoreCase);
                        items.Add(new SystemStatusItem
                        {
                            Name = "Behavior Monitoring",
                            Category = "Security",
                            Status = behaviorEnabled ? SystemStatus.Good : SystemStatus.Warning,
                            StatusText = behaviorEnabled ? "Active" : "Inactive",
                            Details = "Monitors application behavior for suspicious activity."
                        });

                        // IOAV Protection
                        bool ioavEnabled = lines[3].Equals("True", StringComparison.OrdinalIgnoreCase);
                        items.Add(new SystemStatusItem
                        {
                            Name = "IOAV Protection",
                            Category = "Security",
                            Status = ioavEnabled ? SystemStatus.Good : SystemStatus.Warning,
                            StatusText = ioavEnabled ? "Active" : "Inactive",
                            Details = "IE Downloads and Outlook Express Attachments scanning."
                        });

                        // Last Scan
                        string lastQuickScan = lines[4];
                        string lastFullScan = lines[5];
                        items.Add(new SystemStatusItem
                        {
                            Name = "Recent Scans",
                            Category = "Security",
                            Status = SystemStatus.Info,
                            StatusText = lastQuickScan != "Never" ? $"Quick: {lastQuickScan}" : "No recent scan",
                            Details = $"Quick Scan: {lastQuickScan}\nFull Scan: {lastFullScan}"
                        });

                        // DEP
                        bool depEnabled = lines[6].Contains("ON", StringComparison.OrdinalIgnoreCase);
                        items.Add(new SystemStatusItem
                        {
                            Name = "Data Execution Prevention",
                            Category = "Security",
                            Status = depEnabled ? SystemStatus.Good : SystemStatus.Warning,
                            StatusText = depEnabled ? "Enabled" : "Disabled",
                            Details = "Prevents code execution from data-only memory pages."
                        });

                        // ASLR
                        bool aslrEnabled = lines[7].Contains("ON", StringComparison.OrdinalIgnoreCase);
                        items.Add(new SystemStatusItem
                        {
                            Name = "ASLR",
                            Category = "Security",
                            Status = aslrEnabled ? SystemStatus.Good : SystemStatus.Warning,
                            StatusText = aslrEnabled ? "Enabled" : "Disabled",
                            Details = "Address Space Layout Randomization makes exploitation harder."
                        });

                        // CFG
                        bool cfgEnabled = lines[8].Contains("ON", StringComparison.OrdinalIgnoreCase);
                        items.Add(new SystemStatusItem
                        {
                            Name = "Control Flow Guard",
                            Category = "Security",
                            Status = cfgEnabled ? SystemStatus.Good : SystemStatus.Warning,
                            StatusText = cfgEnabled ? "Enabled" : "Disabled",
                            Details = "Protects against memory corruption vulnerabilities."
                        });
                    }
                }
            }
            catch (Exception ex)
            {
                items.Add(new SystemStatusItem
                {
                    Name = "Windows Defender",
                    Category = "Security",
                    Status = SystemStatus.Unknown,
                    StatusText = "Error",
                    Details = $"Failed to query: {ex.Message}"
                });
            }
        });

        // Add to observable collection on UI thread
        foreach (var item in items)
        {
            SystemStatusItems.Add(item);
        }
    }

    private async Task CheckPowerSettingsAsync()
    {
        var items = new List<SystemStatusItem>();

        await Task.Run(() =>
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    Arguments = @"-ExecutionPolicy Bypass -Command ""
                        $activePlan = powercfg /getactivescheme;
                        if ($activePlan -match '\(([^)]+)\)') {
                            Write-Output $matches[1];
                        } else {
                            Write-Output 'Unknown';
                        }

                        $minProc = powercfg /query SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMIN | Select-String 'Current AC Power Setting Index:';
                        $maxProc = powercfg /query SCHEME_CURRENT SUB_PROCESSOR PROCTHROTTLEMAX | Select-String 'Current AC Power Setting Index:';

                        if ($minProc) {
                            $minVal = ($minProc -replace '.+: 0x([0-9a-f]+)', '$1');
                            Write-Output ([Convert]::ToInt32($minVal, 16));
                        } else { Write-Output '0'; }

                        if ($maxProc) {
                            $maxVal = ($maxProc -replace '.+: 0x([0-9a-f]+)', '$1');
                            Write-Output ([Convert]::ToInt32($maxVal, 16));
                        } else { Write-Output '100'; }

                        $turbo = powercfg /query SCHEME_CURRENT SUB_PROCESSOR PERFBOOSTMODE | Select-String 'Current AC Power Setting Index:';
                        if ($turbo) {
                            $turboVal = ($turbo -replace '.+: 0x([0-9a-f]+)', '$1');
                            Write-Output ([Convert]::ToInt32($turboVal, 16));
                        } else { Write-Output '0'; }
                    """,
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(psi);
                if (process is not null)
                {
                    string result = process.StandardOutput.ReadToEnd();
                    process.WaitForExit();

                    var lines = result.Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
                    if (lines.Length >= 4)
                    {
                        string planName = lines[0];
                        int minState = int.Parse(lines[1]);
                        int maxState = int.Parse(lines[2]);
                        int turboMode = int.Parse(lines[3]);

                        // Power Plan
                        bool isHighPerformance = planName.Contains("High performance", StringComparison.OrdinalIgnoreCase) ||
                                                 planName.Contains("Ultimate", StringComparison.OrdinalIgnoreCase);
                        items.Add(new SystemStatusItem
                        {
                            Name = "Power Plan",
                            Category = "Performance",
                            Status = isHighPerformance ? SystemStatus.Good : SystemStatus.Warning,
                            StatusText = planName,
                            Details = isHighPerformance ? "Optimized for maximum performance" : "Consider High Performance plan for production systems"
                        });

                        // CPU State
                        bool isMaxPerformance = minState >= 100 && maxState >= 100;
                        items.Add(new SystemStatusItem
                        {
                            Name = "CPU Power State",
                            Category = "Performance",
                            Status = isMaxPerformance ? SystemStatus.Good : SystemStatus.Warning,
                            StatusText = $"{minState}% - {maxState}%",
                            Details = $"Minimum: {minState}%\nMaximum: {maxState}%"
                        });

                        // Turbo Boost
                        bool turboEnabled = turboMode > 0;
                        items.Add(new SystemStatusItem
                        {
                            Name = "Turbo Boost",
                            Category = "Performance",
                            Status = turboEnabled ? SystemStatus.Good : SystemStatus.Info,
                            StatusText = turboEnabled ? $"Enabled (Mode {turboMode})" : "Disabled",
                            Details = turboEnabled ? "CPU can exceed base frequency" : "CPU limited to base frequency"
                        });
                    }
                }
            }
            catch (Exception ex)
            {
                items.Add(new SystemStatusItem
                {
                    Name = "Power Settings",
                    Category = "Performance",
                    Status = SystemStatus.Unknown,
                    StatusText = "Error",
                    Details = $"Failed to query: {ex.Message}"
                });
            }
        });

        // Add to observable collection on UI thread
        foreach (var item in items)
        {
            SystemStatusItems.Add(item);
        }
    }

    private async Task CheckMemoryAndDiskAsync()
    {
        var items = new List<SystemStatusItem>();

        await Task.Run(() =>
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    Arguments = @"-ExecutionPolicy Bypass -Command ""
                        $os = Get-CimInstance Win32_OperatingSystem;
                        $totalMemGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2);
                        $freeMemGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2);
                        $usedMemGB = [math]::Round($totalMemGB - $freeMemGB, 2);
                        $memPercent = [math]::Round(($usedMemGB / $totalMemGB) * 100, 1);

                        Write-Output $totalMemGB;
                        Write-Output $usedMemGB;
                        Write-Output $freeMemGB;
                        Write-Output $memPercent;

                        $pageFile = Get-CimInstance Win32_PageFileUsage -ErrorAction SilentlyContinue;
                        if ($pageFile) {
                            Write-Output $pageFile.Name;
                            Write-Output $pageFile.AllocatedBaseSize;
                            Write-Output $pageFile.CurrentUsage;
                        } else {
                            Write-Output 'N/A';Write-Output '0';Write-Output '0';
                        }

                        $disks = Get-PhysicalDisk -ErrorAction SilentlyContinue;
                        if ($disks) {
                            foreach ($disk in $disks) {
                                Write-Output $disk.FriendlyName;
                                Write-Output $disk.MediaType;
                                Write-Output $disk.HealthStatus;
                                Write-Output $disk.BusType;
                                if ($disk.Size) {
                                    $sizeGB = [math]::Round($disk.Size / 1GB, 2);
                                    Write-Output $sizeGB;
                                } else {
                                    Write-Output '0';
                                }
                                Write-Output '---';
                            }
                        }
                    """,
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(psi);
                if (process is not null)
                {
                    string result = process.StandardOutput.ReadToEnd();
                    process.WaitForExit();

                    var lines = result.Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
                    if (lines.Length >= 7)
                    {
                        double totalMem = double.Parse(lines[0]);
                        double usedMem = double.Parse(lines[1]);
                        double freeMem = double.Parse(lines[2]);
                        double memPercent = double.Parse(lines[3]);

                        // Memory Status
                        SystemStatus memStatus = memPercent < 80 ? SystemStatus.Good :
                                                memPercent < 90 ? SystemStatus.Warning : SystemStatus.Error;
                        items.Add(new SystemStatusItem
                        {
                            Name = "Memory Usage",
                            Category = "Hardware",
                            Status = memStatus,
                            StatusText = $"{memPercent:F1}% ({usedMem:F1} GB / {totalMem:F1} GB)",
                            Details = $"Total: {totalMem:F1} GB\nUsed: {usedMem:F1} GB\nFree: {freeMem:F1} GB"
                        });

                        // Page File
                        string pageFileName = lines[4];
                        int pageFileAllocated = int.Parse(lines[5]);
                        int pageFileUsage = int.Parse(lines[6]);

                        if (pageFileName != "N/A")
                        {
                            double pagePercent = pageFileAllocated > 0 ? (pageFileUsage / (double)pageFileAllocated) * 100 : 0;
                            SystemStatus pageStatus = pagePercent < 50 ? SystemStatus.Good :
                                                     pagePercent < 75 ? SystemStatus.Warning : SystemStatus.Error;
                            items.Add(new SystemStatusItem
                            {
                                Name = "Page File",
                                Category = "Hardware",
                                Status = pageStatus,
                                StatusText = $"{pageFileUsage} MB / {pageFileAllocated} MB",
                                Details = $"Location: {pageFileName}\nAllocated: {pageFileAllocated} MB\nUsage: {pageFileUsage} MB ({pagePercent:F1}%)"
                            });
                        }

                        // Physical Disks
                        int diskIndex = 7;
                        while (diskIndex + 5 < lines.Length)
                        {
                            string diskName = lines[diskIndex];
                            string mediaType = lines[diskIndex + 1];
                            string healthStatus = lines[diskIndex + 2];
                            string busType = lines[diskIndex + 3];
                            string sizeGB = lines[diskIndex + 4];

                            SystemStatus diskStatus = healthStatus.Equals("Healthy", StringComparison.OrdinalIgnoreCase) ? SystemStatus.Good :
                                                     healthStatus.Equals("Warning", StringComparison.OrdinalIgnoreCase) ? SystemStatus.Warning : SystemStatus.Error;

                            bool isSSD = mediaType.Contains("SSD", StringComparison.OrdinalIgnoreCase);
                            items.Add(new SystemStatusItem
                            {
                                Name = diskName,
                                Category = "Hardware",
                                Status = diskStatus,
                                StatusText = $"{healthStatus} - {mediaType}",
                                Details = $"Media: {mediaType}\nHealth: {healthStatus}\nBus: {busType}\nSize: {sizeGB} GB" +
                                         (isSSD ? "\n✓ SSD - Fast storage" : "")
                            });

                            diskIndex += 6; // Skip to next disk (including '---' separator)
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                items.Add(new SystemStatusItem
                {
                    Name = "Memory & Disk",
                    Category = "Hardware",
                    Status = SystemStatus.Unknown,
                    StatusText = "Error",
                    Details = $"Failed to query: {ex.Message}"
                });
            }
        });

        // Add to observable collection on UI thread
        foreach (var item in items)
        {
            SystemStatusItems.Add(item);
        }
    }

    private async Task CheckPCIeDevicesAsync()
    {
        var items = new List<SystemStatusItem>();

        await Task.Run(() =>
        {
            try
            {
                var psi = new ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    Arguments = @"-ExecutionPolicy Bypass -Command ""
                        $problemDevices = Get-PnpDevice -Class 'Display','Net','SCSIAdapter' -Status Error,Degraded,Unknown -ErrorAction SilentlyContinue;
                        if ($problemDevices) {
                            foreach ($dev in $problemDevices) {
                                Write-Output $dev.FriendlyName;
                                Write-Output $dev.Class;
                                Write-Output $dev.Status;
                                Write-Output $dev.Problem;
                                Write-Output '---';
                            }
                        } else {
                            Write-Output 'OK';
                        }

                        Write-Output '===';

                        $tpm = Get-Tpm -ErrorAction SilentlyContinue;
                        if ($tpm) {
                            Write-Output $tpm.TpmPresent;
                            Write-Output $tpm.TpmReady;
                            Write-Output $tpm.TpmEnabled;
                            Write-Output $tpm.TpmActivated;
                        } else {
                            Write-Output 'N/A';Write-Output 'N/A';Write-Output 'N/A';Write-Output 'N/A';
                        }
                    """,
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                };

                using var process = Process.Start(psi);
                if (process is not null)
                {
                    string result = process.StandardOutput.ReadToEnd();
                    process.WaitForExit();

                    var sections = result.Split("===", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

                    // Process device problems
                    if (sections.Length > 0)
                    {
                        var deviceLines = sections[0].Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

                        if (deviceLines.Length > 0 && deviceLines[0] == "OK")
                        {
                            items.Add(new SystemStatusItem
                            {
                                Name = "PCIe Devices",
                                Category = "Hardware",
                                Status = SystemStatus.Good,
                                StatusText = "All devices OK",
                                Details = "No problem devices detected in Display, Network, or Storage controllers"
                            });
                        }
                        else
                        {
                            int deviceIndex = 0;
                            while (deviceIndex + 3 < deviceLines.Length)
                            {
                                string deviceName = deviceLines[deviceIndex];
                                string deviceClass = deviceLines[deviceIndex + 1];
                                string deviceStatus = deviceLines[deviceIndex + 2];
                                string deviceProblem = deviceLines[deviceIndex + 3];

                                SystemStatus status = deviceStatus.Equals("Error", StringComparison.OrdinalIgnoreCase) ? SystemStatus.Error :
                                                     deviceStatus.Equals("Degraded", StringComparison.OrdinalIgnoreCase) ? SystemStatus.Warning : SystemStatus.Unknown;

                                items.Add(new SystemStatusItem
                                {
                                    Name = deviceName,
                                    Category = "Hardware",
                                    Status = status,
                                    StatusText = deviceStatus,
                                    Details = $"Class: {deviceClass}\nStatus: {deviceStatus}\nProblem: {deviceProblem}"
                                });

                                deviceIndex += 5; // Skip to next device (including '---')
                            }
                        }
                    }

                    // Process TPM
                    if (sections.Length > 1)
                    {
                        var tpmLines = sections[1].Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

                        if (tpmLines.Length >= 4)
                        {
                            bool tpmPresent = tpmLines[0].Equals("True", StringComparison.OrdinalIgnoreCase);
                            bool tpmReady = tpmLines[1].Equals("True", StringComparison.OrdinalIgnoreCase);
                            bool tpmEnabled = tpmLines[2].Equals("True", StringComparison.OrdinalIgnoreCase);
                            bool tpmActivated = tpmLines[3].Equals("True", StringComparison.OrdinalIgnoreCase);

                            if (tpmLines[0] != "N/A")
                            {
                                SystemStatus tpmStatus = tpmPresent && tpmReady && tpmEnabled && tpmActivated ? SystemStatus.Good :
                                                        tpmPresent ? SystemStatus.Warning : SystemStatus.Info;

                                string tpmStatusText = tpmPresent && tpmReady ? "Ready" :
                                                      tpmPresent ? "Not Ready" : "Not Present";

                                items.Add(new SystemStatusItem
                                {
                                    Name = "TPM (Trusted Platform Module)",
                                    Category = "Security",
                                    Status = tpmStatus,
                                    StatusText = tpmStatusText,
                                    Details = $"Present: {tpmPresent}\nReady: {tpmReady}\nEnabled: {tpmEnabled}\nActivated: {tpmActivated}"
                                });
                            }
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                items.Add(new SystemStatusItem
                {
                    Name = "PCIe & Hardware",
                    Category = "Hardware",
                    Status = SystemStatus.Unknown,
                    StatusText = "Error",
                    Details = $"Failed to query: {ex.Message}"
                });
            }
        });

        // Add to observable collection on UI thread
        foreach (var item in items)
        {
            SystemStatusItems.Add(item);
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
            if (dir[sourceDir.Length..].StartsWith("\\lib"))
            {
                continue;
            }

            string relativePath = Path.GetRelativePath(sourceDir, dir);
            string newDir = Path.Combine(targetDir, relativePath);
            Directory.CreateDirectory(newDir);
        }
    }

    private static bool CopyFilesByPattern(string sourceDir, string targetDir, string pattern)
    {
        bool anyFilesCopied = false;
        foreach (string file in Directory.GetFiles(sourceDir, pattern, SearchOption.AllDirectories))
        {
            string relativePath = Path.GetRelativePath(sourceDir, file);
            string targetFile = Path.Combine(targetDir, relativePath);

            string? targetFileDir = Path.GetDirectoryName(targetFile);
            if (targetFileDir?[sourceDir.Length..].StartsWith("\\lib") == true)
            {
                continue;
            }

            if (targetFileDir is not null && !Directory.Exists(targetFileDir))
            {
                Directory.CreateDirectory(targetFileDir);
            }

            File.Copy(file, targetFile, true);
            anyFilesCopied = true;
        }

        return anyFilesCopied;
    }

    private static Task<bool> CopyFilesByPatternAsync(string sourceDir, string targetDir, string pattern)
    {
        return Task.Run(() => CopyFilesByPattern(sourceDir, targetDir, pattern));
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

    private static Task CopyDirectoryRecursiveAsync(string sourceDir, string targetDir)
    {
        return Task.Run(() => CopyDirectoryRecursive(sourceDir, targetDir));
    }

    #endregion
}
