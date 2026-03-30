# Quick Start: Python Version Management

## 🚀 Quick Start

```powershell
# Navigate to solution root
cd C:\Users\Michael\source\repos\SajuukKahn\PMXClean

# Download all Python versions from GitHub
.\UpdatePythonVersions.ps1

# Commit to Git
git add PMXClean\PMXVersions
git commit -m "Update Python versions"
git push
```

## 📁 What Gets Created

```
PMXClean\PMXVersions\
├── v1.0.0\        # Python files from release v1.0.0
├── v2.0.0\        # Python files from release v2.0.0
├── v2.1.0\        # Python files from release v2.1.0
└── Versions.md    # Auto-generated metadata
```

## ✨ Common Commands

| Command | Description |
|---------|-------------|
| `.\UpdatePythonVersions.ps1` | Download all versions |
| `.\UpdatePythonVersions.ps1 -Releases "v2.0.0"` | Download specific version |
| `.\UpdatePythonVersions.ps1 -Force` | Re-download all versions |
| `.\UpdatePythonVersions.ps1 -Token "ghp_..."` | Use GitHub token |

## 🔧 Integration

### Visual Studio External Tool

**Tools** → **External Tools** → **Add**:
- Title: `Update Python Versions`
- Command: `powershell.exe`
- Arguments: `-ExecutionPolicy Bypass -File "$(SolutionDir)UpdatePythonVersions.ps1"`

### MSBuild (Optional)

Add to `PMXClean.csproj`:
```xml
<Target Name="UpdatePythonVersions" BeforeTargets="BeforeBuild" Condition="'$(UPDATE_PYTHON_VERSIONS)' == '1'">
  <Exec Command="powershell -ExecutionPolicy Bypass -File &quot;$(SolutionDir)UpdatePythonVersions.ps1&quot;" />
</Target>
```

Run with:
```powershell
$env:UPDATE_PYTHON_VERSIONS = "1"
dotnet build
```

## 📖 Full Documentation

- **[POWERSHELL_INTEGRATION.md](POWERSHELL_INTEGRATION.md)** - Complete guide
- **[PMXVersions\Versions.md](PMXVersions\Versions.md)** - Usage instructions
- **[GITHUB_INTEGRATION.md](GITHUB_INTEGRATION.md)** - GUI approach (alternative)

## ❓ FAQ

**Q: Do I need a GitHub token?**  
A: No, not for public repos. Use token to avoid rate limits or for private repos.

**Q: Will this slow down my builds?**  
A: Only if you add it as a pre-build event. Manual execution recommended.

**Q: Should I commit these files to Git?**  
A: **Yes!** That's the whole point. They become part of your repository.

**Q: How often should I update?**  
A: Whenever PathMasterX releases a new version you want to track.

**Q: Can I delete old versions?**  
A: Yes, just delete the folder and commit: `git rm -r PMXClean\PMXVersions\v1.0.0`
