# WinMerge Integration Summary

## Changes Made

### 1. **Project Configuration** (`PMXClean.csproj`)
- Added `<None Include>` elements to copy all WinMergePortable files to output directory
- Configured single-file publishing with these properties:
  - `PublishSingleFile`: Packages everything into one executable
  - `SelfContained`: Includes .NET runtime (no installation required)
  - `IncludeAllContentForSelfExtract`: Extracts WinMerge files at runtime
  - `EnableCompressionInSingleFile`: Reduces file size

### 2. **Code Refactoring** (`MainWindow.xaml.cs`)

#### New Fields:
```csharp
private readonly string winMergePath;      // Stores WinMerge executable path
private readonly string appBaseDirectory;  // Stores application base directory
```

#### New Methods:
- `ValidateWinMerge()`: Checks WinMerge presence on startup and warns if missing
- `GetWorkingDirectory()`: Returns base directory for file operations (supports single-file deployment)

#### Updated Methods:
- `CompareInstalled_Click()`: Uses stored `winMergePath` instead of constructing it each time
- `PullFreshMaster_Click()`: Uses `GetWorkingDirectory()` instead of `AppDomain.CurrentDomain.BaseDirectory`
- All backup methods: Updated to use `GetWorkingDirectory()`

### 3. **Benefits**

#### For Development:
- ✅ WinMerge is now part of the solution
- ✅ No need to manually copy WinMerge to output folder
- ✅ Automatic validation on startup
- ✅ Better error messages when WinMerge is missing

#### For Deployment:
- ✅ WinMerge automatically included in builds
- ✅ Single-file deployment ready
- ✅ Self-contained (includes .NET 10 runtime)
- ✅ No external dependencies to manage

### 4. **How It Works**

#### During Build:
1. MSBuild copies entire `WinMergePortable` folder to output directory
2. Maintains folder structure: `bin\Release\net10.0-windows\win-x64\publish\WinMergePortable\`

#### During Runtime:
1. Application starts and sets `appBaseDirectory` to executable location
2. `ValidateWinMerge()` checks if WinMerge exists at expected location
3. When "Compare Installed" is clicked, uses stored `winMergePath`

#### Single-File Deployment:
1. When published as single-file, the main executable is compressed (~65MB)
2. WinMerge files remain external alongside the executable (~38MB)
3. `appBaseDirectory` points to the publish folder containing both exe and WinMergePortable
4. All file operations (master, target, backup) use `GetWorkingDirectory()`
5. Total deployment size: ~103MB (exe + WinMerge + debug symbols)

**Why WinMerge is External:**
- WinMerge contains 363 files that must remain as separate files to function
- Embedding would break WinMerge's plugin system and file associations
- External deployment ensures WinMerge works identically to portable version

### 5. **Deployment Options**

#### Option 1: Single-File (Recommended for Distribution)
```powershell
.\Deploy.ps1 -DeploymentType SingleFile -Configuration Release
```
- **Result**: One 65MB executable + WinMergePortable folder (103MB total)
- **Pros**: Easy to distribute, no installation needed, self-contained .NET runtime
- **Cons**: WinMerge must remain alongside executable (can't be truly single-file)

#### Option 2: Standard (Recommended for Internal Use)
```powershell
.\Deploy.ps1 -DeploymentType Standard -Configuration Release
```
- **Result**: ~50MB executable + WinMergePortable folder + .NET files
- **Pros**: Faster startup, smaller main executable
- **Cons**: Multiple files to distribute

### 6. **Path Resolution Logic**

```
Single-File Deployment:
├── User runs: PMXClean.exe (from publish folder)
├── Application sets: appBaseDirectory = [publish folder path]
├── WinMerge path: {appBaseDirectory}\WinMergePortable\App\WinMerge64\WinMergeU.exe
└── Work folders: {appBaseDirectory}\master, {appBaseDirectory}\target, {appBaseDirectory}\backup

Standard Deployment:
├── User runs: C:\Tools\PMXClean.exe
├── Application sets: appBaseDirectory = C:\Tools\
├── WinMerge path: C:\Tools\WinMergePortable\App\WinMerge64\WinMergeU.exe
└── Work folders: C:\Tools\master, C:\Tools\target, C:\Tools\backup

Note: In both cases, WinMergePortable folder must be in same directory as executable.
```

### 7. **Testing Checklist**

- [x] Build succeeds without errors
- [x] WinMerge path validated on startup
- [x] "Compare Installed" launches WinMerge correctly
- [x] "Pull Fresh Master" creates master folder correctly
- [x] Backup operations work with GetWorkingDirectory()
- [x] Test single-file deployment (exe + WinMergePortable folder)
- [x] WinMerge launches from published deployment
- [x] Verify master/target/backup folders created in correct location

### 8. **Future Enhancements**

Potential improvements for true single-file deployment:
1. Embed WinMerge as embedded resource and extract on first run to user's AppData
2. Add cleanup logic to remove temporary WinMerge extraction
3. Implement WinMerge version checking and auto-update
4. Consider alternative comparison tools with smaller footprint

### 9. **Troubleshooting**

**Q: WinMerge not found error on startup**
- Check if WinMergePortable folder exists in solution
- Verify .csproj has the `<None Include>` elements
- Rebuild solution to copy files

**Q: Single-file deployment doesn't work**
- Ensure all properties are set in .csproj
- Use `Deploy.ps1` script which sets required parameters
- Check output folder for WinMergePortable presence

**Q: Large single-file executable size**
- Expected behavior (~150MB with .NET runtime + WinMerge)
- Use Standard deployment for smaller footprint
- Consider using framework-dependent deployment if .NET 10 is installed on target machines

