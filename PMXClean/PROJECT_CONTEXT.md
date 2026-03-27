# PMXClean - Complete Project Context Document

**Last Updated**: 2025-01-15  
**Version**: 2.0  
**Status**: Production Ready

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture & Design Patterns](#architecture--design-patterns)
4. [Feature Implementation](#feature-implementation)
5. [File Structure](#file-structure)
6. [Code Patterns & Conventions](#code-patterns--conventions)
7. [UI/UX Design Philosophy](#uiux-design-philosophy)
8. [Deployment Configuration](#deployment-configuration)
9. [Evolution Timeline](#evolution-timeline)
10. [Future Enhancements](#future-enhancements)
11. [Troubleshooting Guide](#troubleshooting-guide)

---

## Project Overview

### Purpose
**PMXClean** is a utility tool for managing PathMasterX (PMX) installations. It provides:
- Multi-instance backup management
- Python file comparison with WinMerge
- File cleanup operations (JSON, Python, DLLs, retention files, page stubs)
- PMX launcher with 17 command-line switches
- Network diagnostics
- Large file discovery
- Dynamic PathMasterX installation discovery

### Origin
Originally a batch script (`ScriptUtility.bat`) that was refactored into a professional WPF application with advanced features and zero-configuration installation discovery.

### Target Users
- **Developers**: Working on PathMasterX code (development builds)
- **Field Engineers**: Managing production PathMasterX installations
- **QA/Testing**: Comparing builds, managing test configurations
- **Operations**: Backup/restore, cleanup, diagnostics

---

## Technology Stack

### Core Framework
- **.NET 10** (`net10.0-windows`)
- **C# 14.0** (latest language features)
- **WPF** (Windows Presentation Foundation)

### NuGet Packages
```xml
<PackageReference Include="CommunityToolkit.Mvvm" Version="8.4.2" />
<PackageReference Include="MaterialDesignThemes" Version="5.3.1" />
```

### External Tools
- **WinMergePortable**: Bundled with application (~38MB, 363 files)
  - Path: `WinMergePortable\App\WinMerge64\WinMergeU.exe`
  - Used for Python file comparison

### Development Environment
- **Visual Studio 2026 Professional** (18.4.2)
- **PowerShell** (deployment scripts)
- **Windows 10/11** (target OS)

---

## Architecture & Design Patterns

### Application Structure
```
PMXClean
├── MainWindow.xaml           # Main UI definition (5 tabs)
├── MainWindow.xaml.cs        # All business logic (code-behind)
├── InputDialog.xaml          # UNUSED - Replaced with inline textboxes
├── InputDialog.xaml.cs       # UNUSED - Replaced with inline textboxes
├── App.xaml                  # Application resources
├── Deploy.ps1                # Deployment automation
└── WinMergePortable\         # Bundled WinMerge installation
```

### Design Patterns

#### **Code-Behind Architecture**
- All logic in `MainWindow.xaml.cs` (not MVVM)
- Event-driven with direct UI manipulation
- Simple, maintainable, no abstraction layers

#### **Inline Editing Pattern**
```csharp
// Pattern: Overlay textbox on ComboBox for rename/create operations
<Grid>
    <ComboBox x:Name="TargetComboBox" ... />
    <TextBox x:Name="EditTextBox" Visibility="Collapsed" ... />
</Grid>

// Show textbox: Hide ComboBox, Show TextBox, Focus, SelectAll
// Hide textbox: Hide TextBox, Show ComboBox
// Triggers: Enter (commit), Esc (cancel), LostFocus (cancel)
```

#### **Silent Operations Philosophy**
- **No MessageBox dialogs** anywhere in the application
- All feedback via status bar at bottom
- Confirmations removed (destructive operations execute immediately)
- Errors displayed as status messages, not modal dialogs

#### **Dynamic Discovery Pattern**
- Recursive directory traversal with depth limits
- Exception handling for UnauthorizedAccessException
- Duplicate prevention
- Smart filtering (skip system users, ignore false positives)

---

## Feature Implementation

### 1. **Dynamic PathMasterX Installation Discovery**

#### Overview
Automatically finds all PathMasterX installations on the system without hardcoded paths.

#### Search Locations
1. **Program Files**:
   - `C:\Program Files\`
   - `C:\Program Files (x86)\`
   - Max depth: 4 levels
   - Type: `InstallationType.ProgramFiles`

2. **User Repositories**:
   - `C:\Users\[user]\source\repos\`
   - `C:\Users\[user]\Documents\repos\`
   - Skips: Public, Default, Default User, All Users
   - Max depth: 8 levels (repos are deeply nested)
   - Type: `InstallationType.UserDevelopment`

#### Discovery Algorithm
```csharp
private void SearchForExecutable(string searchPath, InstallationType installType, 
    int maxDepth, int currentDepth = 0)
{
    // Recursive depth-first search for "PVA.PathMasterX.exe"
    // Stops at first match in each directory tree
    // Handles UnauthorizedAccessException gracefully
    // Prevents duplicates with InstallationAlreadyAdded()
}
```

#### Display Names
- **Production**: `[Production] C:\Program Files\PVA\PathMasterX\`
- **Development**: `[Dev] PathMasterX\bin\x64\Debug\net8.0-windows\`

#### Data Structure
```csharp
private class PathMasterXInstallation
{
    public string Path { get; set; }           // Full directory path
    public string DisplayName { get; set; }    // User-friendly name
    public InstallationType Type { get; set; } // ProgramFiles or UserDevelopment
}

private enum InstallationType
{
    ProgramFiles,    // Production installs
    UserDevelopment, // Development builds
    Custom           // Future: user-added paths
}
```

---

### 2. **Multi-Instance Backup System**

#### Overview
Manage unlimited backup instances with create/rename/delete capabilities.

#### Backup Storage
- **Root Directory**: `[AppBaseDirectory]\Backups\`
- **Structure**: `Backups\[BackupName]\` (mirrors target directory structure)
- **Naming**: User-defined or auto-generated (`Backup_yyyyMMdd_HHmmss`)

#### Backup Operations

##### **Create New Backup**
1. Click "New..." button
2. Inline TextBox appears (overlays BackupComboBox)
3. Default name: `Backup_yyyyMMdd_HHmmss`
4. Press **Enter** to create, **Esc** to cancel
5. Creates empty directory, adds to ComboBox

##### **Rename Backup**
1. Select backup from ComboBox
2. Click "Rename..." button
3. Inline TextBox appears (overlays BackupComboBox)
4. Pre-populated with current name
5. Press **Enter** to rename, **Esc** to cancel
6. Uses `Directory.Move()`

##### **Delete Backup**
1. Select backup from ComboBox
2. Click "Delete" button
3. **No confirmation** - immediate deletion
4. Uses `Directory.Delete(path, true)`

#### Backup Content Operations
- **Copy All Files**: Complete directory mirror
- **Copy JSON**: `*.json` files only
- **Copy Retention**: `*.retention` files only
- **Copy Python**: `*.py` files only
- **Copy DLLs**: `*.DLL` files only
- **Copy Page Stubs**: `*.stub` files only
- **Restore to Target**: Overwrites target with backup (no confirmation)

#### Backup Metadata Display
```
Created: 1/15/2025 2:30 PM
Modified: 1/15/2025 3:45 PM
Files: 1,247 (345.67 MB)
```

#### Implementation Details
```csharp
// Inline editing for new backups
private void NewBackupInstance_Click(...)
{
    BackupComboBox.Visibility = Visibility.Collapsed;
    BackupNewNameTextBox.Visibility = Visibility.Visible;
    BackupNewNameTextBox.Focus();
    BackupNewNameTextBox.SelectAll();
}

// Name sanitization
foreach (char c in System.IO.Path.GetInvalidFileNameChars())
{
    backupName = backupName.Replace(c, '_');
}

// Duplicate prevention
if (Directory.Exists(newBackupPath))
{
    UpdateStatus($"Error: Backup '{backupName}' already exists");
    return;
}
```

---

### 3. **Python File Comparison with WinMerge**

#### Overview
Compare Python files between "master" (reference) and "target" (current installation).

#### Workflow

##### **Pull Fresh Master**
1. Deletes existing `master\` directory
2. Copies directory structure from target
3. Copies all `*.py` files to `master\`
4. Status: "Copy from source to master complete"

##### **Compare Installed**
1. Deletes existing `target\` directory
2. Copies directory structure from target
3. Copies all `*.py` files to `target\`
4. Launches WinMerge with arguments:
   ```
   /r /f *.py /u /wl /dl "SOURCE" "[masterDir]" "[targetDir]"
   ```
5. Status: "WinMerge launched successfully"

#### WinMerge Arguments Explained
- `/r`: Recursive comparison
- `/f *.py`: Filter for Python files
- `/u`: Unified diff format
- `/wl`: Ignore whitespace at line ends
- `/dl "SOURCE"`: Left panel label

#### Directory Structure
```
[AppBaseDirectory]
├── master\          # Reference copy (user-maintained)
│   └── [mirrors target structure]
└── target\          # Current installation copy (temporary)
    └── [mirrors target structure]
```

---

### 4. **File Cleanup Operations**

#### Overview
Delete specific file types from target installation (silent, no confirmation).

#### Supported File Types
1. **JSON Files** (`*.json`)
2. **Retention Files** (`*.retention`)
3. **Python Files** (`*.py`)
4. **Page Stubs** (`*.stub`)

#### Implementation
```csharp
private void DeleteFilesByPattern(string pattern, string fileType)
{
    try
    {
        UpdateStatus($"Deleting {fileType}...");
        
        int count = 0;
        foreach (string file in Directory.GetFiles(currentTargetPath, pattern, 
            SearchOption.AllDirectories))
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
```

#### Safety Considerations
- **No undo**: Deletions are permanent
- **No confirmation**: Silent execution (status bar feedback only)
- **Recursive**: Searches all subdirectories
- **Target-specific**: Only affects currently selected installation

---

### 5. **PMX Launcher with 17 Command-Line Switches**

#### Overview
Launch PathMasterX with custom configuration from GUI.

#### Switch Categories

##### **Application Switches (8)**
1. **Offline Mode** (`-offline`)
   - Disables network features
2. **Auto-Accept Prompts** (`-autoAdvance`)
   - Automatically accepts dialogs/prompts
3. **Software Only Rendering** (`-software`)
   - Disables hardware GPU acceleration
4. **Free Window** (`-freeWindow`)
   - Allows window to be moved and resized
5. **Start Page** (`-page:[name]`)
   - Navigate to specific page on startup
6. **Window Size** (`-size:[width]:[height]`)
   - Set initial window dimensions
7. **Window Position** (`-position:[X]:[Y]`)
   - Set initial window screen position

##### **Vision Switches (2)**
1. **Vision Debug** (`-visionDebug`)
   - Verbose error reporting for vision system
2. **Vision Trace** (`-visionTrace`)
   - External vision tracing/logging

##### **Screen Recording Switches (7)**
1. **Record On Startup** (`-recordOnStartup`)
   - Start recording immediately
2. **Record High Quality** (`-recordHighQuality`)
   - Use high-quality encoding
3. **Record High Framerate** (`-recordHighFramerate`)
   - 30 FPS instead of default
4. **Record Microphone** (`-recordMicrophone`)
   - Include microphone audio
5. **Record Webcam** (`-recordWebcam`)
   - Include webcam overlay
6. **Max Recording Segments** (`-recordMaxSegments:[maxSegments]`)
   - Limit consecutive 30-minute segments

#### Launch Process
```csharp
private void LaunchPMX_Click(...)
{
    // 1. Build argument list from UI controls
    var args = new List<string>();
    if (OfflineCheckBox.IsChecked == true) args.Add("-offline");
    // ... (repeat for all switches)
    
    // 2. Validate numeric inputs (window size, position, segments)
    if (!int.TryParse(WindowWidthTextBox.Text, out int width))
    {
        UpdateStatus("Error: Window size must be valid numbers");
        return;
    }
    
    // 3. Check if executable exists
    string exePath = System.IO.Path.Combine(currentTargetPath, "PVA.PathMasterX.exe");
    if (!File.Exists(exePath))
    {
        UpdateStatus($"Error: PMX executable not found at {exePath}");
        return;
    }
    
    // 4. Launch with Process.Start
    Process.Start(new ProcessStartInfo
    {
        FileName = exePath,
        Arguments = string.Join(" ", args),
        WorkingDirectory = currentTargetPath,
        UseShellExecute = true
    });
    
    // 5. Status feedback
    UpdateStatus($"PMX launched with arguments: {string.Join(" ", args)}");
}
```

---

### 6. **Network Diagnostics**

#### Overview
Check network configuration and device connectivity.

#### Features

##### **Network Configuration**
- Executes PowerShell command:
  ```powershell
  Get-NetIPConfiguration | Format-Table -Property 'InterfaceAlias','IPv4Address'
  ```
- Displays adapter names and IP addresses

##### **Ping Tests**
Three hardcoded devices (PathMasterX-specific hardware):
1. **Galil Motion Controller**: `100.100.100.101`
2. **Modbus I/O**: `100.100.100.110`
3. **Camera**: `200.200.200.201`

#### Implementation
```csharp
private async void NetworkCheck_Click(...)
{
    // Async to prevent UI blocking
    await Task.Run(() => /* PowerShell execution */);
    
    // Ping with 500ms timeout
    bool galilOnline = await PingHost("100.100.100.101");
    
    // Display results in UtilityOutputTextBox
    output.AppendLine(galilOnline ? "Status: Online" : "Status: Offline");
}

private async Task<bool> PingHost(string host)
{
    using var ping = new Ping();
    var reply = await ping.SendPingAsync(host, 500);
    return reply.Status == IPStatus.Success;
}
```

---

### 7. **Large File Discovery**

#### Overview
Recursively search user profile for files larger than 200MB.

#### Search Parameters
- **Root**: `%USERPROFILE%` (e.g., `C:\Users\mcannon\`)
- **Threshold**: 209,715,200 bytes (200MB)
- **Recursive**: All subdirectories
- **Silent failures**: Catches all exceptions (access denied, etc.)

#### Output Format
```
=== Files larger than 200MB ===

C:\Users\mcannon\Downloads\large_video.mp4
    Size: 534 MB
    Modified: 1/14/2025 10:30:15 AM

C:\Users\mcannon\Documents\project_backup.zip
    Size: 1024 MB
    Modified: 1/12/2025 3:45:00 PM
```

#### Implementation
```csharp
private void SearchLargeFiles(string path, long sizeThreshold, StringBuilder output)
{
    try
    {
        // Check files in current directory
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
            catch { } // Ignore file access errors
        }
        
        // Recursively search subdirectories
        foreach (string dir in Directory.GetDirectories(path))
        {
            try { SearchLargeFiles(dir, sizeThreshold, output); }
            catch { } // Ignore directory access errors
        }
    }
    catch { } // Ignore all other errors
}
```

---

### 8. **File Version Display**

#### Overview
Display the version from `PVA.PathMasterX.exe` in the header.

#### Implementation
```csharp
private void UpdateFileVersionDisplay()
{
    string exePath = System.IO.Path.Combine(currentTargetPath, "PVA.PathMasterX.exe");
    
    if (File.Exists(exePath))
    {
        var versionInfo = FileVersionInfo.GetVersionInfo(exePath);
        string version = versionInfo.FileVersion ?? "Unknown";
        FileVersionTextBlock.Text = $"File Version: {version}";
    }
    else
    {
        FileVersionTextBlock.Text = "Executable not found";
    }
}
```

#### Trigger Points
- On startup (first installation selected)
- On ComboBox selection change
- On "Refresh Paths" click

#### Visual Design
- **Color**: Light blue (`#FF90CAF9`)
- **Font**: 11pt italic
- **Location**: Below Target Path ComboBox in header
- **Format**: `File Version: 1.2.3.4567`

---

### 9. **Open Target Folder Button**

#### Overview
One-click access to open selected installation in Windows File Explorer.

#### Implementation
```csharp
private void OpenTargetFolder_Click(...)
{
    Process.Start(new ProcessStartInfo
    {
        FileName = "explorer.exe",
        Arguments = currentTargetPath,
        UseShellExecute = true
    });
}
```

#### Button Design
- **Icon**: 📁 (folder emoji)
- **Label**: "Open Folder"
- **Tooltip**: "Open target folder in File Explorer"
- **Location**: Between ComboBox and "Refresh Paths" button

---

## File Structure

```
PMXClean/
│
├── PMXClean.csproj               # Project configuration
├── App.xaml                      # Application resources
├── App.xaml.cs                   # Application startup logic
│
├── MainWindow.xaml               # Main UI (5 tabs, 600x900px)
├── MainWindow.xaml.cs            # All business logic (~1100 lines)
│
├── InputDialog.xaml              # UNUSED - Legacy dialog
├── InputDialog.xaml.cs           # UNUSED - Replaced with inline textboxes
│
├── Deploy.ps1                    # PowerShell deployment script
│
├── WinMergePortable/             # Bundled WinMerge installation
│   └── App/WinMerge64/
│       └── WinMergeU.exe
│
└── Documentation/
    ├── README.md                        # User guide
    ├── WINMERGE_INTEGRATION.md          # WinMerge bundling details
    ├── DEPLOYMENT_SUCCESS.md            # Deployment test results
    ├── BACKUP_MANAGER.md                # Backup system documentation
    ├── BACKUP_ENHANCEMENT_SUMMARY.md    # Backup redesign notes
    ├── PATH_DISCOVERY.md                # Discovery algorithm details
    ├── UI_IMPROVEMENTS.md               # MessageBox removal & inline editing
    ├── HEADER_ENHANCEMENTS.md           # Version display & folder button
    └── PROJECT_CONTEXT.md               # This file
```

---

## Code Patterns & Conventions

### Naming Conventions
- **UI Controls**: PascalCase with type suffix
  - `TargetPathComboBox`, `BackupNewNameTextBox`, `StatusTextBlock`
- **Event Handlers**: `ControlName_EventName`
  - `RefreshPaths_Click`, `BackupComboBox_SelectionChanged`
- **Private Fields**: camelCase with no prefix
  - `currentTargetPath`, `discoveredInstallations`
- **Classes**: PascalCase
  - `PathMasterXInstallation`
- **Enums**: PascalCase
  - `InstallationType`

### Error Handling Pattern
```csharp
try
{
    UpdateStatus("Starting operation...");
    
    // Operation logic here
    
    UpdateStatus("Operation complete");
}
catch (Exception ex)
{
    UpdateStatus($"Error: {ex.Message}");
}
```

**Key Points**:
- No `throw` - always catch and display
- Always update status bar
- No MessageBox - silent error reporting
- Logging via `Debug.WriteLine()` (not visible to users)

### Status Bar Updates
```csharp
private void UpdateStatus(string message)
{
    StatusTextBlock.Text = message;
}
```

**Usage**:
- Start of operation: "Starting operation..."
- Progress: "Processing files..."
- Success: "Operation complete (123 files)"
- Error: "Error: [exception message]"

### Async Operations Pattern
```csharp
private async void MethodName_Click(object sender, RoutedEventArgs e)
{
    try
    {
        UpdateStatus("Starting...");
        
        await Task.Run(() =>
        {
            // Long-running operation on background thread
        });
        
        UpdateStatus("Complete");
    }
    catch (Exception ex)
    {
        UpdateStatus($"Error: {ex.Message}");
    }
}
```

**Used For**:
- Network checks (PowerShell execution, ping)
- Large file search (recursive directory traversal)
- Any operation that might take > 100ms

### File Copy Pattern
```csharp
// 1. Create directory structure first
CopyDirectoryStructure(sourceDir, targetDir);

// 2. Copy files (by pattern or all)
CopyFilesByPattern(sourceDir, targetDir, "*.py");
// OR
CopyDirectoryRecursive(sourceDir, targetDir);

// Helper: Directory structure
private void CopyDirectoryStructure(string sourceDir, string targetDir)
{
    foreach (string dir in Directory.GetDirectories(sourceDir, "*", 
        SearchOption.AllDirectories))
    {
        string relativePath = System.IO.Path.GetRelativePath(sourceDir, dir);
        string newDir = System.IO.Path.Combine(targetDir, relativePath);
        Directory.CreateDirectory(newDir);
    }
}

// Helper: Files by pattern
private void CopyFilesByPattern(string sourceDir, string targetDir, string pattern)
{
    foreach (string file in Directory.GetFiles(sourceDir, pattern, 
        SearchOption.AllDirectories))
    {
        string relativePath = System.IO.Path.GetRelativePath(sourceDir, file);
        string targetFile = System.IO.Path.Combine(targetDir, relativePath);
        
        string? targetFileDir = System.IO.Path.GetDirectoryName(targetFile);
        if (targetFileDir != null && !Directory.Exists(targetFileDir))
        {
            Directory.CreateDirectory(targetFileDir);
        }
        
        File.Copy(file, targetFile, true); // Overwrite existing
    }
}
```

---

## UI/UX Design Philosophy

### Core Principles

#### 1. **Zero Interruptions**
- **No MessageBox dialogs** anywhere
- All feedback via status bar
- Operations complete without user intervention
- Keyboard-driven workflows (Enter/Esc shortcuts)

#### 2. **Inline Editing**
- TextBoxes overlay ComboBoxes for rename/create
- Immediate visual feedback
- Context remains visible (no modal dialogs)
- Example:
  ```
  [Before]  [ComboBox showing: Backup_20250115]
  [During]  [TextBox showing: Backup_20250115_v2 (editable)]
  [After]   [ComboBox showing: Backup_20250115_v2]
  ```

#### 3. **Silent Operations**
- Destructive operations execute immediately
- No "Are you sure?" confirmations
- Status bar provides success/failure feedback
- Trust user intent (power-user philosophy)

#### 4. **Progressive Disclosure**
- 5-tab layout groups related features
- Most common operations visible immediately
- Advanced switches organized in bordered sections
- Status bar always visible at bottom

#### 5. **Visual Hierarchy**
- **Headers**: 18pt Bold (section titles)
- **Subheaders**: 14pt Bold (subsection titles)
- **Body**: Default size (controls and content)
- **Status**: Always visible footer

### Color Scheme

#### **Header**
- Background: `#FF2D2D30` (dark gray)
- Text: White
- Version Text: `#FF90CAF9` (light blue)

#### **Backup Section**
- Title: `#FF4CAF50` (green)
- "New" Button: `#FF4CAF50` (green)
- "Copy All Files" Button: `#FF4CAF50` (green)
- "Launch PMX" Button: `#FF4CAF50` (green)

#### **Cleanup Section**
- Title: `#FFF44336` (red)
- All Buttons: `#FFCC4444` (light red)
- "Delete" Button: `#FFCC4444` (light red)
- "Restore to Target" Button: `#FFCC4444` (light red)

#### **Status Bar**
- Background: `#FF2D2D30` (dark gray)
- Text: White

### Layout Dimensions
- **Window**: 900x600 (initial size, resizable)
- **Button Heights**: 
  - Standard: 40px
  - Small (Backup management): 30px
  - Large (Launch PMX): 50px
- **Header ComboBox**: 32px
- **Backup ComboBox**: 30px

---

## Deployment Configuration

### Project Settings (PMXClean.csproj)

```xml
<PropertyGroup>
  <OutputType>WinExe</OutputType>
  <TargetFramework>net10.0-windows</TargetFramework>
  <UseWPF>true</UseWPF>
  
  <!-- Single File Publishing -->
  <PublishSingleFile>true</PublishSingleFile>
  <SelfContained>true</SelfContained>
  <RuntimeIdentifier>win-x64</RuntimeIdentifier>
  <IncludeNativeLibrariesForSelfExtract>true</IncludeNativeLibrariesForSelfExtract>
  <EnableCompressionInSingleFile>true</EnableCompressionInSingleFile>
</PropertyGroup>

<!-- WinMerge Content (External Folder) -->
<ItemGroup>
  <Content Include="WinMergePortable\**\*.*">
    <CopyToOutputDirectory>PreserveNewest</CopyToOutputDirectory>
    <CopyToPublishDirectory>PreserveNewest</CopyToPublishDirectory>
    <ExcludeFromSingleFile>true</ExcludeFromSingleFile>
  </Content>
</ItemGroup>
```

### Deployment Model: Hybrid
- **Single File**: PMXClean.exe (~65MB)
- **External Folder**: WinMergePortable\ (~38MB)
- **Total**: ~103MB

**Rationale**: WinMerge plugins/resources can't be embedded in single file.

### Deploy.ps1 Script

```powershell
param(
    [ValidateSet("SingleFile", "Standard", "Both")]
    [string]$DeploymentType = "SingleFile",
    
    [ValidateSet("Debug", "Release")]
    [string]$Configuration = "Release"
)

function Publish-Application {
    param([string]$OutputPath, [bool]$SingleFile)
    
    $publishArgs = @(
        "publish",
        "-c", $Configuration,
        "-r", "win-x64",
        "--self-contained", "true",
        "-o", $OutputPath
    )
    
    if ($SingleFile) {
        $publishArgs += "/p:PublishSingleFile=true"
    }
    
    dotnet @publishArgs
}

# Execute based on DeploymentType
# Check for WinMerge presence
# Report file sizes and counts
```

**Usage**:
```powershell
.\Deploy.ps1                    # Single file (default)
.\Deploy.ps1 -DeploymentType Standard
.\Deploy.ps1 -Configuration Debug
```

---

## Evolution Timeline

### Phase 1: Batch Script to WPF (Initial Refactoring)
**Goal**: Convert `ScriptUtility.bat` to professional WPF application

**Implemented**:
- 5-tab layout (Compare Python, Backup & Cleanup, Utility, PMX Launcher)
- WinMerge integration for Python file comparison
- Basic backup/restore operations
- File cleanup operations (JSON, Python, DLLs, retention, stubs)
- Network diagnostics
- Large file search
- Status bar for feedback

**Architecture**: Code-behind, event-driven, no MVVM

---

### Phase 2: PMX Launcher Enhancement
**Goal**: Implement all 17 PathMasterX command-line switches

**Implemented**:
- Application switches (8): offline, autoAdvance, software, freeWindow, page, size, position
- Vision switches (2): visionDebug, visionTrace
- Screen Recording switches (7): recordOnStartup, recordHighQuality, recordHighFramerate, recordMicrophone, recordWebcam, recordMaxSegments

**UI Organization**: 3 bordered sections with descriptive labels and tooltips

---

### Phase 3: WinMerge Integration & Deployment
**Goal**: Bundle WinMerge and prepare for single-file deployment

**Implemented**:
- WinMergePortable added to solution (363 files, ~38MB)
- PMXClean.csproj updated with Content inclusion and ExcludeFromSingleFile
- Single-file publishing configuration
- Deploy.ps1 script for automated builds
- Hybrid deployment model (exe + external folder)

**Result**: 65MB PMXClean.exe + 38MB WinMergePortable\ = 103MB total

**Documentation**: WINMERGE_INTEGRATION.md, DEPLOYMENT_SUCCESS.md

---

### Phase 4: Multi-Instance Backup System
**Goal**: Replace single backup folder with unlimited backup instances

**Implemented**:
- ComboBox for backup selection (sorted by LastWriteTime)
- Create/Rename/Delete backup management
- InputDialog for naming (later replaced with inline textboxes)
- Backup metadata display (created, modified, files, size)
- "Copy All Files" quick backup button
- Backup instance storage: `Backups\[BackupName]\`

**Documentation**: BACKUP_MANAGER.md, BACKUP_ENHANCEMENT_SUMMARY.md

---

### Phase 5: Dynamic Path Discovery
**Goal**: Eliminate hardcoded paths, automatically discover all PathMasterX installations

**Implemented**:
- Recursive search in Program Files (maxDepth: 4)
- Recursive search in user repositories (maxDepth: 8)
- PathMasterXInstallation class with Type and DisplayName
- InstallationType enum (ProgramFiles, UserDevelopment, Custom)
- Smart filtering (skip Public/Default users, ignore PathMasterX-LicenseGenerator)
- ComboBox-based selection with [Production] and [Dev] prefixes
- Refresh button for manual rescanning

**Documentation**: PATH_DISCOVERY.md

---

### Phase 6: UI/UX Improvements - Silent Operations
**Goal**: Eliminate all MessageBox dialogs, implement inline editing

**Implemented**:
- Removed all 28 MessageBox.Show() calls
- Status bar as sole feedback mechanism
- Inline TextBox editing for backup rename/create
- Enter/Esc/LostFocus handlers for textboxes
- Silent confirmations (no "Are you sure?" dialogs)
- Keyboard-driven workflows

**Result**: Zero modal interruptions, professional power-user experience

**Documentation**: UI_IMPROVEMENTS.md

---

### Phase 7: Header Enhancements
**Goal**: Add file version display and File Explorer integration

**Implemented**:
- FileVersionInfo reading from PVA.PathMasterX.exe
- Version display below Target Path ComboBox (light blue, 11pt italic)
- "📁 Open Folder" button to launch File Explorer
- Two-row header layout
- Automatic version update on selection change

**Documentation**: HEADER_ENHANCEMENTS.md

---

### Phase 8: Backup TextBox Fix
**Goal**: Fix new backup creation to use correct location

**Implemented**:
- Removed BackupNewNameTextBox from header
- Added BackupNewNameTextBox to Backup section (overlaying BackupComboBox)
- Updated C# to hide/show ComboBox properly
- Now matches rename behavior pattern

**Status**: Current phase (completed)

---

## Future Enhancements

### High Priority

#### 1. **Undo/Redo System**
Since operations are now silent, add undo capability:
- Track last N operations in memory
- "Undo Last Operation" button
- Support for: delete, restore, cleanup
- Not needed for: launch, compare, network checks

#### 2. **Custom Installation Paths**
Allow user to add paths not found by discovery:
- "Add Custom Path..." button
- Manual path entry with validation
- Saved to config file (JSON or XML)
- Type: `InstallationType.Custom`

#### 3. **Configuration Persistence**
Save user preferences:
- Last selected target path
- Last selected backup
- PMX launcher switch settings
- Window size/position
- Storage: JSON file in AppBaseDirectory

#### 4. **Backup Comparison**
Compare backup contents:
- "Compare with Target" button
- Shows differences (added/modified/deleted files)
- Uses WinMerge or built-in diff viewer

#### 5. **Scheduled Operations**
Background task scheduler:
- Auto-backup at specified intervals
- Cleanup old backups after N days
- Email/log notifications
- Requires Windows service or Task Scheduler integration

---

### Medium Priority

#### 6. **Extended Version Display**
Show more metadata in header:
```
File Version: 1.2.3.4567
Product Version: 1.2.3 Release
Build Date: 2025-01-15 14:32:15
Company: Precision Valve & Automation
```

#### 7. **Backup Tags/Labels**
Tag backups with custom labels:
- "Pre-Update", "Working", "Broken", "Test"
- Color-coded in ComboBox
- Filterable dropdown

#### 8. **Network Configuration Presets**
Save multiple device sets:
- "Factory Floor" (Galil, Modbus, Camera)
- "Test Lab" (different IPs)
- "Field Site A" (site-specific devices)

#### 9. **Log Viewer**
Built-in log file viewer:
- Parse PathMasterX log files
- Search/filter capabilities
- Export to CSV/JSON

#### 10. **Quick Launch Profiles**
Save PMX launcher configurations:
- "Debug Mode" (visionDebug + visionTrace + freeWindow)
- "Recording Mode" (recordOnStartup + recordHighQuality)
- "Kiosk Mode" (software + fixed size/position)

---

### Low Priority (Nice to Have)

#### 11. **Dark/Light Theme Toggle**
User-selectable color schemes

#### 12. **Multi-Language Support**
Internationalization for non-English users

#### 13. **Cloud Backup Integration**
Upload backups to OneDrive/Dropbox/Azure

#### 14. **Diff Viewer Integration**
Built-in diff viewer (instead of WinMerge dependency)

#### 15. **Command-Line Interface**
Enable scripted/automated operations:
```
PMXClean.exe --backup "MyBackup" --target "[Production]"
```

---

## Troubleshooting Guide

### Common Issues

#### **Discovery Finds No Installations**
**Symptoms**: ComboBox is empty on startup

**Causes**:
1. PathMasterX not installed
2. Installed in non-standard location
3. Executable renamed (not "PVA.PathMasterX.exe")
4. Access denied to Program Files or user repos

**Solutions**:
1. Install PathMasterX to standard location
2. Add "Custom Path" feature (future enhancement)
3. Check Debug output window for UnauthorizedAccessException
4. Run as Administrator (if access denied)

---

#### **WinMerge Not Launching**
**Symptoms**: "Error: WinMerge not found" in status bar

**Causes**:
1. WinMergePortable folder missing
2. WinMergePortable folder in wrong location
3. WinMergeU.exe missing or renamed

**Solutions**:
1. Ensure `WinMergePortable\App\WinMerge64\WinMergeU.exe` exists
2. Check Deploy.ps1 output - should say "WinMerge found: Yes"
3. Re-deploy using Deploy.ps1
4. Verify Content item in PMXClean.csproj

---

#### **Inline TextBox Won't Appear**
**Symptoms**: Clicking "New..." or "Rename..." does nothing

**Causes**:
1. Visibility not being set to Visible
2. Focus() failing (control disabled or hidden)
3. XAML overlay not configured correctly

**Solutions**:
1. Check XAML: TextBox must be in same Grid as ComboBox
2. Verify KeyDown and LostFocus handlers are wired up
3. Check Debug output for exceptions
4. Ensure Visibility.Collapsed (not Visibility.Hidden)

---

#### **Backup Creates But Doesn't Appear in ComboBox**
**Symptoms**: Status says "Created new backup" but ComboBox doesn't update

**Causes**:
1. `LoadBackupInstances()` not called after creation
2. ComboBox.SelectedItem not set to new backup name
3. Directory created but with different casing

**Solutions**:
1. Ensure `LoadBackupInstances()` is called in `CreateNewBackup()`
2. Ensure `BackupComboBox.SelectedItem = backupName;`
3. Check for case sensitivity issues (Windows is case-insensitive but .NET is case-sensitive)

---

#### **"Restore to Target" Deletes Files Instead of Overwriting**
**Symptoms**: Target has fewer files after restore

**Causes**:
1. Backup is empty or partial
2. Restore logic deletes target first (it doesn't)
3. File paths not matching correctly

**Solutions**:
1. Check backup contents before restoring
2. Verify `CopyDirectoryRecursive()` uses `File.Copy(file, targetFile, true)`
3. The third parameter (true) means "overwrite existing"
4. If files are missing, backup was incomplete

---

#### **File Version Shows "Unknown" or Error**
**Symptoms**: Version text shows "Executable not found" or "Error reading version"

**Causes**:
1. PVA.PathMasterX.exe doesn't exist at expected location
2. Executable doesn't have embedded version resources
3. Access denied to read file properties

**Solutions**:
1. Verify executable exists: `System.IO.Path.Combine(currentTargetPath, "PVA.PathMasterX.exe")`
2. Check executable properties in Windows Explorer (Details tab)
3. If version is missing, compile with version resources enabled

---

#### **Delete Operations Don't Delete All Files**
**Symptoms**: Some files remain after "Delete Python" or similar

**Causes**:
1. Files are locked (in use by another process)
2. Access denied (permissions issue)
3. Exception caught and ignored (silent failure)

**Solutions**:
1. Close PathMasterX before deleting Python files
2. Check if files are read-only
3. Add logging to `DeleteFilesByPattern()` to see which files fail:
   ```csharp
   catch (Exception ex)
   {
       Debug.WriteLine($"Failed to delete {file}: {ex.Message}");
   }
   ```

---

### Performance Issues

#### **Slow Startup (Discovery Takes > 5 seconds)**
**Causes**:
1. Deep directory trees (many levels)
2. Large number of subdirectories
3. Network drives being scanned
4. Antivirus scanning each directory access

**Solutions**:
1. Reduce maxDepth (currently 4 for Program Files, 8 for repos)
2. Add exclusions for known slow paths (e.g., OneDrive, Dropbox)
3. Cache discovery results (save to JSON, reload on startup)
4. Add "Rescan" button instead of automatic on startup

---

#### **Large File Search Takes Forever**
**Causes**:
1. Scanning entire `%USERPROFILE%` is slow
2. Many large directories (Videos, Downloads, etc.)
3. Network drives, OneDrive, or other slow paths

**Solutions**:
1. Add progress indicator (e.g., "Scanned 5,234 files...")
2. Allow user to specify root path
3. Add exclusion list (AppData, OneDrive, etc.)
4. Add "Stop" button to cancel search

---

### Debugging Tips

#### **Enable Debug Output**
Already implemented - just open Output window in Visual Studio:
- View → Output
- Show output from: Debug
- Look for `Debug.WriteLine()` messages

#### **Add Logging**
Enhance existing Debug.WriteLine() calls:
```csharp
Debug.WriteLine($"[{DateTime.Now:HH:mm:ss.fff}] SearchForExecutable: {searchPath} (depth: {currentDepth})");
```

#### **Breakpoint Locations**
Key places to set breakpoints:
1. `DiscoverPathMasterXInstallations()` - Start of discovery
2. `SearchForExecutable()` - Each directory searched
3. `InstallationAlreadyAdded()` - Duplicate prevention
4. `PopulateTargetPathComboBox()` - ComboBox population
5. Event handlers (Click events) - Verify they're being called

---

## Key Implementation Details

### Path Handling
- **Always use** `System.IO.Path.Combine()` for path construction
- **Never** hardcode backslashes or forward slashes
- **Always use** `System.IO.Path.GetRelativePath()` for relative paths
- **Always use** `System.IO.Path.GetDirectoryName()` to get directory from file path

### Exception Handling
- **Catch UnauthorizedAccessException** specifically for directory access
- **Catch Exception** for file operations
- **Always update status bar** in catch blocks
- **Never throw exceptions** - always display to user via status

### Async Patterns
- **Use async/await** for operations that might block UI (> 100ms)
- **Use Task.Run()** to offload work to background thread
- **Always await** before updating UI
- **Example**: NetworkCheck_Click, CheckLargeFiles_Click

### UI Updates
- **Always call UpdateStatus()** at start and end of operations
- **Update status bar** instead of MessageBox for all feedback
- **Use Visibility.Collapsed** (not Visibility.Hidden) for inline editing
- **Always Focus() and SelectAll()** when showing inline TextBox

---

## Critical Code Sections

### 1. Dynamic Discovery (Most Complex)
**File**: MainWindow.xaml.cs  
**Lines**: ~80-270  
**Key Methods**:
- `DiscoverPathMasterXInstallations()` - Coordinator
- `SearchProgramFiles()` - Scans Program Files
- `SearchUserRepositories()` - Scans user repos
- `SearchForPathMasterXInRepos()` - Finds PathMasterX in repos
- `SearchForExecutable()` - Recursive search with depth limit
- `InstallationAlreadyAdded()` - Duplicate prevention
- `GenerateDisplayName()` - Creates [Production] or [Dev] prefix

**Gotchas**:
- Must handle UnauthorizedAccessException silently
- Must prevent infinite recursion with maxDepth
- Must skip system users (Public, Default)
- Must distinguish between PathMasterX and PathMasterX-LicenseGenerator

---

### 2. Inline Editing (Most Unique)
**File**: MainWindow.xaml.cs  
**Lines**: ~480-620  
**Key Methods**:
- `NewBackupInstance_Click()` - Shows new backup TextBox
- `BackupNewNameTextBox_KeyDown()` - Enter/Esc handling
- `BackupNewNameTextBox_LostFocus()` - Auto-hide on focus loss
- `RenameBackup_Click()` - Shows rename TextBox
- `BackupRenameTextBox_KeyDown()` - Enter/Esc handling
- `BackupRenameTextBox_LostFocus()` - Auto-hide on focus loss

**Pattern**:
```csharp
// Show TextBox
BackupComboBox.Visibility = Visibility.Collapsed;
TextBox.Visibility = Visibility.Visible;
TextBox.Focus();
TextBox.SelectAll();

// Hide TextBox (on Enter, Esc, or LostFocus)
TextBox.Visibility = Visibility.Collapsed;
BackupComboBox.Visibility = Visibility.Visible;
```

---

### 3. File Copy Operations (Most Used)
**File**: MainWindow.xaml.cs  
**Lines**: ~1050-1120  
**Key Methods**:
- `CopyDirectoryStructure()` - Creates empty directory tree
- `CopyFilesByPattern()` - Copies matching files (preserves structure)
- `CopyDirectoryRecursive()` - Copies all files (preserves structure)

**Usage Pattern**:
```csharp
// ALWAYS create structure first
CopyDirectoryStructure(source, target);

// THEN copy files
CopyFilesByPattern(source, target, "*.py");
// OR
CopyDirectoryRecursive(source, target);
```

---

## Contact & Support

**Project Owner**: mcannon  
**Repository**: C:\Users\mcannon\source\repos\PMXClean\  
**Visual Studio Version**: 2026 Professional (18.4.2)  
**Target Framework**: .NET 10  

**For Questions**:
1. Check this document first
2. Review relevant documentation file (see File Structure)
3. Check Debug output window for errors
4. Search for similar patterns in MainWindow.xaml.cs

---

## Document Maintenance

### When to Update This Document
- After major feature additions
- After architectural changes
- When adding new dependencies
- After bug fixes that reveal design issues
- When changing deployment model

### What to Update
- Feature Implementation section (add new features)
- Evolution Timeline (add new phases)
- File Structure (if files added/removed)
- Code Patterns (if new patterns emerge)
- Troubleshooting Guide (new issues discovered)

### Version History
- **v1.0** (2025-01-15): Initial comprehensive context document
- **v2.0** (Current): Post-Phase 8 (Backup TextBox Fix)

---

## Quick Reference

### Most Important Files
1. **MainWindow.xaml.cs** - All business logic
2. **MainWindow.xaml** - All UI definition
3. **PMXClean.csproj** - Deployment configuration
4. **Deploy.ps1** - Automated deployment

### Most Important Methods
1. `DiscoverPathMasterXInstallations()` - Find all installations
2. `SearchForExecutable()` - Recursive search logic
3. `UpdateStatus()` - All user feedback
4. `CopyFilesByPattern()` - File copy operations
5. `LaunchPMX_Click()` - PMX launcher logic

### Most Important Patterns
1. **Inline Editing**: Hide ComboBox, show TextBox, Enter/Esc/LostFocus
2. **Silent Operations**: No MessageBox, status bar only
3. **Error Handling**: Try-catch with UpdateStatus()
4. **Async Operations**: Task.Run() for long operations
5. **Path Discovery**: Recursive with maxDepth and exception handling

---

**END OF DOCUMENT**

This document contains everything needed to understand, maintain, and extend PMXClean. Keep it updated as the project evolves.
