# PMX Utility Tool

A modern WPF application that replaces the `ScriptUtility.bat` batch script with a clean, user-friendly interface.

## Features

### 1. **Compare Python**
- **Compare Installed**: Copies Python files from the target path to a `target` folder and launches WinMerge to compare with the `master` folder
- **Pull Fresh Master**: Copies Python files from the target path to a `master` folder for future comparisons

### 2. **Backup & Cleanup**
A unified tab with two columns for managing backups and cleanup operations:

#### Backup Manager (Left Column)
**Multi-Instance Backup System** - Create and manage multiple named backups:

- **Backup Selection**: ComboBox to select from existing backups
- **Management Buttons**:
  - **New...**: Create a new named backup instance
  - **Rename...**: Rename the selected backup
  - **Delete**: Permanently delete the selected backup
- **Backup Info**: Displays creation date, modification date, file count, and total size
- **Backup Operations**:
  - **Copy All Files**: Backup entire target directory (NEW!)
  - **Copy JSON**: Backs up all `.json` files
  - **Copy Retention**: Backs up all `.retention` files
  - **Copy Python**: Backs up all `.py` files
  - **Copy DLLs**: Backs up all `.DLL` files
  - **Copy Page Stubs**: Backs up all `.stub` files
  - **Restore to Target**: Restores selected backup to target path

All backups are stored in `Backups\[BackupName]\` folders for easy organization.

#### Cleanup (Right Column)
- **Delete JSON**: Removes all `.json` files from the target path
- **Delete Retention**: Removes all `.retention` files from the target path
- **Delete Python**: Removes all `.py` files from the target path
- **Delete Page Stubs**: Removes all `.stub` files from the target path

⚠️ **Warning**: All cleanup operations are irreversible!

### 3. **Utility**
- **Check Network Settings**: Displays network configuration and pings:
  - Galil (100.100.100.101)
  - Modbus I/O (100.100.100.110)
  - Camera (200.200.200.201)
- **Check for Large Files**: Searches for files larger than 200MB in the user profile directory

### 4. **PMX Launcher**
Launch PathMasterX with various command-line options organized into three categories:

#### Application Options
- **Offline Mode** (`-offline`): Start the application with offline mode checked by default
- **Auto-Accept Prompts** (`-autoAdvance`): Automatically confirm startup dialogs
- **Software Only Rendering** (`-software`): Start the application with "Software only" rendering
- **Free Window** (`-freeWindow`): Start the application with a movable, resizable window
- **Start Page** (`-page:[name]`): Start the application and immediately navigate to the specified page
- **Window Size** (`-size:[width]:[height]`): Set the width and height of the application in pixels
- **Window Position** (`-position:[X]:[Y]`): Set the position of the application in pixels from the top left corner

#### Vision Options
- **Vision Debug** (`-visionDebug`): Begin the application with verbose vision error reporting
- **Vision Trace** (`-visionTrace`): Begin the application with external vision tracing enabled

#### Screen Recording Options
- **Record On Startup** (`-recordOnStartup`): Start recording during startup
- **Record High Quality** (`-recordHighQuality`): Record in High Quality
- **Record High Framerate** (`-recordHighFramerate`): Record at 30 FPS
- **Record Microphone** (`-recordMicrophone`): Record Microphone audio
- **Record Webcam** (`-recordWebcam`): Record Webcam feed
- **Max Recording Segments** (`-recordMaxSegments:[maxSegments]`): Set the maximum number of consecutive 30 minute segments

## Path Configuration

The application supports two paths:
- **Default Path**: `C:\Program Files\PVA\PathMasterX\`
- **Alternate Path**: `%USERPROFILE%\source\repos\precisionvalve\PathMasterX\PathMasterX\bin\x64\Debug\net8.0-windows\`

Use the **Swap Path** button to toggle between paths if both exist.

## Requirements

- Windows 10 or later
- .NET 10 (included in self-contained deployment)
- WinMerge Portable is bundled with the application for Python comparison features

## Deployment

### Single-File Deployment (Recommended)
The application is configured for hybrid single-file deployment:

```powershell
# Publish as single-file executable with external WinMerge
dotnet publish -c Release -r win-x64 --self-contained true /p:PublishSingleFile=true

# Or use the deployment script
.\Deploy.ps1 -DeploymentType SingleFile -Configuration Release
```

**Output structure:**
- `PMXClean.exe` - 65MB single-file executable (includes .NET 10 runtime)
- `WinMergePortable\` - 38MB folder with 363 files (must remain external)
- Total: ~103MB

**Why WinMerge is external:** WinMerge requires its files to remain as separate files for plugins, language packs, and file associations to work correctly.

### Standard Deployment
For standard deployment without single-file packaging:

```powershell
dotnet publish -c Release -r win-x64 --self-contained true

# Or use the deployment script
.\Deploy.ps1 -DeploymentType Standard -Configuration Release
```

The WinMergePortable folder and all application files will be in the publish directory.

## Usage

1. Launch the application (PMXClean.exe)
2. Verify the correct target path is displayed
3. Navigate through the tabs to access different features
4. Click buttons to perform operations
5. Monitor the status bar for operation feedback

## WinMerge Integration

WinMerge Portable is bundled within the solution at `WinMergePortable\App\WinMerge64\WinMergeU.exe`. The application automatically:
- Validates WinMerge presence on startup
- Uses the bundled version for all comparison operations
- Shows a warning if WinMerge is not found (but continues to work for other features)

When deployed as a single-file, WinMerge files are extracted to the application's base directory automatically.

## Advantages over Batch Script

- ✅ Modern, intuitive graphical interface
- ✅ Organized two-column layout for related operations (Backup & Cleanup)
- ✅ Color-coded sections (green for backup, red for cleanup)
- ✅ Real-time status updates
- ✅ Confirmation dialogs for destructive operations
- ✅ Asynchronous operations (no UI freezing)
- ✅ Better error handling and reporting
- ✅ More maintainable C# code
- ✅ Bundled WinMerge for easy deployment
- ✅ Single-file deployment option

## Migration Notes

This WPF application replicates all functionality from `ScriptUtility.bat`:
- All menu options have been converted to tabs and buttons
- Backup and Cleanup combined into single tab with two columns for better workflow
- All file operations maintain the same behavior
- Network checks provide the same information
- PMX launcher supports all original command-line arguments
- Path swapping functionality is preserved

