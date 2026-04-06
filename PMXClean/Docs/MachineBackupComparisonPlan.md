# .machine Backup Comparison Feature - Implementation Plan

## Overview
This document outlines the findings from analyzing the BackupExamples folders and proposes an implementation plan for extending the comparison tool to support .machine file backups.

---

## Key Insights from Backup Analysis

### 1. Backup File Structure

**.machine files are renamed ZIP archives** containing a folder structure that mirrors the PathMaster X installation.

**Root-level structure:**
```
<BackupRoot>/
├── Headers.data           # Version info (pipe-delimited)
├── IsFullBackup           # Optional marker file (0 bytes) - only in full backups
├── Base/
│   ├── Core/
│   │   ├── Functions/     # Python files (.py)
│   │   ├── Favorites/     # JSON configuration
│   │   ├── Localization/  # .culture files
│   │   └── Logs/          # Only in full backups (.log files)
│   └── UI/
├── Device/                # Device configurations
│   ├── Actuator/
│   ├── Barcode/
│   ├── Camera/
│   ├── Controller/
│   └── ... (16 device types)
└── Feature/               # Feature modules
    ├── Communication/
    ├── Dashboard/
    ├── Inspection/        # Only in full backups (v1.3.0.0+)
    ├── Process/
    ├── Product/
    ├── Program/
    ├── ShotScale/
    ├── SprayWidth/
    ├── Tool/
    └── Trigger/
```

### 2. Headers.data Format

Pipe-delimited version information with format: `ModuleName|VersionNumber|RelativePath`

**Example (Regular Backup - v1.2.0.1):**
```
Triggers|1.2.0.1|.\Feature\Trigger
Process|1.2.0.1|.\Feature\Process
...
Core|1.2.0.1|.\Base\Core
```

**Example (Full Backup - v1.3.0.0):**
```
Triggers|1.3.0.0|.\Feature\Trigger
...
Inspections|1.3.0.0|.\Feature\Inspection    ← New module in newer version
...
```

**Key observations:**
- All modules typically share the same version number within a backup
- Module order varies between backups (not alphabetical)
- 27-28 modules typically present
- Newer versions may have additional modules (e.g., "Inspections")

### 3. Regular vs Full Backup Differences

| Aspect | Regular Backup | Full Backup |
|--------|----------------|-------------|
| IsFullBackup marker | ❌ Not present | ✅ Present (0 bytes) |
| Log files (.log) | ❌ Not included | ✅ Included in Base/Core/Logs/ |
| File count | ~1,200 files | ~1,450 files |
| Python files | ~562 .py files | ~700 .py files |
| Product files | 2 .product files | 59 .product files |
| Database (.db) | ❌ Not included | ⚠️ Only Thumbs.db (Windows cache) |

**Notable extra content in Full Backups:**
- Application logs (dated .log files)
- More product definitions
- Inspection module (version-dependent)
- .mca, .retention files
- More .mim, .mpat files

### 4. File Types in Backups

| Extension | Description | Count (Regular) | Count (Full) |
|-----------|-------------|-----------------|--------------|
| .py | Python scripts | 562 | 700 |
| .culture | Localization files | 140 | 140 |
| .step | Trigger step definitions | 114 | 70 |
| .png | Image assets | 110 | 115 |
| .lane | Lane configurations | 106 | 64 |
| .stub | Stub files | 52 | 54 |
| .json | JSON configurations | 34 | 41 |
| .trigger | Trigger definitions | 20 | 21 |
| .rtos | RTOS configs | 18 | 22 |
| .txt | Text files | 16 | 12 |
| .mim | MIM files | 8 | 29 |
| .MPAT/.mpat | Pattern files | 6 | 28 |
| .product | Product definitions | 2 | 59 |
| .log | Log files | 0 | 8 |

### 5. Custom DLL Detection (Underscore Prefix)

**Finding:** No DLLs were found in either backup example. However, the user specified that:
- DLLs starting with `_` (underscore) are **custom/customizable implementations**
- These should be tracked and highlighted as important customizations

**Implication:** Need to add logic to detect and flag `_*.dll` files when present in .machine backups.

### 6. JSON File Structure

JSON files have a versioned header format:
```json
Version: 1.1.0.0
{"$type":"ObservableCollection`1[[System.String, ...]], System.ObjectModel","$values":["..."]}
```

The version on line 1 is separate from the JSON content that starts on line 2.

---

## Implementation Plan - Bullet-Pointed Instructions

### Phase 1: Core Infrastructure

1. **Create MachineBackupService class** (new file: `PMXClean/Services/MachineBackupService.cs`)
   - [ ] Add method to extract .machine ZIP to temporary folder
   - [ ] Add method to parse Headers.data file
   - [ ] Add method to detect IsFullBackup marker
   - [ ] Add method to find underscore-prefixed DLLs
   - [ ] Add method to clean up temporary extraction folder
   - [ ] Add method to identify backup version from Headers.data

2. **Create backup-related models** (new file: `PMXClean/Models/MachineBackupInfo.cs`)
   - [ ] Create `MachineBackupInfo` record with properties:
     - `FilePath` (string) - Original .machine file path
     - `ExtractedPath` (string) - Temp extraction location
     - `IsFullBackup` (bool) - Whether IsFullBackup marker exists
     - `BackupVersion` (string) - Version from Headers.data
     - `Modules` (list) - Parsed module info from Headers.data
     - `CustomDlls` (list) - List of underscore-prefixed DLLs found
   - [ ] Create `BackupModuleInfo` record:
     - `Name` (string)
     - `Version` (string)
     - `RelativePath` (string)

### Phase 2: UI Changes

3. **Update ComparisonViewModel** (`PMXClean/ViewModels/ComparisonViewModel.cs`)
   - [ ] Add `MachineBackupInfo? LoadedBackup` property
   - [ ] Add `BackupComparisonMode` enum (InstalledVsVersion, BackupVsVersion, BackupVsInstalled)
   - [ ] Add `ComparisonMode` property to track current mode
   - [ ] Add `LoadMachineBackupCommand` to load/extract .machine file
   - [ ] Add `BackupInfoText` property to display backup details
   - [ ] Modify `CompareAsync` to support backup as a comparison source
   - [ ] Add `ClearBackupCommand` to unload backup and clean up temp files

4. **Update MainWindow.xaml** - Compare Python Tab
   - [ ] Add "Load Backup" button next to version dropdown
   - [ ] Add visual indicator when backup is loaded (badge/icon)
   - [ ] Add backup info display card (shows version, full/regular, module count)
   - [ ] Add radio buttons or toggle for comparison mode:
     - "Compare: Installed ↔ Version" (existing)
     - "Compare: Backup ↔ Version"
     - "Compare: Backup ↔ Installed"
   - [ ] Add button to clear/unload backup
   - [ ] Add custom DLL warning indicator (if any found)

5. **Add file picker integration**
   - [ ] Implement OpenFileDialog for .machine files
   - [ ] Filter to show only *.machine files
   - [ ] Default to common backup locations if known

### Phase 3: Comparison Logic Enhancement

6. **Extend PythonComparisonService** (`PMXClean/Services/PythonComparisonService.cs`)
   - [ ] Modify `CompareDirectories` to accept optional filter for file types (not just .py)
   - [ ] Add comparison statistics per module (using Headers.data paths)
   - [ ] Consider adding comparison support for .json, .trigger, .step files

7. **Add module-level comparison summary**
   - [ ] Create `ModuleComparisonResult` model
   - [ ] Calculate differences per module (using paths from Headers.data)
   - [ ] Display module-by-module summary in UI

### Phase 4: Display Enhancements

8. **Add backup-specific status indicators**
   - [ ] Add icon/indicator for full vs regular backup
   - [ ] Highlight custom DLLs with warning icon
   - [ ] Show module version mismatches prominently
   - [ ] Add tooltip showing Headers.data version for each module

9. **Add comparison summary card**
   - [ ] Show backup version vs target version
   - [ ] List modules with version differences
   - [ ] Show count of files unique to backup (customizations)
   - [ ] Highlight any missing modules between versions

### Phase 5: Cleanup & Polish

10. **Implement temp folder management**
    - [ ] Auto-cleanup extracted backup on application close
    - [ ] Add `IDisposable` pattern to `MachineBackupInfo`
    - [ ] Handle scenarios where temp folder cleanup fails

11. **Add error handling**
    - [ ] Handle corrupted/invalid .machine files
    - [ ] Handle missing Headers.data
    - [ ] Handle ZIP extraction errors
    - [ ] Show user-friendly error messages

12. **Testing considerations**
    - [ ] Test with both RegularBackupExample and FullBackupExample
    - [ ] Test comparison against multiple installed versions
    - [ ] Verify custom DLL detection works (when DLLs are present)
    - [ ] Test cleanup on unexpected application termination

---

## Questions for User Review

1. **File type comparison scope:** Should the comparison include only .py files (current behavior) or expand to include .json, .trigger, .step, .culture files?

2. **Comparison modes priority:** Which comparison mode is most important?
   - Backup ↔ Defined Version (see what changed from a known release)
   - Backup ↔ Installed (see differences from current machine state)

3. **Custom DLL handling:** When underscore-prefixed DLLs are found, what action should be taken?
   - Just display a warning/list?
   - Provide option to copy them somewhere?
   - Compare against installed DLLs?

4. **Module-level grouping:** Should the comparison tree be organized by module (from Headers.data) or maintain the current folder-based view?

5. **Multiple backup comparison:** Should the tool support comparing two .machine files against each other (e.g., comparing backups from different dates)?

6. **Backup history:** Should the tool remember recently loaded .machine files for quick re-loading?

---

## Technical Notes

- .machine files are standard ZIP archives - use `System.IO.Compression.ZipFile`
- Temp folder should use `Path.GetTempPath()` with unique subfolder
- Headers.data parsing: simple `string.Split('|')` per line
- Consider lazy extraction - only extract when comparison starts
- IsFullBackup check: `File.Exists(Path.Combine(extractPath, "IsFullBackup"))`

---

## File Changes Summary

| File | Action | Purpose |
|------|--------|---------|
| `Services/MachineBackupService.cs` | CREATE | Backup extraction and parsing logic |
| `Models/MachineBackupInfo.cs` | CREATE | Backup info models |
| `ViewModels/ComparisonViewModel.cs` | MODIFY | Add backup loading and mode support |
| `MainWindow.xaml` | MODIFY | Add backup UI controls |
| `Converters/Converters.cs` | MODIFY | Add any new converters if needed |

---

*Document created for review before implementation. Please edit/approve before code changes begin.*
