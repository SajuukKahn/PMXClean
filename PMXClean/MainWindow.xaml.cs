    namespace PMXClean
{
    using System.Diagnostics;
    using System.IO;
    using System.Net.NetworkInformation;
    using System.Text;
    using System.Windows;
    using System.Windows.Controls;
    using System.Windows.Data;
    using System.Windows.Documents;
    using System.Windows.Input;
    using System.Windows.Media;
    using System.Windows.Media.Imaging;
    using System.Windows.Navigation;

    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private string currentTargetPath;
        private readonly string winMergePath;
        private readonly string appBaseDirectory;
        private readonly string backupsRootDirectory;
        private string? currentBackupPath;
        private List<PathMasterXInstallation> discoveredInstallations;

        public MainWindow()
        {
            InitializeComponent();

            // Get the application base directory
            appBaseDirectory = AppDomain.CurrentDomain.BaseDirectory;
            backupsRootDirectory = System.IO.Path.Combine(appBaseDirectory, "Backups");

            // Construct WinMerge path relative to application
            winMergePath = System.IO.Path.Combine(appBaseDirectory, 
                @"WinMergePortable\App\WinMerge64\WinMergeU.exe");

            currentTargetPath = string.Empty;
            discoveredInstallations = new List<PathMasterXInstallation>();

            InitializePaths();
            ValidateWinMerge();
            LoadBackupInstances();
        }

        private class PathMasterXInstallation
        {
            public string Path { get; set; } = string.Empty;
            public string DisplayName { get; set; } = string.Empty;
            public InstallationType Type { get; set; }
        }

        private enum InstallationType
        {
            ProgramFiles,
            UserDevelopment,
            Custom
        }

        private void ValidateWinMerge()
        {
            if (!File.Exists(winMergePath))
            {
                UpdateStatus("Warning: WinMerge not found - Python comparison features will not work");
            }
        }

        private string GetWorkingDirectory()
        {
            // For single-file deployment, working directory will be the extraction folder
            return appBaseDirectory;
        }

        private void UpdateStatus(string message)
        {
            StatusTextBlock.Text = message;
        }

        private void InitializePaths()
        {
            UpdateStatus("Discovering PathMasterX installations...");
            DiscoverPathMasterXInstallations();
            PopulateTargetPathComboBox();
        }

        private void DiscoverPathMasterXInstallations()
        {
            discoveredInstallations.Clear();

            // Search C:\Program Files and C:\Program Files (x86)
            SearchProgramFiles();

            // Search user repositories
            SearchUserRepositories();

            if (discoveredInstallations.Count == 0)
            {
                UpdateStatus("Warning: No PathMasterX installations found - Application will have limited functionality");
            }
            else
            {
                UpdateStatus($"Found {discoveredInstallations.Count} PathMasterX installation(s)");
            }
        }

        private void SearchProgramFiles()
        {
            var programFilesPaths = new[]
            {
                Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles),
                Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86)
            };

            foreach (var programFilesPath in programFilesPaths)
            {
                if (string.IsNullOrEmpty(programFilesPath) || !Directory.Exists(programFilesPath))
                {
                    continue;
                }

                try
                {
                    // Search for PVA.PathMasterX.exe in Program Files
                    SearchForExecutable(programFilesPath, InstallationType.ProgramFiles, maxDepth: 4);
                }
                catch (Exception ex)
                {
                    // Log but don't show error - this is expected for access denied
                    Debug.WriteLine($"Error searching {programFilesPath}: {ex.Message}");
                }
            }
        }

        private void SearchUserRepositories()
        {
            try
            {
                string usersPath = @"C:\Users";
                if (!Directory.Exists(usersPath))
                {
                    return;
                }

                foreach (var userDir in Directory.GetDirectories(usersPath))
                {
                    try
                    {
                        var userDirInfo = new DirectoryInfo(userDir);

                        // Skip Public and other system users
                        if (userDirInfo.Name.Equals("Public", StringComparison.OrdinalIgnoreCase) ||
                            userDirInfo.Name.Equals("Default", StringComparison.OrdinalIgnoreCase) ||
                            userDirInfo.Name.Equals("Default User", StringComparison.OrdinalIgnoreCase) ||
                            userDirInfo.Name.Equals("All Users", StringComparison.OrdinalIgnoreCase))
                        {
                            continue;
                        }

                        // Search in source\repos
                        string reposPath = System.IO.Path.Combine(userDir, "source", "repos");
                        if (Directory.Exists(reposPath))
                        {
                            SearchForPathMasterXInRepos(reposPath);
                        }

                        // Also check Documents\repos (alternative location)
                        string docsReposPath = System.IO.Path.Combine(userDir, "Documents", "repos");
                        if (Directory.Exists(docsReposPath))
                        {
                            SearchForPathMasterXInRepos(docsReposPath);
                        }
                    }
                    catch (UnauthorizedAccessException)
                    {
                        // Skip users we don't have access to
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

        private void SearchForPathMasterXInRepos(string reposPath)
        {
            try
            {
                // Do a depth-first search for PVA.PathMasterX.exe (not PathMasterX-LicenseGenerator, etc.)
                // Typical structure: repos\precisionvalve\PathMasterX\PathMasterX\bin\...
                SearchForExecutable(reposPath, InstallationType.UserDevelopment, maxDepth: 8);
            }
            catch (Exception ex)
            {
                Debug.WriteLine($"Error searching repos at {reposPath}: {ex.Message}");
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
                // Look for PVA.PathMasterX.exe in current directory
                string exePath = System.IO.Path.Combine(searchPath, "PVA.PathMasterX.exe");
                if (File.Exists(exePath))
                {
                    var directory = System.IO.Path.GetDirectoryName(exePath);
                    if (!string.IsNullOrEmpty(directory) && !InstallationAlreadyAdded(directory))
                    {
                        var installation = new PathMasterXInstallation
                        {
                            Path = directory,
                            DisplayName = GenerateDisplayName(directory, installType),
                            Type = installType
                        };
                        discoveredInstallations.Add(installation);
                    }

                    return; // Found it, no need to search deeper
                }

                // Search subdirectories
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

        private bool InstallationAlreadyAdded(string path)
        {
            return discoveredInstallations.Any(i => 
                i.Path.Equals(path, StringComparison.OrdinalIgnoreCase));
        }

        private string GenerateDisplayName(string path, InstallationType type)
        {
            try
            {
                switch (type)
                {
                    case InstallationType.ProgramFiles:
                        return $"[Production] {path}";

                    case InstallationType.UserDevelopment:
                        // Extract meaningful parts from the path
                        var parts = path.Split(System.IO.Path.DirectorySeparatorChar);
                        var relevantParts = new List<string>();

                        bool foundBin = false;
                        for (int i = parts.Length - 1; i >= 0; i--)
                        {
                            relevantParts.Insert(0, parts[i]);
                            if (parts[i].Equals("bin", StringComparison.OrdinalIgnoreCase))
                            {
                                foundBin = true;
                                if (i > 0)
                                {
                                    relevantParts.Insert(0, parts[i - 1]); // Add project name
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

                    default:
                        return path;
                }
            }
            catch
            {
                return path;
            }
        }

        private void PopulateTargetPathComboBox()
        {
            TargetPathComboBox.Items.Clear();

            // Sort: Production first, then Development
            var sortedInstallations = discoveredInstallations
                .OrderBy(i => i.Type == InstallationType.ProgramFiles ? 0 : 1)
                .ThenBy(i => i.DisplayName)
                .ToList();

            foreach (var installation in sortedInstallations)
            {
                TargetPathComboBox.Items.Add(installation);
            }

            // Set DisplayMemberPath to show DisplayName
            TargetPathComboBox.DisplayMemberPath = "DisplayName";

            // Select first item if available
            if (TargetPathComboBox.Items.Count > 0)
            {
                TargetPathComboBox.SelectedIndex = 0;
            }
        }

        private void TargetPathComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (TargetPathComboBox.SelectedItem is PathMasterXInstallation installation)
            {
                currentTargetPath = installation.Path;
                UpdateStatus($"Selected: {installation.DisplayName}");
                UpdateFileVersionDisplay();
            }
        }

        private void UpdateFileVersionDisplay()
        {
            try
            {
                if (string.IsNullOrEmpty(currentTargetPath))
                {
                    FileVersionTextBlock.Text = "";
                    return;
                }

                string exePath = System.IO.Path.Combine(currentTargetPath, "PVA.PathMasterX.exe");

                if (File.Exists(exePath))
                {
                    var versionInfo = FileVersionInfo.GetVersionInfo(exePath);
                    string version = versionInfo.FileVersion ?? "Unknown";
                    string productVersion = versionInfo.ProductVersion ?? version;

                    FileVersionTextBlock.Text = $"File Version: {version}";
                }
                else
                {
                    FileVersionTextBlock.Text = "Executable not found";
                }
            }
            catch (Exception ex)
            {
                FileVersionTextBlock.Text = $"Error reading version: {ex.Message}";
            }
        }

        private void OpenTargetFolder_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                if (string.IsNullOrEmpty(currentTargetPath))
                {
                    UpdateStatus("Error: No target path selected");
                    return;
                }

                if (!Directory.Exists(currentTargetPath))
                {
                    UpdateStatus("Error: Target directory does not exist");
                    return;
                }

                Process.Start(new ProcessStartInfo
                {
                    FileName = "explorer.exe",
                    Arguments = currentTargetPath,
                    UseShellExecute = true
                });

                UpdateStatus($"Opened folder: {currentTargetPath}");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error opening folder: {ex.Message}");
            }
        }

        private void RefreshPaths_Click(object sender, RoutedEventArgs e)
        {
            DiscoverPathMasterXInstallations();

            // Remember current selection if possible
            string previousPath = currentTargetPath;

            PopulateTargetPathComboBox();

            // Try to restore previous selection
            if (!string.IsNullOrEmpty(previousPath))
            {
                var previousInstallation = discoveredInstallations
                    .FirstOrDefault(i => i.Path.Equals(previousPath, StringComparison.OrdinalIgnoreCase));

                if (previousInstallation != null)
                {
                    TargetPathComboBox.SelectedItem = previousInstallation;
                }
            }

            UpdateStatus($"Refresh complete - Found {discoveredInstallations.Count} installation(s)");
        }

        // Compare Python Methods
        private void CompareInstalled_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                UpdateStatus("Copying files for comparison...");

                string targetDir = System.IO.Path.Combine(GetWorkingDirectory(), "target");

                if (Directory.Exists(targetDir))
                {
                    Directory.Delete(targetDir, true);
                }

                Directory.CreateDirectory(targetDir);

                CopyDirectoryStructure(currentTargetPath, targetDir);
                CopyFilesByPattern(currentTargetPath, targetDir, "*.py");

                UpdateStatus("Starting WinMerge...");

                string masterDir = System.IO.Path.Combine(GetWorkingDirectory(), "master");

                if (!File.Exists(winMergePath))
                {
                    UpdateStatus("Error: WinMerge not found - Please ensure WinMergePortable is included");
                    return;
                }

                Process.Start(new ProcessStartInfo
                {
                    FileName = winMergePath,
                    Arguments = $"/r /f *.py /u /wl /dl \"SOURCE\" \"{masterDir}\" \"{targetDir}\"",
                    UseShellExecute = true
                });
                UpdateStatus("WinMerge launched successfully");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error during comparison: {ex.Message}");
            }
        }

        private void PullFreshMaster_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                UpdateStatus("Copying files from source to master...");

                string masterDir = System.IO.Path.Combine(GetWorkingDirectory(), "master");

                if (Directory.Exists(masterDir))
                {
                    Directory.Delete(masterDir, true);
                }

                Directory.CreateDirectory(masterDir);

                CopyDirectoryStructure(currentTargetPath, masterDir);
                CopyFilesByPattern(currentTargetPath, masterDir, "*.py");

                UpdateStatus("Copy from source to master complete");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error pulling fresh master: {ex.Message}");
            }
        }

        // Backup Management Methods
        private void LoadBackupInstances()
        {
            BackupComboBox.Items.Clear();

            if (!Directory.Exists(backupsRootDirectory))
            {
                Directory.CreateDirectory(backupsRootDirectory);
            }

            var backupDirs = Directory.GetDirectories(backupsRootDirectory)
                .Select(d => new DirectoryInfo(d))
                .OrderByDescending(d => d.LastWriteTime)
                .ToList();

            foreach (var dir in backupDirs)
            {
                BackupComboBox.Items.Add(dir.Name);
            }

            if (BackupComboBox.Items.Count > 0)
            {
                BackupComboBox.SelectedIndex = 0;
            }
            else
            {
                UpdateBackupInfo();
            }
        }

        private void BackupComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (BackupComboBox.SelectedItem != null)
            {
                string backupName = BackupComboBox.SelectedItem.ToString()!;
                currentBackupPath = System.IO.Path.Combine(backupsRootDirectory, backupName);
                UpdateBackupInfo();
            }
            else
            {
                currentBackupPath = null;
                UpdateBackupInfo();
            }
        }

        private void UpdateBackupInfo()
        {
            if (string.IsNullOrEmpty(currentBackupPath) || !Directory.Exists(currentBackupPath))
            {
                BackupInfoTextBlock.Text = "No backup selected. Create a new backup to begin.";
                BackupInfoTextBlock.Foreground = new SolidColorBrush(Colors.Gray);
                return;
            }

            try
            {
                var dirInfo = new DirectoryInfo(currentBackupPath);
                var fileCount = Directory.GetFiles(currentBackupPath, "*", SearchOption.AllDirectories).Length;
                var totalSize = Directory.GetFiles(currentBackupPath, "*", SearchOption.AllDirectories)
                    .Sum(f => new FileInfo(f).Length);
                var sizeMB = totalSize / 1024.0 / 1024.0;

                BackupInfoTextBlock.Text = $"Created: {dirInfo.CreationTime:g}\n" +
                                          $"Modified: {dirInfo.LastWriteTime:g}\n" +
                                          $"Files: {fileCount:N0} ({sizeMB:N2} MB)";
                BackupInfoTextBlock.Foreground = new SolidColorBrush(Colors.Black);
            }
            catch (Exception ex)
            {
                BackupInfoTextBlock.Text = $"Error reading backup info: {ex.Message}";
                BackupInfoTextBlock.Foreground = new SolidColorBrush(Colors.Red);
            }
        }

        private void NewBackupInstance_Click(object sender, RoutedEventArgs e)
        {
            // Show inline textbox for new backup name
            string defaultName = $"Backup_{DateTime.Now:yyyyMMdd_HHmmss}";
            BackupNewNameTextBox.Text = defaultName;
            BackupNewNameTextBox.Tag = "new"; // Mark as new operation
            BackupComboBox.Visibility = Visibility.Collapsed;
            BackupNewNameTextBox.Visibility = Visibility.Visible;
            BackupNewNameTextBox.Focus();
            BackupNewNameTextBox.SelectAll();
            UpdateStatus("Enter backup name and press Enter or Esc to cancel");
        }

        private void BackupNewNameTextBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                CreateNewBackup(BackupNewNameTextBox.Text);
                BackupNewNameTextBox.Visibility = Visibility.Collapsed;
                BackupComboBox.Visibility = Visibility.Visible;
                e.Handled = true;
            }
            else if (e.Key == Key.Escape)
            {
                BackupNewNameTextBox.Visibility = Visibility.Collapsed;
                BackupComboBox.Visibility = Visibility.Visible;
                UpdateStatus("Backup creation cancelled");
                e.Handled = true;
            }
        }

        private void BackupNewNameTextBox_LostFocus(object sender, RoutedEventArgs e)
        {
            if (BackupNewNameTextBox.Visibility == Visibility.Visible)
            {
                BackupNewNameTextBox.Visibility = Visibility.Collapsed;
                BackupComboBox.Visibility = Visibility.Visible;
            }
        }

        private void CreateNewBackup(string backupName)
        {
            if (string.IsNullOrWhiteSpace(backupName))
            {
                UpdateStatus("Error: Backup name cannot be empty");
                return;
            }

            // Sanitize backup name
            foreach (char c in System.IO.Path.GetInvalidFileNameChars())
            {
                backupName = backupName.Replace(c, '_');
            }

            string newBackupPath = System.IO.Path.Combine(backupsRootDirectory, backupName);

            if (Directory.Exists(newBackupPath))
            {
                UpdateStatus($"Error: Backup '{backupName}' already exists");
                return;
            }

            try
            {
                Directory.CreateDirectory(newBackupPath);
                LoadBackupInstances();
                BackupComboBox.SelectedItem = backupName;
                UpdateStatus($"Created new backup: {backupName}");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error creating backup: {ex.Message}");
            }
        }

        private void RenameBackup_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(currentBackupPath))
            {
                UpdateStatus("Error: Please select a backup to rename");
                return;
            }

            string currentName = System.IO.Path.GetFileName(currentBackupPath);
            BackupRenameTextBox.Text = currentName;
            BackupRenameTextBox.Tag = currentBackupPath; // Store original path
            BackupComboBox.Visibility = Visibility.Collapsed;
            BackupRenameTextBox.Visibility = Visibility.Visible;
            BackupRenameTextBox.Focus();
            BackupRenameTextBox.SelectAll();
            UpdateStatus("Enter new backup name and press Enter or Esc to cancel");
        }

        private void BackupRenameTextBox_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.Key == Key.Enter)
            {
                RenameBackup(BackupRenameTextBox.Tag?.ToString() ?? string.Empty, BackupRenameTextBox.Text);
                BackupRenameTextBox.Visibility = Visibility.Collapsed;
                BackupComboBox.Visibility = Visibility.Visible;
                e.Handled = true;
            }
            else if (e.Key == Key.Escape)
            {
                BackupRenameTextBox.Visibility = Visibility.Collapsed;
                BackupComboBox.Visibility = Visibility.Visible;
                UpdateStatus("Rename cancelled");
                e.Handled = true;
            }
        }

        private void BackupRenameTextBox_LostFocus(object sender, RoutedEventArgs e)
        {
            if (BackupRenameTextBox.Visibility == Visibility.Visible)
            {
                BackupRenameTextBox.Visibility = Visibility.Collapsed;
                BackupComboBox.Visibility = Visibility.Visible;
            }
        }

        private void RenameBackup(string oldPath, string newName)
        {
            if (string.IsNullOrWhiteSpace(newName))
            {
                UpdateStatus("Error: Backup name cannot be empty");
                return;
            }

            // Sanitize backup name
            foreach (char c in System.IO.Path.GetInvalidFileNameChars())
            {
                newName = newName.Replace(c, '_');
            }

            string newBackupPath = System.IO.Path.Combine(backupsRootDirectory, newName);

            if (Directory.Exists(newBackupPath))
            {
                UpdateStatus($"Error: Backup '{newName}' already exists");
                return;
            }

            try
            {
                Directory.Move(oldPath, newBackupPath);
                LoadBackupInstances();
                BackupComboBox.SelectedItem = newName;
                UpdateStatus($"Renamed backup to: {newName}");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error renaming backup: {ex.Message}");
            }
        }

        private void DeleteBackupInstance_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(currentBackupPath))
            {
                UpdateStatus("Error: Please select a backup to delete");
                return;
            }

            string backupName = System.IO.Path.GetFileName(currentBackupPath);

            try
            {
                Directory.Delete(currentBackupPath, true);
                UpdateStatus($"Deleted backup: {backupName}");
                LoadBackupInstances();
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error deleting backup: {ex.Message}");
            }
        }

        // Backup Operation Methods
        private void BackupAll_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(currentBackupPath))
            {
                UpdateStatus("Error: Please select or create a backup first");
                return;
            }

            try
            {
                UpdateStatus("Backing up all files...");

                CopyDirectoryStructure(currentTargetPath, currentBackupPath);
                CopyDirectoryRecursive(currentTargetPath, currentBackupPath);

                UpdateBackupInfo();
                UpdateStatus("All files backup complete");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error backing up all files: {ex.Message}");
            }
        }

        private void BackupJson_Click(object sender, RoutedEventArgs e)
        {
            BackupFilesByPattern("*.json", "JSON");
        }

        private void BackupRetention_Click(object sender, RoutedEventArgs e)
        {
            BackupFilesByPattern("*.retention", "Retention");
        }

        private void BackupPython_Click(object sender, RoutedEventArgs e)
        {
            BackupFilesByPattern("*.py", "Python");
        }

        private void BackupDlls_Click(object sender, RoutedEventArgs e)
        {
            BackupFilesByPattern("*.DLL", "DLLs");
        }

        private void BackupStubs_Click(object sender, RoutedEventArgs e)
        {
            BackupFilesByPattern("*.stub", "Page Stubs");
        }

        private void BackupFilesByPattern(string pattern, string fileType)
        {
            if (string.IsNullOrEmpty(currentBackupPath))
            {
                UpdateStatus("Error: Please select or create a backup first");
                return;
            }

            try
            {
                UpdateStatus($"Backing up {fileType}...");

                if (!Directory.Exists(currentBackupPath))
                {
                    Directory.CreateDirectory(currentBackupPath);
                }

                CopyDirectoryStructure(currentTargetPath, currentBackupPath);
                CopyFilesByPattern(currentTargetPath, currentBackupPath, pattern);

                UpdateBackupInfo();
                UpdateStatus($"{fileType} backup complete");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error backing up {fileType}: {ex.Message}");
            }
        }

        private void OverwriteTarget_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(currentBackupPath))
            {
                UpdateStatus("Error: Please select a backup to restore");
                return;
            }

            string backupName = System.IO.Path.GetFileName(currentBackupPath);

            try
            {
                UpdateStatus($"Restoring backup '{backupName}' to target...");

                if (!Directory.Exists(currentBackupPath))
                {
                    UpdateStatus("Error: Backup folder does not exist");
                    return;
                }

                CopyDirectoryRecursive(currentBackupPath, currentTargetPath);

                UpdateStatus("Restore complete");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error restoring backup: {ex.Message}");
            }
        }

        // Cleanup Methods
        private void DeleteJson_Click(object sender, RoutedEventArgs e)
        {
            DeleteFilesByPattern("*.json", "JSON");
        }

        private void DeleteRetention_Click(object sender, RoutedEventArgs e)
        {
            DeleteFilesByPattern("*.retention", "Retention");
        }

        private void DeletePython_Click(object sender, RoutedEventArgs e)
        {
            DeleteFilesByPattern("*.py", "Python");
        }

        private void DeletePageStubs_Click(object sender, RoutedEventArgs e)
        {
            DeleteFilesByPattern("*.stub", "Page Stubs");
        }

        private void DeleteFilesByPattern(string pattern, string fileType)
        {
            try
            {
                UpdateStatus($"Deleting {fileType}...");

                int count = 0;
                foreach (string file in Directory.GetFiles(currentTargetPath, pattern, SearchOption.AllDirectories))
                {
                    File.Delete(file);
                    count++;
                }

                UpdateStatus($"{fileType} deletion complete ({count} files)");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error deleting {fileType}: {ex.Message}");
            }
        }

        // Utility Methods
        private async void NetworkCheck_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                UpdateStatus("Checking network settings...");
                UtilityOutputTextBox.Clear();

                var output = new StringBuilder();
                output.AppendLine("=== Network Configuration ===\n");

                // Get network adapter info
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
                        if (process != null)
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

                // Ping Galil
                output.AppendLine("Pinging Galil (100.100.100.101)...");
                bool galilOnline = await PingHost("100.100.100.101");
                output.AppendLine(galilOnline ? "    Status: Online" : "    Status: Offline");

                // Ping Modbus I/O
                output.AppendLine("\nPinging Modbus I/O (100.100.100.110)...");
                bool modbusOnline = await PingHost("100.100.100.110");
                output.AppendLine(modbusOnline ? "    Status: Online" : "    Status: Offline");

                // Ping Camera
                output.AppendLine("\nPinging Camera (200.200.200.201)...");
                bool cameraOnline = await PingHost("200.200.200.201");
                output.AppendLine(cameraOnline ? "    Status: Online" : "    Status: Offline");

                UtilityOutputTextBox.Text = output.ToString();
                UpdateStatus("Network check complete");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error checking network: {ex.Message}", "Error", 
                    MessageBoxButton.OK, MessageBoxImage.Error);
                UpdateStatus($"Error: {ex.Message}");
            }
        }

        private async Task<bool> PingHost(string host)
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

        private async void CheckLargeFiles_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                UpdateStatus("Searching for large files...");
                UtilityOutputTextBox.Clear();
                UtilityOutputTextBox.Text = "Searching for files larger than 200MB...\nThis may take a while...\n\n";

                var output = new StringBuilder();
                output.AppendLine("=== Files larger than 200MB ===\n");

                await Task.Run(() =>
                {
                    string userPath = Environment.GetFolderPath(Environment.SpecialFolder.UserProfile);
                    long sizeThreshold = 209715200; // 200MB

                    SearchLargeFiles(userPath, sizeThreshold, output);
                });

                UtilityOutputTextBox.Text += output.ToString();
                UpdateStatus("Large file search complete");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error searching for large files: {ex.Message}");
            }
        }

        private void SearchLargeFiles(string path, long sizeThreshold, StringBuilder output)
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
                            output.AppendLine($"{fileInfo.FullName}");
                            output.AppendLine($"    Size: {fileInfo.Length / 1024 / 1024} MB");
                            output.AppendLine($"    Modified: {fileInfo.LastWriteTime}\n");
                        }
                    }
                    catch { }
                }

                foreach (string dir in Directory.GetDirectories(path))
                {
                    try
                    {
                        SearchLargeFiles(dir, sizeThreshold, output);
                    }
                    catch { }
                }
            }
            catch { }
        }

        // PMX Launcher
        private void LaunchPMX_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                UpdateStatus("Launching PMX...");

                var args = new List<string>();

                // Application switches
                if (OfflineCheckBox.IsChecked == true)
                {
                    args.Add("-offline");
                }

                if (AutoAdvanceCheckBox.IsChecked == true)
                {
                    args.Add("-autoAdvance");
                }

                if (SoftwareRenderingCheckBox.IsChecked == true)
                {
                    args.Add("-software");
                }

                if (FreeWindowCheckBox.IsChecked == true)
                {
                    args.Add("-freeWindow");
                }

                if (!string.IsNullOrWhiteSpace(StartPageTextBox.Text))
                {
                    args.Add($"-page:{StartPageTextBox.Text}");
                }

                // Window size
                if (!string.IsNullOrWhiteSpace(WindowWidthTextBox.Text) && 
                    !string.IsNullOrWhiteSpace(WindowHeightTextBox.Text))
                {
                    if (int.TryParse(WindowWidthTextBox.Text, out int width) && 
                        int.TryParse(WindowHeightTextBox.Text, out int height))
                    {
                        args.Add($"-size:{width}:{height}");
                    }
                    else
                    {
                        UpdateStatus("Error: Window size must be valid numbers");
                        return;
                    }
                }

                // Window position
                if (!string.IsNullOrWhiteSpace(WindowXTextBox.Text) && 
                    !string.IsNullOrWhiteSpace(WindowYTextBox.Text))
                {
                    if (int.TryParse(WindowXTextBox.Text, out int x) && 
                        int.TryParse(WindowYTextBox.Text, out int y))
                    {
                        args.Add($"-position:{x}:{y}");
                    }
                    else
                    {
                        UpdateStatus("Error: Window position must be valid numbers");
                        return;
                    }
                }

                // Vision switches
                if (VisionDebugCheckBox.IsChecked == true)
                {
                    args.Add("-visionDebug");
                }

                if (VisionTraceCheckBox.IsChecked == true)
                {
                    args.Add("-visionTrace");
                }

                // Screen Recording switches
                if (RecordOnStartupCheckBox.IsChecked == true)
                {
                    args.Add("-recordOnStartup");
                }

                if (RecordHighQualityCheckBox.IsChecked == true)
                {
                    args.Add("-recordHighQuality");
                }

                if (RecordHighFramerateCheckBox.IsChecked == true)
                {
                    args.Add("-recordHighFramerate");
                }

                if (RecordMicrophoneCheckBox.IsChecked == true)
                {
                    args.Add("-recordMicrophone");
                }

                if (RecordWebcamCheckBox.IsChecked == true)
                {
                    args.Add("-recordWebcam");
                }

                if (!string.IsNullOrWhiteSpace(MaxSegmentsTextBox.Text))
                {
                    if (int.TryParse(MaxSegmentsTextBox.Text, out int maxSegments))
                    {
                        args.Add($"-recordMaxSegments:{maxSegments}");
                    }
                    else
                    {
                        UpdateStatus("Error: Max segments must be a valid number");
                        return;
                    }
                }

                string exePath = System.IO.Path.Combine(currentTargetPath, "PVA.PathMasterX.exe");

                if (!File.Exists(exePath))
                {
                    UpdateStatus($"Error: PMX executable not found at {exePath}");
                    return;
                }

                Process.Start(new ProcessStartInfo
                {
                    FileName = exePath,
                    Arguments = string.Join(" ", args),
                    WorkingDirectory = currentTargetPath,
                    UseShellExecute = true
                });

                UpdateStatus($"PMX launched with arguments: {string.Join(" ", args)}");
            }
            catch (Exception ex)
            {
                UpdateStatus($"Error launching PMX: {ex.Message}");
            }
        }

        // Helper Methods
        private void CopyDirectoryStructure(string sourceDir, string targetDir)
        {
            foreach (string dir in Directory.GetDirectories(sourceDir, "*", SearchOption.AllDirectories))
            {
                string relativePath = System.IO.Path.GetRelativePath(sourceDir, dir);
                string newDir = System.IO.Path.Combine(targetDir, relativePath);
                Directory.CreateDirectory(newDir);
            }
        }

        private void CopyFilesByPattern(string sourceDir, string targetDir, string pattern)
        {
            foreach (string file in Directory.GetFiles(sourceDir, pattern, SearchOption.AllDirectories))
            {
                string relativePath = System.IO.Path.GetRelativePath(sourceDir, file);
                string targetFile = System.IO.Path.Combine(targetDir, relativePath);

                string? targetFileDir = System.IO.Path.GetDirectoryName(targetFile);
                if (targetFileDir != null && !Directory.Exists(targetFileDir))
                {
                    Directory.CreateDirectory(targetFileDir);
                }

                File.Copy(file, targetFile, true);
            }
        }

        private void CopyDirectoryRecursive(string sourceDir, string targetDir)
        {
            foreach (string file in Directory.GetFiles(sourceDir, "*", SearchOption.AllDirectories))
            {
                string relativePath = System.IO.Path.GetRelativePath(sourceDir, file);
                string targetFile = System.IO.Path.Combine(targetDir, relativePath);

                string? targetFileDir = System.IO.Path.GetDirectoryName(targetFile);
                if (targetFileDir != null && !Directory.Exists(targetFileDir))
                {
                    Directory.CreateDirectory(targetFileDir);
                }

                File.Copy(file, targetFile, true);
            }
        }
    }
}