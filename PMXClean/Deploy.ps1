# PMX Clean Deployment Script
# This script publishes the application in various configurations

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet('SingleFile', 'Standard', 'Both')]
    [string]$DeploymentType = 'Both',
    
    [Parameter(Mandatory=$false)]
    [ValidateSet('Release', 'Debug')]
    [string]$Configuration = 'Release'
)

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  PMX Clean - Deployment Script" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

$projectPath = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectFile = Join-Path $projectPath "PMXClean.csproj"

if (-not (Test-Path $projectFile)) {
    Write-Host "Error: Project file not found at $projectFile" -ForegroundColor Red
    exit 1
}

# Clean previous builds
Write-Host "Cleaning previous builds..." -ForegroundColor Yellow
dotnet clean $projectFile -c $Configuration
Write-Host ""

# Function to publish
function Publish-Application {
    param(
        [string]$Type,
        [string]$Config,
        [bool]$SingleFile
    )
    
    $outputPath = Join-Path $projectPath "bin\$Config\net10.0-windows\win-x64\publish"
    
    Write-Host "Publishing: $Type" -ForegroundColor Green
    Write-Host "Configuration: $Config" -ForegroundColor Gray
    Write-Host "Output: $outputPath" -ForegroundColor Gray
    Write-Host ""
    
    if ($SingleFile) {
        dotnet publish $projectFile `
            -c $Config `
            -r win-x64 `
            --self-contained true `
            /p:PublishSingleFile=true `
            /p:IncludeNativeLibrariesForSelfExtract=true `
            /p:IncludeAllContentForSelfExtract=true `
            /p:EnableCompressionInSingleFile=true
    }
    else {
        dotnet publish $projectFile `
            -c $Config `
            -r win-x64 `
            --self-contained true
    }
    
    if ($LASTEXITCODE -eq 0) {
        $exePath = Join-Path $outputPath "PMXClean.exe"
        if (Test-Path $exePath) {
            $fileInfo = Get-Item $exePath
            $fileSizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
            Write-Host ""
            Write-Host "✓ Success!" -ForegroundColor Green
            Write-Host "  Executable: $exePath" -ForegroundColor Gray
            Write-Host "  Size: $fileSizeMB MB" -ForegroundColor Gray
            
            # Check if WinMerge is present
            $winMergePath = Join-Path $outputPath "WinMergePortable\App\WinMerge64\WinMergeU.exe"
            if (Test-Path $winMergePath) {
                Write-Host "  WinMerge: ✓ Included" -ForegroundColor Gray
            }
            else {
                Write-Host "  WinMerge: ✗ Not found (comparison features will not work)" -ForegroundColor Yellow
            }
        }
    }
    else {
        Write-Host "✗ Build failed!" -ForegroundColor Red
    }
    Write-Host ""
}

# Execute deployment based on type
switch ($DeploymentType) {
    'SingleFile' {
        Publish-Application -Type "Single-File Deployment" -Config $Configuration -SingleFile $true
    }
    'Standard' {
        Publish-Application -Type "Standard Deployment" -Config $Configuration -SingleFile $false
    }
    'Both' {
        Publish-Application -Type "Single-File Deployment" -Config $Configuration -SingleFile $true
        Write-Host "─────────────────────────────────────────────────────" -ForegroundColor Cyan
        Publish-Application -Type "Standard Deployment" -Config $Configuration -SingleFile $false
    }
}

Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Deployment Complete!" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Yellow
Write-Host "  cd bin\$Configuration\net10.0-windows\win-x64\publish" -ForegroundColor Gray
Write-Host "  .\PMXClean.exe" -ForegroundColor Gray
Write-Host ""
