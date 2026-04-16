# PMXClean Next Steps - Detailed Implementation Plan

---

- Target remote pc for queries in powershell instead of only local checks
- Also add ability to run the powershell script in the PathMaster X target location and gather the output

## 4. Rework Deploy Script for Single-File Deployment

**Current State:** `Deploy.ps1` publishes both single-file and standard builds, outputs to `bin\Release\net10.0-windows\win-x64\publish`.

**Goal:** Optimize for single-file deployment workflow.

### Implementation Approach

- [ ] **4.1 Analyze current issues**
  - WinMerge dependency is external (checked but not bundled)
  - Both build types go to same output path (overwrite risk)
  - No version tagging or artifact naming

- [ ] **4.2 Update Deploy.ps1**
  - Default to single-file only (remove 'Both' as default)
  - Add version extraction from `.csproj` or AssemblyInfo
  - Create versioned output folder: `publish\PMXClean_v{version}\`
  - Add option to include WinMerge in extraction (if using it)
  - Add artifact naming: `PMXClean_{version}_{date}.exe`

- [ ] **4.3 Optimize single-file settings in .csproj**
  - Verify `<PublishSingleFile>true</PublishSingleFile>`
  - Consider `<PublishTrimmed>true</PublishTrimmed>` for smaller size
  - Add `<IncludeNativeLibrariesForSelfExtract>true</IncludeNativeLibrariesForSelfExtract>`
  - Test `<EnableCompressionInSingleFile>true</EnableCompressionInSingleFile>` impact

- [ ] **4.4 Add GitHub release script**
  - Optional: Add script section to create GitHub release with artifact
  - Use `gh release create` if GitHub CLI is available

---

## 6. Ultimate Goal: Ahead-Version Locked File Guidance

**Current State:** Can compare locked files against specific PMXVersion, showing diff.

**Goal:** When user's installed version is BEHIND our latest PMXVersion, show what changes they need to make to their locked files to upgrade.

### Implementation Approach

- [ ] **6.1 Determine version ordering**
  - Parse version strings (e.g., "1.2.3.4") into comparable Version objects
  - Sort PMXVersions to identify "ahead" versions relative to backup/installation
  - Identify which version the user has (from backup Headers.data or installation)

- [ ] **6.2 Create `UpgradeGuidanceService.cs`**
  - Input: User's current locked file content, source version, target version
  - Find the file in both PMXVersions/{sourceVersion} and PMXVersions/{targetVersion}
  - Generate diff showing what changed between versions
  - For locked files: highlight which lines user needs to manually update

- [ ] **6.3 Create upgrade guidance model**
  - `LockedFileUpgradeInfo`:
	- FileName, RelativePath
	- CurrentVersion, TargetVersion
	- RequiredChanges (list of diff hunks)
	- IsBlocker (true if locked lines changed)
	- SuggestedAction (text guidance)

- [ ] **6.4 Implement UI**
  - "Upgrade Analysis" view/tab
  - Select source version (or auto-detect from backup)
  - Select target version (defaults to latest available)
  - Show list of locked files with change indicators:
	- ✓ Green: No changes needed (locked content identical)
	- ⚠ Yellow: Changes needed in non-locked sections
	- ✗ Red: Changes needed in locked sections (manual intervention required)
  - Click file to see detailed diff with guidance annotations

- [ ] **6.5 Generate actionable guidance**
  - For each locked file with changes:
	- Show "Before" (their locked version) and "After" (target version)
	- Highlight exactly which `#lock` sections have changes
	- Provide copy-paste ready code snippets for manual updates
	- Include context lines to help locate the section

---
