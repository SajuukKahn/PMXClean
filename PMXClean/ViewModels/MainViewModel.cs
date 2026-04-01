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
    public partial string NetworkUtilityOutput { get; set; } = string.Empty;

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

    #endregion

    #region Collections

    public ObservableCollection<PathMasterXInstallation> Installations { get; }
        public ObservableCollection<string> AvailableVersions { get; }
        public ObservableCollection<string> BackupInstances { get; }
        public ObservableCollection<LargeFileResult> LargeFiles { get; } = [];
        public ObservableCollection<LockedFileItem> LockedFiles { get; } = [];
        public ObservableCollection<PageInfo> AvailablePages { get; } = [];

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
            return $"{(type == InstallationType.ProgramFiles ? "[Production]" : "[Dev]")} {path}";
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

            ComparisonViewModel.SetupComparison(
                sourceDir,
                SelectedInstallation.Path,
                SelectedVersion,
                "Installed");
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

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task CopyJsonToDestinationAsync() => await CopyToDestinationByPatternAsync("*.json", "JSON");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task CopyRetentionToDestinationAsync() => await CopyToDestinationByPatternAsync("*.retention", "Retention");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task CopyPythonToDestinationAsync() => await CopyToDestinationByPatternAsync("*.py", "Python");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task CopyDllsToDestinationAsync() => await CopyToDestinationByPatternAsync("*.DLL", "DLLs");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task CopyStubsToDestinationAsync() => await CopyToDestinationByPatternAsync("*.stub", "Page Stubs");

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
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

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
    private async Task CopyProgramFilesToDestinationAsync()
    {
        if (!ValidateBackupSelected())
        {
            return;
        }

        await CopyFeatureFolderToDestinationAsync("Program", "Program");
    }

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
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

                await CopyFilesByPatternAsync(backupPath, SelectedInstallation.Path, pattern);
                StatusMessage = $"{fileType} copied to destination";
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

            string cameraBackupPath = Path.Combine(_backupsRootDirectory, SelectedBackup, "Device", "Camera");

            if (!Directory.Exists(cameraBackupPath))
            {
                return false;
            }

            try
            {
                string[] excludedExtensions = [".dll", ".json", ".py"];
                return Directory.GetFiles(cameraBackupPath, "*", SearchOption.AllDirectories)
                    .Any(f => !excludedExtensions.Contains(Path.GetExtension(f).ToLowerInvariant()));
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
                return Directory.GetFiles(featureBackupPath, "*", SearchOption.AllDirectories).Length > 0;
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

            await Task.Run(() =>
            {
                CopyDirectoryStructure(SelectedInstallation!.Path, backupPath);
                CopyFilesByPattern(SelectedInstallation.Path, backupPath, pattern);
            });

            UpdateBackupInfo();
            NotifyRemoveCommandsCanExecuteChanged();
            StatusMessage = $"{fileType} backup complete";
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
    }

    [RelayCommand(CanExecute = nameof(CanBackupOrCopy))]
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
            NetworkUtilityOutput = string.Empty;

            await GetConsolidatedAdapterInfoAsync();

            // Ping devices
            NetworkUtilityOutput += "\nPinging Galil (100.100.100.101)\n";
            bool galilOnline = await PingHostAsync("100.100.100.101");
            NetworkUtilityOutput += galilOnline ? "    Status: Online\n" : "    Status: Offline\n";

            NetworkUtilityOutput += "\nPinging Modbus I/O (100.100.100.110)\n";
            bool modbusOnline = await PingHostAsync("100.100.100.110");
            NetworkUtilityOutput += modbusOnline ? "    Status: Online\n" : "    Status: Offline\n";

            NetworkUtilityOutput += "\nPinging Camera (200.200.200.201)\n";
            bool cameraOnline = await PingHostAsync("200.200.200.201");
            NetworkUtilityOutput += cameraOnline ? "    Status: Online\n" : "    Status: Offline\n";

            StatusMessage = "Network check complete";
        }
        catch (Exception ex)
        {
            StatusMessage = $"Error: {ex.Message}";
        }
    }

    private async Task GetConsolidatedAdapterInfoAsync()
    {
        await Task.Run(() =>
        {
            try
            {
                // Single query to get all adapter information at once
                var psi = new ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    Arguments = @"-ExecutionPolicy Bypass -Command ""
                        $adapters = Get-NetAdapter | Where-Object { $_.Status -eq 'Up' };
                        foreach ($adapter in $adapters) {
                            Write-Output ('Adapter: ' + $adapter.Name);
                            Write-Output ('  Status: ' + $adapter.Status);

                            # Get IP configuration
                            $ipConfig = Get-NetIPConfiguration -InterfaceAlias $adapter.Name -ErrorAction SilentlyContinue;
                            if ($ipConfig) {
                                if ($ipConfig.IPv4Address) {
                                    Write-Output ('  IPv4: ' + $ipConfig.IPv4Address.IPAddress);
                                }
                                if ($ipConfig.IPv4DefaultGateway) {
                                    Write-Output ('  Gateway: ' + $ipConfig.IPv4DefaultGateway.NextHop);
                                }
                                if ($ipConfig.DNSServer) {
                                    $dnsServers = ($ipConfig.DNSServer | Where-Object { $_.AddressFamily -eq 2 } | Select-Object -ExpandProperty ServerAddresses) -join ', ';
                                    if ($dnsServers) {
                                        Write-Output ('  DNS: ' + $dnsServers);
                                    }
                                }
                            }

                            # Get advanced properties (only for Ethernet adapters)
                            if ($adapter.PhysicalMediaType -like '*802.3*') {
                                $props = Get-NetAdapterAdvancedProperty -Name $adapter.Name -ErrorAction SilentlyContinue;

                                # Jumbo Frames
                                $jumbo = $props | Where-Object { $_.RegistryKeyword -eq '*JumboPacket' } | Select-Object -ExpandProperty DisplayValue -ErrorAction SilentlyContinue;
                                if ($jumbo) { Write-Output ('  Jumbo Frames: ' + $jumbo); }
                            }

                            Write-Output '';
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
                    NetworkUtilityOutput += result.TrimEnd() + "\n";
                }
            }
            catch (Exception ex)
            {
                NetworkUtilityOutput += $"Error getting adapter info: {ex.Message}\n";
            }
        });
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

            UtilityOutput = $"Found {LargeFiles.Count} files larger than 200MB";
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
            if (dir[sourceDir.Length..].StartsWith("\\lib"))
            {
                continue;
            }

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
            if (targetFileDir?[sourceDir.Length..].StartsWith("\\lib") == true)
            {
                continue;
            }

            if (targetFileDir is not null && !Directory.Exists(targetFileDir))
            {
                Directory.CreateDirectory(targetFileDir);
            }

            File.Copy(file, targetFile, true);
        }
    }

    private static Task CopyFilesByPatternAsync(string sourceDir, string targetDir, string pattern)
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
