@echo off
setlocal enabledelayedexpansion

net file 1>nul 2>nul && goto :run || powershell -ex unrestricted -Command "Start-Process -Verb RunAs -FilePath '%comspec%' -ArgumentList '/c %~fnx0 %*'"
goto :eof
:run

title PMX Utility Script
set "defaultPath=C:\Program Files\PVA\PathMasterX\"
set "altPath=%userprofile%\source\repos\precisionvalve\PathMasterX\PathMasterX\bin\x64\Debug\net8.0-windows\"

set "bothPaths=Y"

set targetPath=%defaultPath%

if not exist %targetPath% (
	set "targetPath=%altPath%"
	set "bothPaths="
)

if not exist %targetPath% (
	exit
)

set "launchOffline="
set "autoxAdvance="
set "visionTrace="
set "visionDebug="
set "suppressTopMost="
set "postStartupPage="
set "softwareRendering="

:: ===========================================================================================
:: ===========================================================================================
:: ===========================================================================================

:menu
cls
echo =============
echo  Select Tool
echo =============
echo.
echo Path: %targetPath%
echo.
echo [1] Compare Python
echo [2] Back Up
echo [3] Clean Up
echo [4] Utility
echo [5] PMX Launcher
echo.
echo [x] Exit
echo.
choice /c 12345x /n /m ""
cls

if %ERRORLEVEL% EQU 6 goto close
if %ERRORLEVEL% EQU 5 goto pmxLauncher
if %ERRORLEVEL% EQU 4 goto utilityMenu
if %ERRORLEVEL% EQU 3 goto cleanup
if %ERRORLEVEL% EQU 2 goto backupMenu
if %ERRORLEVEL% EQU 1 goto comparepython

goto menu

:: ===========================================================================================
:: ===========================================================================================
:: ===========================================================================================

:comparepython
cls
echo ================
echo  Compare Python
echo ================
if defined bothPaths (
	echo Source: %targetPath%
)
echo.
echo [1] Compare Installed
echo [2] Pull Fresh Master
echo.
echo [x] Back
if defined bothPaths (
	echo.
	echo [s] Swap Source
)
echo.

if defined bothPaths (
	choice /c 12x /n /m ""
) else (
	choice /c 12xs /n /m ""
)
cls

if defined bothPaths (
	if %ERRORLEVEL% EQU 4 (
		if /i "%targetPath%"=="%defaultPath%" (
			if exist "%altPath%" (
				set "targetPath=%altPath%"
			) else (
				echo Alternate path not found!
			)
		) else (
			set "targetPath=%defaultPath%"
		)
	)
)
if %ERRORLEVEL% EQU 3 goto menu
if %ERRORLEVEL% EQU 2 goto compare
if %ERRORLEVEL% EQU 1 goto pullfresh

goto comparepython

:compare
echo --- Copying files ---
rmdir /s /q target\
if not exist "target\" mkdir "target\"
xcopy "%targetPath%" target\ /t /e /c /q /y
xcopy "%targetPath%*.py" target\ /s /y
echo ------- Copy completed -------- Starting WinMerge -------
echo - Changes in WinMerge do not affect the installed files -
timeout /t 3 /nobreak >nul
start .\WinMergePortable\App\WinMerge64\WinMergeU.exe /r /f *.py /u /wl /dl "SOURCE" ".\master" ".\target"
goto comparepython

:pullfresh
echo -------- Copying files from the source into master ---------
rmdir /s /q master\
if not exist "master\" mkdir "master\"
xcopy "%targetPath%" master\ /t /e /c /q /y
xcopy "%targetPath%*.py" master\ /s /y
echo -------- Copy from source to master complete ---------
timeout /t 2 /nobreak >nul
goto comparepython

:: ===========================================================================================
:: ===========================================================================================
:: ===========================================================================================

:backupMenu
cls
echo ===============
echo  Back Up Files
echo ===============
if defined bothPaths (
	echo Source: %targetPath%
)
echo.
echo [1] Start New - Delete \backup
echo [2] Copy JSON
echo [3] Copy Retention
echo [4] Copy Python
echo [5] Copy DLLs
echo [6] Copy Page Stubs
echo [7] Overwrite %targetPath% with backup
echo.
echo [x] Back
if defined bothPaths (
	echo.
	echo [s] Swap Source
)
echo.

if defined bothPaths (
	choice /c 1234567xs /n /m ""
) else (
	choice /c 1234567x /n /m ""
)
cls

if defined bothPaths (
	if %ERRORLEVEL% EQU 9 (
		if /i "%targetPath%"=="%defaultPath%" (
			if exist "%altPath%" (
				set "targetPath=%altPath%"
			) else (
				echo Alternate path not found!
			)
		) else (
			set "targetPath=%defaultPath%"
		)
	)
)
if %ERRORLEVEL% EQU 8 goto menu
if %ERRORLEVEL% EQU 7 goto overwriteTarget
if %ERRORLEVEL% EQU 6 goto copyStubs
if %ERRORLEVEL% EQU 5 goto copyDlls
if %ERRORLEVEL% EQU 4 goto copyPython
if %ERRORLEVEL% EQU 3 goto copyRetention
if %ERRORLEVEL% EQU 2 goto backupJson
if %ERRORLEVEL% EQU 1 goto newbackup

goto backupMenu

:newbackup
echo -------- Removing the backup folder ---------
rmdir /s /q backup\
echo -------- Initializing backup folder ---------
timeout /t 2 /nobreak >nul
mkdir backup\
goto backupMenu

:backupJson
echo -------- Copying JSON from the source into backup ---------
if not exist "backup\" mkdir "backup\"
xcopy "%targetPath%" backup\ /t /e /c /q /y
xcopy "%targetPath%*.json" backup\ /s /y
echo -------- Copying JSON source into backup complete ---------
timeout /t 2 /nobreak >nul
goto backupMenu

:copyRetention
echo -------- Copying Retention from the source into backup ---------
if not exist "backup\" mkdir "backup\"
xcopy "%targetPath%" backup\ /t /e /c /q /y
xcopy "%targetPath%*.retention" backup\ /s /y
echo -------- Copying Retention source into backup complete ---------
timeout /t 2 /nobreak >nul
goto backupMenu

:copyPython
echo -------- Copying Python from the source into backup ---------
if not exist "backup\" mkdir "backup\"
xcopy "%targetPath%" backup\ /t /e /c /q /y
xcopy "%targetPath%*.py" backup\ /s /y
echo -------- Copying Python source into backup complete ---------
timeout /t 2 /nobreak >nul
goto backupMenu

:copyDlls
echo -------- Copying DLLs from the source into backup ---------
if not exist "backup\" mkdir "backup\"
xcopy "%targetPath%" backup\ /t /e /c /q /y
xcopy "%targetPath%*.DLL" backup\ /s /y
echo -------- Copying DLLs source into backup complete ---------
timeout /t 2 /nobreak >nul
goto backupMenu

:copyStubs
echo -------- Copying Page Stubs from the source into backup ---------
if not exist "backup\" mkdir "backup\"
xcopy "%targetPath%" backup\ /t /e /c /q /y
xcopy "%targetPath%*.stub" backup\ /s /y
echo -------- Copying Page Stubs source into backup complete ---------
timeout /t 2 /nobreak >nul
goto backupMenu

:overwriteTarget
echo Overwriting the Target Path with backup folder contents
echo %targetPath%
echo This cannot be undone: Press Y to confirm
choice /c YN /n /m ""
if %ERRORLEVEL% NEQ 1 goto backupMenu

echo -------- Copying all data in the backup folder to Target Location ---------
xcopy backup\ "%targetPath%" /s /y /c
echo -------- Copying all data in the backup folder to Target Location ---------
timeout /t 2 /nobreak >nul
goto backupMenu

:: ===========================================================================================
:: ===========================================================================================
:: ===========================================================================================

:cleanup
cls
echo ================
echo  Clean Up Files
echo ================
if defined bothPaths (
	echo Target: %targetPath%
)
echo.
echo [1] Delete JSON
echo [2] Delete Retention
echo [3] Delete Python
echo [4] Delete Page Stubs
echo.
echo [x] Back
if defined bothPaths (
	echo.
	echo [s] Swap Target
)
echo.

if defined bothPaths (
	choice /c 1234xs /n /m ""
) else (
	choice /c 1234x /n /m ""
)
cls

if defined bothPaths (
	if %ERRORLEVEL% EQU 6 (
		if /i "%targetPath%"=="%defaultPath%" (
			if exist "%altPath%" (
				set "targetPath=%altPath%"
			) else (
				echo Alternate path not found!
			)
		) else (
			set "targetPath=%defaultPath%"
		)
	)
)
if %ERRORLEVEL% EQU 5 goto menu
if %ERRORLEVEL% EQU 4 goto deletePageStubs
if %ERRORLEVEL% EQU 3 goto deletePython
if %ERRORLEVEL% EQU 2 goto deleteRetention
if %ERRORLEVEL% EQU 1 goto deleteJson

goto cleanup

:deletePageStubs
erase "%targetPath%*.stub" /s /f
echo -- All Page Stub Files Deleted --
echo "%targetPath%"
timeout /t 2 /nobreak >nul
goto cleanup

:deleteJson
erase "%targetPath%*.json" /s /f
echo -- All JSON Files Deleted --
echo "%targetPath%"
timeout /t 2 /nobreak >nul
goto cleanup

:deleteRetention
erase "%targetPath%*.retention" /s /f
echo -- All Retention Files Deleted --
echo "%targetPath%"
timeout /t 2 /nobreak >nul
goto cleanup

:deletePython
erase "%targetPath%*.py" /s /f
echo -- All Python Files Deleted --
echo "%targetPath%"
timeout /t 2 /nobreak >nul
goto cleanup

:: ===========================================================================================
:: ===========================================================================================
:: ===========================================================================================

:utilityMenu
cls
echo ===========
echo  Utilities
echo ===========
if defined bothPaths (
	echo Target: %targetPath%
)
echo.
echo [1] Check Network Settings
echo [2] Check for large files
echo [3] 
echo.
echo [x] Back
echo.

choice /c 123x /n /m ""
cls

if %ERRORLEVEL% EQU 4 goto menu
if %ERRORLEVEL% EQU 3 goto tres
if %ERRORLEVEL% EQU 2 goto checkLargeFiles
if %ERRORLEVEL% EQU 1 goto networkCheck

goto utilityMenu

:networkCheck
PowerShell -ExecutionPolicy Bypass -Command "& {Get-NetIPConfiguration | Format-Table -Property 'InterfaceAlias','IPv4Address';Get-NetAdapterAdvancedProperty -Name 'Camera*' | Where-Object 'DisplayName' -in ('Jumbo Packet', 'Receive Buffers','Interrupt Moderation Rate') | Format-Table -Property 'DisplayName', 'DisplayValue';}"
echo Pinging Galil
set "target_ip=100.100.100.101"
ping /n 1 /w 500 /4 %target_ip% | find "TTL=" >nul
if errorlevel 1 (
    echo     %target_ip% is Offline
) else (
    echo     %target_ip% is Online
)
echo.
echo Pinging Modbus I/O
set "target_ip=100.100.100.110"
ping /n 1 /w 500 /4 %target_ip% | find "TTL=" >nul
if errorlevel 1 (
    echo     %target_ip% is Offline
) else (
    echo     %target_ip% is Online
)
echo.
echo Pinging Camera
set "target_ip=200.200.200.201"
ping /n 1 /w 500 /4 %target_ip% | find "TTL=" >nul
if errorlevel 1 (
    echo     %target_ip% is Offline
) else (
    echo     %target_ip% is Online
)
echo.
pause
goto utilityMenu

:checkLargeFiles
echo Finding Files larger than 200MB...
forfiles /P C:\Users\ /M *.* /S /D +"01/01/2020" /C "cmd /c if @fsize gtr 209715200 echo @path @fsize @fdate @ftime"
pause
goto utilityMenu

:tres
goto utilityMenu

:: ===========================================================================================
:: ===========================================================================================
:: ===========================================================================================

:pmxLauncher
cls
echo ==============
echo  PMX Launcher
echo ==============
if defined bothPaths (
	echo Source: %targetPath%
)
echo.
echo Select options for launch below:
echo.
echo [1] Launch Offline %launchOffline%
echo [2] Auto-Accept Prompts %autoAdvance%
echo [3] Suppress Top Most %suppressTopMost%
echo [4] Vision Trace %visionTrace%
echo [5] Vision Debug %visionDebug%
echo [6] Software Only Rendering %softwareRendering%
echo.

if defined postStartupPage (
	echo [7] Start Page: %postStartupPage%
) else (
	echo [7] Start Page: Process Production
)

echo.
echo.
echo [L] Launch PMX with settings
echo.
echo.
echo [x] Back
echo.

if defined bothPaths (
	echo.
	echo [s] Swap Target
)
echo.

if defined bothPaths (
	choice /c 1234567Lxs /n /m ""
) else (
	choice /c 1234567Lx /n /m ""
)

cls

if defined bothPaths (
	if %ERRORLEVEL% EQU 10 (
		if /i "%targetPath%"=="%defaultPath%" (
			if exist "%altPath%" (
				set "targetPath=%altPath%"
			) else (
				echo Alternate path not found!
			)
		) else (
			set "targetPath=%defaultPath%"
		)
	)
)

if %ERRORLEVEL% EQU 9 goto menu
if %ERRORLEVEL% EQU 8 goto launchPMX
if %ERRORLEVEL% EQU 7 goto setStartPage
if %ERRORLEVEL% EQU 6 goto softwareRenderMode
if %ERRORLEVEL% EQU 5 goto visionDebugMode
if %ERRORLEVEL% EQU 4 goto visionTraceMode
if %ERRORLEVEL% EQU 3 goto topMostMode
if %ERRORLEVEL% EQU 2 goto autoAdvanceMode
if %ERRORLEVEL% EQU 1 goto launchOfflineMode

goto pmxLauncher

:softwareRenderMode
if defined softwareRendering (
	set "softwareRendering="
) else (
	set "softwareRendering=Y"
)
goto pmxLauncher

:visionDebugMode
if defined visionDebug (
	set "visionDebug="
) else (
	set "visionDebug=Y"
)
goto pmxLauncher

:visionTraceMode
if defined visionTrace (
	set "visionTrace="
) else (
	set "visionTrace=Y"
)
goto pmxLauncher

:setStartPage
echo Enter Page ReferenceName:
set /p postStartupPage=""
goto pmxLauncher

:topMostMode
if defined suppressTopMost (
	set "suppressTopMost="
) else (
	set "suppressTopMost=Y"
)
goto pmxLauncher

:autoAdvanceMode
if defined autoAdvance (
	set "autoAdvance="
) else (
	set "autoAdvance=Y"
)
goto pmxLauncher

:launchOfflineMode
if defined launchOffline (
	set "launchOffline="
) else (
	set "launchOffline=Y"
)
goto pmxLauncher

:launchPMX

set "arglist="

if defined launchOffline (
	set "arglist=%arglist%-offline " 
)

if defined autoAdvance (
	set "arglist=%arglist%-autoAdvance "
)

if defined suppressTopMost (
	set "arglist=%arglist%-topMost:false "
)

if defined visionTrace (
	set "arglist=%arglist%-visionTrace "
)

if defined visionDebug (
	set "arglist=%arglist%-visionDebug "
)

if defined softwareRendering (
	set "arglist=%arglist%-software "
)

if defined postStartupPage (
	set "arglist=%arglist%-page:%postStartupPage%"
)

::echo %arglist%
::pause
start "" /d %targetPath% /b PVA.PathMasterX.exe %arglist%

:close
exit
