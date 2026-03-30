# PowerShell Script Integration for Python Version Management

## Overview

Instead of using the GUI to download Python versions, you can now use a **PowerShell script** that integrates with your build process. This script downloads Python files from PathMasterX GitHub releases directly into the `PMXClean\PMXVersions\` folder, making them part of your source code repository.

---

## Key Differences from GUI Approach

| Feature | GUI (GitHubReleasesWindow) | PowerShell Script |
|---------|---------------------------|-------------------|
| Location | Downloads to external folder | Downloads to `PMXClean\PMXVersions\` |
| Git Integration | Not tracked | **Files committed to Git** |
| Automation | Manual clicks | **Scriptable/CI-friendly** |
| Build Integration | No | **Yes** (Pre-build, MSBuild target) |
| Speed | Interactive | Fast, batch-friendly |
| Use Case | Ad-hoc comparison | Version control, automation |

---

## The PowerShell Script

### Location

```
C:\Users\Michael\source\repos\SajuukKahn\PMXClean\UpdatePythonVersions.ps1
```

### What It Does

1. **Fetches releases** from `precisionvalve/PathMasterX` via GitHub API
2. **Downloads** release source archives (zipballs)
3. **Extracts** only Python files (`.py`)
4. **Excludes** the `lib/` directory
5. **Saves** to `PMXClean\PMXVersions\[tag-name]\`
6. **Updates** `Versions.md` with metadata
7. **Skips** already-downloaded versions (unless `-Force`)

---

## Usage

### Basic Usage

From the solution root directory:

```powershell
.\UpdatePythonVersions.ps1
```

Output:
```
========================================
PathMasterX Python Version Updater
========================================

Fetching releases from https://api.github.com/repos/precisionvalve/PathMasterX/releases...
Found 15 releases

Processing release: v2.0.0
  Downloading archive...
  Extracting Python files...
  ✓ Extracted 47 Python files

Processing release: v2.1.0
  ✓ Already exists (47 files). Use -Force to re-download.

...

========================================
Update Complete!
========================================
Success: 10
Skipped: 5
Failed:  0

Versions directory: C:\...\PMXClean\PMXVersions

⚠ Don't forget to commit the updated files to Git!
```

### Download Specific Versions

```powershell
.\UpdatePythonVersions.ps1 -Releases "v2.0.0,v2.1.0,v2.2.0"
```

### Force Re-download

```powershell
.\UpdatePythonVersions.ps1 -Force
```

Re-downloads all versions, overwriting existing files.

### With GitHub Token (Private Repo)

Set environment variable:
```powershell
$env:GITHUB_TOKEN = "ghp_yourpersonalaccesstoken"
.\UpdatePythonVersions.ps1
```

Or pass as parameter:
```powershell
.\UpdatePythonVersions.ps1 -Token "ghp_yourpersonalaccesstoken"
```

---

## Integration Options

### 1. Manual Execution

Run whenever you need updated versions:

```powershell
cd C:\Users\Michael\source\repos\SajuukKahn\PMXClean
.\UpdatePythonVersions.ps1
git add PMXClean\PMXVersions
git commit -m "Update Python versions"
git push
```

**Recommended for**: Local development, occasional updates

---

### 2. Visual Studio External Tool

Add to **Tools** menu for easy access:

1. **Tools** → **External Tools...**
2. Click **Add**
3. Configure:
   - **Title**: `Update Python Versions`
   - **Command**: `powershell.exe`
   - **Arguments**: `-ExecutionPolicy Bypass -File "$(SolutionDir)UpdatePythonVersions.ps1"`
   - **Initial directory**: `$(SolutionDir)`
   - **Use Output window**: ✅ Checked

4. Click **OK**

Now you can run: **Tools** → **Update Python Versions**

**Recommended for**: Developers who want a menu option

---

### 3. Pre-Build Event (MSBuild)

Add to `PMXClean.csproj` in a `<PropertyGroup>`:

```xml
<PreBuildEvent>powershell -ExecutionPolicy Bypass -File "$(SolutionDir)UpdatePythonVersions.ps1"</PreBuildEvent>
```

**⚠ Warning**: This runs on EVERY build and can slow down compilation.

**Recommended for**: CI/CD builds only

---

### 4. Custom MSBuild Target (Conditional)

Use the provided `MSBuild.Integration.targets` file:

#### Option A: Release Builds Only

Add to `PMXClean.csproj` before `</Project>`:

```xml
<Target Name="UpdatePythonVersions" BeforeTargets="BeforeBuild" Condition="'$(Configuration)' == 'Release'">
  <Message Importance="high" Text="Updating Python versions from GitHub..." />
  <Exec Command="powershell -ExecutionPolicy Bypass -File &quot;$(SolutionDir)UpdatePythonVersions.ps1&quot;" 
        IgnoreExitCode="true" 
        ContinueOnError="true" />
</Target>
```

#### Option B: On-Demand via Environment Variable

```xml
<Target Name="UpdatePythonVersionsOnDemand" BeforeTargets="BeforeBuild" Condition="'$(UPDATE_PYTHON_VERSIONS)' == '1'">
  <Message Importance="high" Text="Updating Python versions from GitHub (on-demand)..." />
  <Exec Command="powershell -ExecutionPolicy Bypass -File &quot;$(SolutionDir)UpdatePythonVersions.ps1&quot;" />
</Target>
```

Usage:
```powershell
$env:UPDATE_PYTHON_VERSIONS = "1"
dotnet build
```

#### Option C: CI/CD Only

```xml
<Target Name="UpdatePythonVersionsCI" BeforeTargets="BeforeBuild" Condition="'$(CI)' == 'true' AND '$(Configuration)' == 'Release'">
  <Message Importance="high" Text="Updating Python versions from GitHub (CI build)..." />
  <Exec Command="powershell -ExecutionPolicy Bypass -File &quot;$(SolutionDir)UpdatePythonVersions.ps1&quot; -Token $(GITHUB_TOKEN)" />
</Target>
```

**Recommended for**: Advanced users, CI/CD pipelines

---

### 5. CI/CD Pipeline Integration

#### Azure DevOps

```yaml
steps:
- task: PowerShell@2
  displayName: 'Update Python Versions'
  inputs:
    filePath: 'UpdatePythonVersions.ps1'
    arguments: '-Token $(GitHubToken)'
    workingDirectory: '$(Build.SourcesDirectory)'
    
- task: CmdLine@2
  displayName: 'Commit updated versions'
  inputs:
    script: |
      git config user.name "Build Agent"
      git config user.email "build@pmxclean.local"
      git add PMXClean/PMXVersions
      git commit -m "Update Python versions [skip ci]"
      git push
```

#### GitHub Actions

```yaml
- name: Update Python Versions
  run: |
    pwsh -File UpdatePythonVersions.ps1 -Token ${{ secrets.GITHUB_TOKEN }}
  
- name: Commit changes
  run: |
    git config user.name "GitHub Actions"
    git config user.email "actions@github.com"
    git add PMXClean/PMXVersions
    git commit -m "Update Python versions" || echo "No changes"
    git push
```

**Recommended for**: Automated builds, continuous deployment

---

## File Structure After Running

```
PMXClean/
├── PMXVersions/
│   ├── Versions.md              # Auto-updated metadata
│   ├── v1.0.0/
│   │   ├── [Python files]       # Excluding lib/
│   │   └── [Directory structure preserved]
│   ├── v2.0.0/
│   │   └── ...
│   ├── v2.1.0/
│   │   └── ...
│   └── ...
└── UpdatePythonVersions.ps1     # At solution root
```

---

## Git Workflow

### After Running Script

```powershell
# 1. Run script
.\UpdatePythonVersions.ps1

# 2. Check what changed
git status

# 3. Review changes
git diff PMXClean/PMXVersions/Versions.md

# 4. Stage changes
git add PMXClean/PMXVersions

# 5. Commit
git commit -m "feat: Update Python versions (v2.0.0, v2.1.0)"

# 6. Push
git push origin master
```

### .gitignore Considerations

**Do NOT** add `PMXVersions/` to `.gitignore`. These files **should be committed** to version control.

However, you may want to ignore temporary files:

```gitignore
# Ignore temp downloads
*.zip

# But keep Python versions
!PMXClean/PMXVersions/**/*.py
!PMXClean/PMXVersions/Versions.md
```

---

## Script Parameters

### -Releases

**Type**: String  
**Default**: Empty (downloads all)  
**Format**: Comma-separated tags

**Example**:
```powershell
.\UpdatePythonVersions.ps1 -Releases "v2.0.0,v2.1.0"
```

### -Token

**Type**: String  
**Default**: `$env:GITHUB_TOKEN`  
**Purpose**: GitHub Personal Access Token

**When needed**:
- Private repositories
- Avoid rate limits (60 → 5000 requests/hour)

**Example**:
```powershell
.\UpdatePythonVersions.ps1 -Token "ghp_abc123..."
```

### -Force

**Type**: Switch  
**Default**: False  
**Purpose**: Re-download existing versions

**Example**:
```powershell
.\UpdatePythonVersions.ps1 -Force
```

---

## Troubleshooting

### Script Execution Policy Error

```
... cannot be loaded because running scripts is disabled on this system.
```

**Solution**:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Or run with bypass:
```powershell
powershell -ExecutionPolicy Bypass -File UpdatePythonVersions.ps1
```

### API Rate Limit Exceeded

```
Error fetching releases: API rate limit exceeded
```

**Solution**: Use a GitHub token:
```powershell
.\UpdatePythonVersions.ps1 -Token "ghp_yourtoken"
```

### 404 Repository Not Found

```
Error fetching releases: Repository not found
```

**Causes**:
- Repository is private (requires token)
- Owner/repo name is incorrect
- Repository doesn't exist

**Solution**: Verify repository URL and use token for private repos

### No Python Files Found

```
✗ No Python files found
```

**Causes**:
- Release doesn't contain Python code
- All Python files are in `lib/` (excluded)

**Solution**: Verify release contains Python files outside `lib/` directory

---

## Comparison: GUI vs Script

### When to Use GUI (GitHubReleasesWindow)

✅ **Good for**:
- One-time downloads
- Exploring available releases
- Visual selection
- Occasional use

❌ **Not good for**:
- Automation
- Version control
- Build integration
- Batch operations

### When to Use Script (UpdatePythonVersions.ps1)

✅ **Good for**:
- Version-controlled Python files
- Build automation
- CI/CD pipelines
- Batch updates
- Scripted workflows

❌ **Not good for**:
- Users uncomfortable with PowerShell
- Quick one-off downloads (GUI is faster)

---

## Advanced Usage

### Download Only Releases (No Pre-releases)

The script currently downloads all releases. To filter, modify the script or use `-Releases` parameter:

```powershell
# Get only non-prerelease tags
$releases = (Invoke-RestMethod -Uri "https://api.github.com/repos/precisionvalve/PathMasterX/releases").tag_name | Where-Object { $_ -match '^v\d+\.\d+\.\d+$' }
.\UpdatePythonVersions.ps1 -Releases ($releases -join ',')
```

### Schedule Regular Updates

Windows Task Scheduler:

1. **Create Task**
2. **Trigger**: Daily at 2 AM
3. **Action**: Start a program
   - Program: `powershell.exe`
   - Arguments: `-ExecutionPolicy Bypass -File "C:\...\UpdatePythonVersions.ps1"`
   - Start in: `C:\...\PMXClean`

### Notification on Completion

Add to end of script:

```powershell
# Send email notification
Send-MailMessage -To "dev@example.com" -From "build@example.com" `
    -Subject "Python Versions Updated" -Body "Success: $successCount versions"
```

---

## Summary

The PowerShell script approach provides:

- ✅ **Version Control**: Python files are part of your repository
- ✅ **Automation**: Integrates with build systems
- ✅ **Consistency**: Same versions across all developers
- ✅ **Traceability**: Git history shows when versions changed
- ✅ **CI/CD Ready**: Works in automated pipelines

**Recommended Workflow**:
1. Run script manually or via CI/CD
2. Commit updated `PMXVersions/` to Git
3. All developers pull latest versions
4. Use WinMerge to compare versions as needed

---

**Last Updated**: 2025-03-28  
**Script Version**: 1.0  
**Status**: Production Ready
