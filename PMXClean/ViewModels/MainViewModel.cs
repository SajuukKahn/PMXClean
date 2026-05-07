namespace PMXClean.ViewModels;

using System.Collections.ObjectModel;
using System.ComponentModel;
using System.Diagnostics;
using System.IO;
using System.Net.NetworkInformation;
using System.Reflection;
using System.Runtime.Loader;
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
        public ObservableCollection<ProcessInfo> RunningProcesses { get; } = [];
        public ObservableCollection<SerialPortInfo> SerialPorts { get; } = [];

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

    /// <summary>
    /// Loads available versions - now extracts from target installation DLLs instead of embedded resources.
    /// </summary>
    private void LoadAvailableVersions()
    {
        AvailableVersions.Clear();

        // No longer using embedded resources - versions are extracted from installation DLLs
        // Add a single "Installed" version entry
        AvailableVersions.Add("Installed");
        SelectedVersion = "Installed";

        StatusMessage = "Ready to compare against installed version";
    }

    private void UpdateVersionInfo()
    {
        if (string.IsNullOrEmpty(SelectedVersion) || SelectedInstallation is null)
        {
            VersionInfoText = string.Empty;
            return;
        }

        // Count Python files that would be extracted from DLLs
        try
        {
            int pythonFileCount = CountPythonFilesInDlls(SelectedInstallation.Path);
            VersionInfoText = $"{pythonFileCount} Python files in DLLs";
        }
        catch (Exception ex)
        {
            VersionInfoText = $"Error counting files: {ex.Message}";
        }
    }

    /// <summary>
    /// Counts Python files embedded in DLLs within the installation path (subfolders only).
    /// </summary>
    private static int CountPythonFilesInDlls(string installationPath)
    {
        int count = 0;

        try
        {
            // Get all DLL files from subfolders (excluding root)
            var dllFiles = Directory.GetFiles(installationPath, "*.dll", SearchOption.AllDirectories)
                .Where(dll => !Path.GetDirectoryName(dll)!.Equals(installationPath, StringComparison.OrdinalIgnoreCase));

            foreach (var dllPath in dllFiles)
            {
                try
                {
                    var assembly = Assembly.LoadFrom(dllPath);
                    var resourceNames = assembly.GetManifestResourceNames();
                    count += resourceNames.Count(name => name.EndsWith(".py", StringComparison.OrdinalIgnoreCase));
                }
                catch
                {
                    // Skip DLLs that can't be loaded
                }
            }
        }
        catch
        {
            // Return 0 if there's an error
        }

        return count;
    }

    /// <summary>
    /// Sets up the comparison paths when version or installation changes.
    /// Extracts Python files from DLLs in the installation to a temp directory and configures the ComparisonViewModel.
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
            int extractedCount = ExtractPythonFilesFromDlls(SelectedInstallation.Path, sourceDir);

            if (extractedCount == 0)
            {
                StatusMessage = $"No Python files found in DLLs";
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

            StatusMessage = $"Extracted {extractedCount} Python files from DLLs for comparison";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error setting up comparison: {ex.Message}";
        }
    }

    /// <summary>
    /// Extracts Python files from all DLLs in the installation path (subfolders only) to a target directory.
    /// Returns the count of extracted files.
    /// The extracted files are placed relative to the DLL's location, not based on the resource namespace.
    /// </summary>
    private static int ExtractPythonFilesFromDlls(string installationPath, string targetDir)
    {
        int extractedCount = 0;

        try
        {
            // Get all DLL files from subfolders (excluding root)
            var dllFiles = Directory.GetFiles(installationPath, "*.dll", SearchOption.AllDirectories)
                .Where(dll => !Path.GetDirectoryName(dll)!.Equals(installationPath, StringComparison.OrdinalIgnoreCase))
                .ToList();

            foreach (var dllPath in dllFiles)
            {
                try
                {
                    // Load assembly in isolated context to allow unloading
                    var loadContext = new AssemblyLoadContext(name: null, isCollectible: true);
                    try
                    {
                        var assembly = loadContext.LoadFromAssemblyPath(dllPath);
                        var resourceNames = assembly.GetManifestResourceNames();
                        var pythonResources = resourceNames.Where(name => name.EndsWith(".py", StringComparison.OrdinalIgnoreCase));

                        // Get the DLL's directory relative to installation path
                        string dllDirectory = Path.GetDirectoryName(dllPath)!;
                        string relativeDllPath = Path.GetRelativePath(installationPath, dllDirectory);

                        foreach (var resourceName in pythonResources)
                    {
                        try
                        {
                            using var stream = assembly.GetManifestResourceStream(resourceName);
                            if (stream is not null)
                            {
                                // Extract folder structure and filename from the resource name
                                // Resource: "PVA.PathMasterX.Base.Core.Safety.Button.Configuration.py"
                                //   → "Configuration.py" in DLL folder
                                // Resource: "PVA.PathMasterX.Base.Core.Safety.Button.Functions.Monitor.py"
                                //   → "Functions\Monitor.py" relative to DLL folder

                                // Get the assembly's root namespace by taking the assembly name
                                string assemblyNamespace = assembly.GetName().Name ?? string.Empty;

                                // Split resource name by dots
                                var parts = resourceName.Split('.');

                                if (parts.Length < 2)
                                {
                                    // Unexpected format, skip
                                    continue;
                                }

                                // Last part is "py", second-to-last is the actual filename
                                string pythonFileName = parts[^2] + ".py";

                                // Find where the assembly namespace ends in the resource name
                                // and extract any additional path segments after it
                                string resourcePath = resourceName;
                                if (!string.IsNullOrEmpty(assemblyNamespace) && 
                                    resourcePath.StartsWith(assemblyNamespace + ".", StringComparison.OrdinalIgnoreCase))
                                {
                                    // Remove assembly namespace prefix
                                    resourcePath = resourcePath.Substring(assemblyNamespace.Length + 1);
                                }

                                // Split what remains and extract folder structure
                                // Example: "Functions.Monitor.py" → ["Functions", "Monitor", "py"]
                                var pathParts = resourcePath.Split('.');

                                // Build the subfolder path (everything except the last 2 parts which are filename.py)
                                string subfolderPath = string.Empty;
                                if (pathParts.Length > 2)
                                {
                                    var folderParts = pathParts.Take(pathParts.Length - 2);
                                    subfolderPath = Path.Combine(folderParts.ToArray());
                                }

                                // Build final output path
                                string outputPath = string.IsNullOrEmpty(subfolderPath)
                                    ? Path.Combine(targetDir, relativeDllPath, pythonFileName)
                                    : Path.Combine(targetDir, relativeDllPath, subfolderPath, pythonFileName);

                                // Create subdirectories if needed
                                string? outputDir = Path.GetDirectoryName(outputPath);
                                if (outputDir is not null && !Directory.Exists(outputDir))
                                {
                                    Directory.CreateDirectory(outputDir);
                                }

                                // Write to file
                                using var fileStream = File.Create(outputPath);
                                stream.CopyTo(fileStream);

                                extractedCount++;
                                Debug.WriteLine($"Extracted: {resourceName} → {Path.GetRelativePath(targetDir, outputPath)}");
                            }
                        }
                        catch (Exception ex)
                        {
                            Debug.WriteLine($"Error extracting {resourceName} from {Path.GetFileName(dllPath)}: {ex.Message}");
                        }
                    }
                    }
                    finally
                    {
                        // Unload the assembly to prevent locking
                        loadContext.Unload();
                    }
                }
                catch (Exception ex)
                {
                    Debug.WriteLine($"Error loading DLL {Path.GetFileName(dllPath)}: {ex.Message}");
                }
            }
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error extracting Python files from DLLs: {ex.Message}");
        }

        return extractedCount;
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

        // Since we now only have "Installed" version, just set it and report version info
        try
        {
            SelectedVersion = "Installed";

            string? fileVersion = null;

            // Get version from executable or backup
            if (!SelectedInstallation.IsBackup)
            {
                string exePath = Path.Combine(SelectedInstallation.Path, "PVA.PathMasterX.exe");
                if (File.Exists(exePath))
                {
                    var versionInfo = FileVersionInfo.GetVersionInfo(exePath);
                    fileVersion = versionInfo.FileVersion;
                }
            }
            else
            {
                fileVersion = SelectedInstallation.BackupInfo?.BackupVersion;
            }

            if (!string.IsNullOrEmpty(fileVersion))
            {
                StatusMessage = $"Using installed version: {fileVersion}";
            }
            else
            {
                StatusMessage = "Using installed version (version info unavailable)";
            }
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error setting version: {ex.Message}";
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
    /// Compares the selected locked file against the version extracted from DLLs.
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
            StatusMessage = $"Comparing {SelectedLockedFile.Name} against DLL-embedded version...";

            // Get the relative path of the file from the installation root
            string relativePath = SelectedLockedFile.RelativePath;

            // Extract the file from DLLs for comparison
            string? versionFilePath = ExtractPythonFileFromDllsForComparison(
                SelectedInstallation.Path, 
                relativePath, 
                version);

            // Perform the comparison
            LockedFileComparisonResult = FileComparisonService.CompareFiles(
                versionFilePath,
                SelectedLockedFile.FullPath,
                relativePath);

            LockedFileComparisonVersion = version;
            OnPropertyChanged(nameof(IsLockedFileComparisonActive));

            string statusDesc = LockedFileComparisonResult.Status switch
            {
                FileComparisonStatus.Same => "Files are identical",
                FileComparisonStatus.Different => $"Files differ ({LockedFileComparisonResult.AddedLines} added, {LockedFileComparisonResult.RemovedLines} removed)",
                FileComparisonStatus.LeftOnly => "File only exists in DLL (not in filesystem)",
                FileComparisonStatus.RightOnly => "File only exists in filesystem (not in DLL)",
                _ => "Comparison complete"
            };

            StatusMessage = $"Compared {SelectedLockedFile.Name} vs DLL version: {statusDesc}";
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
    /// Extracts a specific Python file from DLLs to a temporary location for comparison.
    /// This searches all DLLs for the matching Python file based on relative path.
    /// </summary>
    private static string? ExtractPythonFileFromDllsForComparison(string installationPath, string relativePath, string version)
    {
        try
        {
            // Get filename and subfolder structure from relative path
            // Example: "Base\Core\Drivers\Safety\Button\Functions\Monitor.py"
            //   → fileName: "Monitor.py"
            //   → directory: "Base\Core\Drivers\Safety\Button"
            //   → subfolder: "Functions"
            string fileName = Path.GetFileName(relativePath);
            string? directory = Path.GetDirectoryName(relativePath);

            // Get all DLL files from subfolders (excluding root)
            var dllFiles = Directory.GetFiles(installationPath, "*.dll", SearchOption.AllDirectories)
                .Where(dll => !Path.GetDirectoryName(dll)!.Equals(installationPath, StringComparison.OrdinalIgnoreCase))
                .ToList();

            foreach (var dllPath in dllFiles)
            {
                try
                {
                    // Check if DLL is in a compatible directory
                    string dllDirectory = Path.GetDirectoryName(dllPath)!;
                    string relativeDllPath = Path.GetRelativePath(installationPath, dllDirectory);

                    // The Python file's directory should start with the DLL's directory
                    // Example: Python in "Base\Core\Drivers\Safety\Button\Functions"
                    //          DLL in "Base\Core\Drivers\Safety\Button"
                    if (directory is not null && !directory.StartsWith(relativeDllPath, StringComparison.OrdinalIgnoreCase))
                    {
                        continue;
                    }

                    // Load assembly in isolated context to allow unloading
                    var loadContext = new AssemblyLoadContext(name: null, isCollectible: true);
                    try
                    {
                        var assembly = loadContext.LoadFromAssemblyPath(dllPath);
                        var resourceNames = assembly.GetManifestResourceNames();
                        string assemblyNamespace = assembly.GetName().Name ?? string.Empty;

                    // Find matching resource by reconstructing the expected resource name
                    string? matchingResource = resourceNames.FirstOrDefault(resName =>
                    {
                        if (!resName.EndsWith(".py", StringComparison.OrdinalIgnoreCase))
                            return false;

                        // Extract filename from resource
                        var parts = resName.Split('.');
                        if (parts.Length < 2)
                            return false;

                        string resourceFileName = parts[^2] + ".py";
                        if (!resourceFileName.Equals(fileName, StringComparison.OrdinalIgnoreCase))
                            return false;

                        // Extract subfolder structure from resource
                        string resourcePath = resName;
                        if (!string.IsNullOrEmpty(assemblyNamespace) && 
                            resourcePath.StartsWith(assemblyNamespace + ".", StringComparison.OrdinalIgnoreCase))
                        {
                            resourcePath = resourcePath.Substring(assemblyNamespace.Length + 1);
                        }

                        var pathParts = resourcePath.Split('.');
                        string resourceSubfolder = string.Empty;
                        if (pathParts.Length > 2)
                        {
                            var folderParts = pathParts.Take(pathParts.Length - 2);
                            resourceSubfolder = Path.Combine(folderParts.ToArray());
                        }

                        // Compare the subfolder structure
                        // Example: relativePath = "Base\Core\Drivers\Safety\Button\Functions\Monitor.py"
                        //          relativeDllPath = "Base\Core\Drivers\Safety\Button"
                        //          expectedSubfolder = "Functions"
                        if (directory is not null && directory.Length > relativeDllPath.Length)
                        {
                            string expectedSubfolder = directory.Substring(relativeDllPath.Length).TrimStart('\\', '/');
                            return resourceSubfolder.Equals(expectedSubfolder, StringComparison.OrdinalIgnoreCase);
                        }
                        else
                        {
                            // File is directly in the DLL's folder (no subfolder)
                            return string.IsNullOrEmpty(resourceSubfolder);
                        }
                    });

                    if (matchingResource is not null)
                    {
                        // Extract to temp location maintaining the relative path
                        string tempDir = Path.Combine(Path.GetTempPath(), "PMXClean_Compare", "locked_file_compare", version);
                        string tempFilePath = Path.Combine(tempDir, relativePath);

                        string? tempFileDir = Path.GetDirectoryName(tempFilePath);
                        if (tempFileDir is not null && !Directory.Exists(tempFileDir))
                        {
                            Directory.CreateDirectory(tempFileDir);
                        }

                        using var stream = assembly.GetManifestResourceStream(matchingResource);
                        if (stream is not null)
                        {
                            using var fileStream = File.Create(tempFilePath);
                            stream.CopyTo(fileStream);
                            Debug.WriteLine($"Extracted for comparison: {relativePath} from {Path.GetFileName(dllPath)}");
                            return tempFilePath;
                        }
                    }
                    }
                    finally
                    {
                        // Unload the assembly to prevent locking
                        loadContext.Unload();
                    }
                }
                catch (Exception ex)
                {
                    Debug.WriteLine($"Error searching DLL {Path.GetFileName(dllPath)}: {ex.Message}");
                }
            }

            // File not found in any DLL
            Debug.WriteLine($"Python file not found in any DLL: {relativePath}");
            return null;
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error extracting Python file for comparison: {ex.Message}");
            return null;
        }
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
            await CheckSerialPortsInfoAsync();

            StatusMessage = "System diagnostics complete";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error: {ex.Message}";
        }
    }

    /// <summary>
    /// Adds serial port summary to system status items (called as part of CheckSystemAsync).
    /// </summary>
    private async Task CheckSerialPortsInfoAsync()
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
                        $ports = Get-PnpDevice -PresentOnly -Class 'Ports' -ErrorAction SilentlyContinue;
                        if ($ports) {
                            $okCount = ($ports | Where-Object { $_.Status -eq 'OK' }).Count;
                            $errorCount = ($ports | Where-Object { $_.Status -ne 'OK' }).Count;
                            $total = $ports.Count;
                            Write-Output ('{0}|{1}|{2}' -f $total, $okCount, $errorCount);
                            foreach ($port in $ports) {
                                Write-Output ('PORT|{0}|{1}' -f $port.FriendlyName, $port.Status);
                            }
                        } else {
                            Write-Output '0|0|0';
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
                    if (lines.Length > 0)
                    {
                        var summaryParts = lines[0].Split('|');
                        if (summaryParts.Length >= 3)
                        {
                            int total = int.Parse(summaryParts[0]);
                            int okCount = int.Parse(summaryParts[1]);
                            int errorCount = int.Parse(summaryParts[2]);

                            var detailsBuilder = new StringBuilder();
                            foreach (var line in lines.Skip(1).Where(l => l.StartsWith("PORT|")))
                            {
                                var parts = line.Split('|');
                                if (parts.Length >= 3)
                                {
                                    string statusIcon = parts[2].Equals("OK", StringComparison.OrdinalIgnoreCase) ? "✓" : "✗";
                                    detailsBuilder.AppendLine($"{statusIcon} {parts[1]} ({parts[2]})");
                                }
                            }

                            SystemStatus status = errorCount > 0 ? SystemStatus.Warning :
                                                 total > 0 ? SystemStatus.Good : SystemStatus.Info;

                            items.Add(new SystemStatusItem
                            {
                                Name = "Serial Ports (COM)",
                                Category = "Hardware",
                                Status = status,
                                StatusText = total > 0 ? $"{total} port(s), {okCount} OK" : "No ports found",
                                Details = detailsBuilder.Length > 0 ? detailsBuilder.ToString().TrimEnd() : "No serial ports detected"
                            });
                        }
                    }
                }
            }
            catch (Exception ex)
            {
                items.Add(new SystemStatusItem
                {
                    Name = "Serial Ports",
                    Category = "Hardware",
                    Status = SystemStatus.Unknown,
                    StatusText = "Error",
                    Details = $"Failed to query: {ex.Message}"
                });
            }
        });

        foreach (var item in items)
        {
            SystemStatusItems.Add(item);
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

                        Write-Output '===MEMORY===';

                        $memory = Get-CimInstance Win32_PhysicalMemory;
                        foreach ($stick in $memory) {
                            $capGB = [math]::Round($stick.Capacity / 1GB, 0);
                            $memType = $stick.SMBIOSMemoryType;
                            $speed = $stick.Speed;
                            $locator = $stick.DeviceLocator;
                            Write-Output ('{0}|{1}|{2}|{3}' -f $locator, $capGB, $memType, $speed);
                        }

                        Write-Output '===DISKS===';

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

                    var sections = result.Split("===", StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);

                    // First section: basic memory info
                    if (sections.Length > 0)
                    {
                        var lines = sections[0].Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries);
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
                        }
                    }

                    // Memory modules section
                    var memorySection = sections.FirstOrDefault(s => s.StartsWith("MEMORY"));
                    if (memorySection is not null)
                    {
                        var memLines = memorySection.Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                            .Skip(1) // Skip "MEMORY" header
                            .ToArray();

                        var moduleDetails = new StringBuilder();
                        foreach (var line in memLines)
                        {
                            var parts = line.Split('|');
                            if (parts.Length >= 4)
                            {
                                string locator = parts[0];
                                string capGB = parts[1];
                                string memType = GetMemoryTypeName(int.TryParse(parts[2], out int typeCode) ? typeCode : 0);
                                string speed = parts[3];
                                moduleDetails.AppendLine($"{locator}: {capGB} GB {memType} @ {speed}MHz");
                            }
                        }

                        if (moduleDetails.Length > 0)
                        {
                            items.Add(new SystemStatusItem
                            {
                                Name = "Memory Modules",
                                Category = "Hardware",
                                Status = SystemStatus.Info,
                                StatusText = $"{memLines.Length} module(s) installed",
                                Details = moduleDetails.ToString().TrimEnd()
                            });
                        }
                    }

                    // Physical Disks section
                    var diskSection = sections.FirstOrDefault(s => s.StartsWith("DISKS"));
                    if (diskSection is not null)
                    {
                        var diskLines = diskSection.Split('\n', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                            .Skip(1) // Skip "DISKS" header
                            .ToArray();

                        int diskIndex = 0;
                        while (diskIndex + 5 <= diskLines.Length)
                        {
                            string diskName = diskLines[diskIndex];
                            string mediaType = diskLines[diskIndex + 1];
                            string healthStatus = diskLines[diskIndex + 2];
                            string busType = diskLines[diskIndex + 3];
                            string sizeGB = diskLines[diskIndex + 4];

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

    /// <summary>
    /// Converts SMBIOSMemoryType code to human-readable memory type name.
    /// </summary>
    private static string GetMemoryTypeName(int typeCode)
    {
        return typeCode switch
        {
            0 => "Unknown",
            1 => "Other",
            2 => "DRAM",
            3 => "Synchronous DRAM",
            4 => "Cache DRAM",
            5 => "EDO",
            6 => "EDRAM",
            7 => "VRAM",
            8 => "SRAM",
            9 => "ROM",
            10 => "ROM",
            11 => "FLASH",
            12 => "EEPROM",
            13 => "FEPROM",
            14 => "EPROM",
            15 => "CDRAM",
            16 => "3DRAM",
            17 => "SDRAM",
            18 => "SGRAM",
            19 => "RDRAM",
            20 => "DDR",
            21 => "DDR2",
            22 => "DDR2 FB-DIMM",
            24 => "DDR3",
            25 => "FBD2",
            26 => "DDR4",
            27 => "LPDDR",
            28 => "LPDDR2",
            29 => "LPDDR3",
            30 => "LPDDR4",
            31 => "Logical non-volatile device",
            32 => "HBM",
            33 => "HBM2",
            34 => "DDR5",
            35 => "LPDDR5",
            _ => $"Unknown ({typeCode})"
        };
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

    /// <summary>
    /// Checks running processes and populates the RunningProcesses collection.
    /// </summary>
    [RelayCommand]
    private async Task CheckRunningProcessesAsync()
    {
        try
        {
            StatusMessage = "Scanning running processes...";
            RunningProcesses.Clear();

            var processes = new List<ProcessInfo>();

            await Task.Run(() =>
            {
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = "powershell.exe",
                        Arguments = @"-ExecutionPolicy Bypass -Command ""
                            Get-Process | ForEach-Object {
                                $memKB = [math]::Round($_.WS / 1KB, 0);
                                $path = '';
                                try { $path = $_.Path; } catch { }
                                Write-Output ('{0}|{1}|{2}|{3}' -f $_.Id, $_.Name, $memKB, $path);
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
                            var parts = line.Split('|');
                            if (parts.Length >= 4)
                            {
                                if (int.TryParse(parts[0], out int pid) && long.TryParse(parts[2], out long memKB))
                                {
                                    processes.Add(new ProcessInfo
                                    {
                                        ProcessId = pid,
                                        Name = parts[1],
                                        MemoryKB = memKB,
                                        Path = parts[3]
                                    });
                                }
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    Debug.WriteLine($"Error getting processes: {ex.Message}");
                }
            });

            // Sort by memory (highest first) and add to collection
            var sorted = processes.OrderByDescending(p => p.MemoryKB).ToList();
            foreach (var proc in sorted)
            {
                RunningProcesses.Add(proc);
            }

            StatusMessage = $"Found {RunningProcesses.Count} running processes";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error scanning processes: {ex.Message}";
        }
    }

    /// <summary>
    /// Checks serial port devices and populates the SerialPorts collection.
    /// </summary>
    [RelayCommand]
    private async Task CheckSerialPortsAsync()
    {
        try
        {
            StatusMessage = "Scanning serial ports...";
            SerialPorts.Clear();

            var ports = new List<SerialPortInfo>();

            await Task.Run(() =>
            {
                try
                {
                    var psi = new ProcessStartInfo
                    {
                        FileName = "powershell.exe",
                        Arguments = @"-ExecutionPolicy Bypass -Command ""
                            Get-PnpDevice -PresentOnly -Class 'Ports' -ErrorAction SilentlyContinue | ForEach-Object {
                                $name = $_.FriendlyName;
                                $status = $_.Status;
                                $driverFile = '';
                                $driverDate = '';
                                $driverVersion = '';
                                try {
                                    $props = Get-PnpDeviceProperty -InstanceID $_.InstanceId -ErrorAction SilentlyContinue;
                                    $driverFile = ($props | Where-Object { $_.KeyName -eq 'DEVPKEY_Device_DriverInfPath' }).Data;
                                    $dateVal = ($props | Where-Object { $_.KeyName -eq 'DEVPKEY_Device_DriverDate' }).Data;
                                    if ($dateVal) { $driverDate = $dateVal.ToString('yyyy-MM-dd'); }
                                    $driverVersion = ($props | Where-Object { $_.KeyName -eq 'DEVPKEY_Device_DriverVersion' }).Data;
                                } catch { }
                                Write-Output ('{0}|{1}|{2}|{3}|{4}' -f $name, $status, $driverFile, $driverDate, $driverVersion);
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
                            var parts = line.Split('|');
                            if (parts.Length >= 5)
                            {
                                DateTime? driverDate = null;
                                if (DateTime.TryParse(parts[3], out var parsedDate))
                                {
                                    driverDate = parsedDate;
                                }

                                ports.Add(new SerialPortInfo
                                {
                                    Name = parts[0],
                                    Status = parts[1],
                                    DriverFileName = parts[2],
                                    DriverDate = driverDate,
                                    DriverVersion = parts[4]
                                });
                            }
                        }
                    }
                }
                catch (Exception ex)
                {
                    Debug.WriteLine($"Error getting serial ports: {ex.Message}");
                }
            });

            // Sort by name and add to collection
            var sorted = ports.OrderBy(p => p.Name).ToList();
            foreach (var port in sorted)
            {
                SerialPorts.Add(port);
            }

            StatusMessage = $"Found {SerialPorts.Count} serial port(s)";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error scanning serial ports: {ex.Message}";
        }
    }

    /// <summary>
    /// Enhanced event log search that includes PathMasterX events and unexpected power loss events.
    /// </summary>
    private async Task SearchEventLogsWithPowerLossAsync()
    {
        try
        {
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

                // Search Windows Error Reporting logs
                SearchWerLogs(searchTerms);

                // Search for power loss / unexpected shutdown events
                SearchPowerLossEvents();
            });

            EventSearchStatus = $"Found {EventLogItems.Count} events (including power events)";
            StatusMessage = $"Event search complete - Found {EventLogItems.Count} events";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error searching event logs: {ex.Message}";
            EventSearchStatus = $"Error: {ex.Message}";
        }
    }

    /// <summary>
    /// Searches for power-related events indicating unexpected shutdowns or power loss.
    /// Event ID 41 (Kernel-Power): System rebooted without cleanly shutting down first.
    /// Event ID 6008 (EventLog): Previous system shutdown was unexpected.
    /// Event ID 1074 (User32): System initiated restart/shutdown (for context).
    /// </summary>
    private void SearchPowerLossEvents()
    {
        try
        {
            // Search for Kernel-Power critical events (Event ID 41 - unexpected shutdown)
            var kernelPowerQuery = new System.Diagnostics.Eventing.Reader.EventLogQuery(
                "System",
                System.Diagnostics.Eventing.Reader.PathType.LogName,
                "*[System[Provider[@Name='Microsoft-Windows-Kernel-Power'] and (EventID=41)]]");

            using (var reader = new System.Diagnostics.Eventing.Reader.EventLogReader(kernelPowerQuery))
            {
                System.Diagnostics.Eventing.Reader.EventRecord? record;
                while ((record = reader.ReadEvent()) is not null)
                {
                    try
                    {
                        string description = record.FormatDescription() ?? "The system rebooted without cleanly shutting down first.";

                        var logItem = new EventLogItem
                        {
                            Name = "Kernel-Power",
                            EventId = record.Id,
                            Level = EventLogLevel.Critical,
                            StatusText = $"Critical - Unexpected Shutdown - {record.TimeCreated:g}",
                            Details = description,
                            Category = "Power Loss",
                            TimeCreated = record.TimeCreated ?? DateTime.MinValue
                        };

                        System.Windows.Application.Current.Dispatcher.InvokeAsync(() =>
                        {
                            InsertEventLogItemSorted(logItem);
                            EventSearchStatus = $"Found {EventLogItems.Count} events...";
                        });
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

            // Search for EventLog provider event ID 6008 (Previous shutdown was unexpected)
            var eventLogQuery = new System.Diagnostics.Eventing.Reader.EventLogQuery(
                "System",
                System.Diagnostics.Eventing.Reader.PathType.LogName,
                "*[System[Provider[@Name='EventLog'] and (EventID=6008)]]");

            using (var reader = new System.Diagnostics.Eventing.Reader.EventLogReader(eventLogQuery))
            {
                System.Diagnostics.Eventing.Reader.EventRecord? record;
                while ((record = reader.ReadEvent()) is not null)
                {
                    try
                    {
                        string description = record.FormatDescription() ?? "The previous system shutdown was unexpected.";

                        var logItem = new EventLogItem
                        {
                            Name = "EventLog",
                            EventId = record.Id,
                            Level = EventLogLevel.Error,
                            StatusText = $"Error - Unexpected Shutdown - {record.TimeCreated:g}",
                            Details = description,
                            Category = "Power Loss",
                            TimeCreated = record.TimeCreated ?? DateTime.MinValue
                        };

                        System.Windows.Application.Current.Dispatcher.InvokeAsync(() =>
                        {
                            InsertEventLogItemSorted(logItem);
                            EventSearchStatus = $"Found {EventLogItems.Count} events...";
                        });
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

            // Search for User32 event ID 1074 (shutdown/restart initiated - for context)
            var user32Query = new System.Diagnostics.Eventing.Reader.EventLogQuery(
                "System",
                System.Diagnostics.Eventing.Reader.PathType.LogName,
                "*[System[Provider[@Name='User32'] and (EventID=1074)]]");

            using (var reader = new System.Diagnostics.Eventing.Reader.EventLogReader(user32Query))
            {
                System.Diagnostics.Eventing.Reader.EventRecord? record;
                int count = 0;
                while ((record = reader.ReadEvent()) is not null && count < 50) // Limit to 50 for performance
                {
                    try
                    {
                        string description = record.FormatDescription() ?? "The process initiated a restart or shutdown.";

                        var logItem = new EventLogItem
                        {
                            Name = "User32",
                            EventId = record.Id,
                            Level = EventLogLevel.Information,
                            StatusText = $"Shutdown/Restart Initiated - {record.TimeCreated:g}",
                            Details = description,
                            Category = "Power Events",
                            TimeCreated = record.TimeCreated ?? DateTime.MinValue
                        };

                        System.Windows.Application.Current.Dispatcher.InvokeAsync(() =>
                        {
                            InsertEventLogItemSorted(logItem);
                            EventSearchStatus = $"Found {EventLogItems.Count} events...";
                        });

                        count++;
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
        }
        catch (Exception ex)
        {
            Debug.WriteLine($"Error searching power loss events: {ex.Message}");
        }
    }

    /// <summary>
    /// Helper method to insert an event log item in sorted order by time (newest first).
    /// </summary>
    private void InsertEventLogItemSorted(EventLogItem logItem)
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
            if (file[sourceDir.Length..].StartsWith("\\lib"))
            {
                continue;
            }

            string relativePath = Path.GetRelativePath(sourceDir, file);
            string targetFile = Path.Combine(targetDir, relativePath);
            string? targetFileDir = Path.GetDirectoryName(targetFile);

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
