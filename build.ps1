# Open Kit 3D - one-shot rebuild (Blender -> FBX/GLB/previews + validation, then Unity import/prefabs/validation/scenes/package/screenshots)
# Usage:  powershell -ExecutionPolicy Bypass -File .\build.ps1 [-Clean] [-SkipBlender] [-SkipUnity] [-Method All|ImportAll|Validate|RenderScreenshots|CaptureM3|CaptureM4|CaptureM4Compare]
#   CaptureM4Compare writes captures\m4\<tag>-*.png with tag = `$env:OKIT_CAPTURE_TAG (default "after")
#   -Clean  delete every generated output first (Blender\out, generated Models/Prefabs/Themes/Materials/Scenes, captures\m3, captures\m4) = from-scratch build
param([switch]$Clean, [switch]$SkipBlender, [switch]$SkipUnity, [string]$Method = "All")
$ErrorActionPreference = "Stop"
$Root    = $PSScriptRoot
# Tool paths: set OKIT_BLENDER / OKIT_UNITY, or have blender on PATH and Unity 6000.4.0f1 in the default Unity Hub folder
$Blender = if ($env:OKIT_BLENDER) { $env:OKIT_BLENDER } else { "blender" }
$Unity   = if ($env:OKIT_UNITY) { $env:OKIT_UNITY } else { Join-Path $env:ProgramFiles "Unity\Hub\Editor\6000.4.0f1\Editor\Unity.exe" }
New-Item -ItemType Directory -Force "$Root\Logs" | Out-Null
if (Test-Path "$Root\Temp\UnityLockfile") {
  $busy = $false
  try { $fs = [System.IO.File]::Open("$Root\Temp\UnityLockfile", 'Open', 'ReadWrite', 'None'); $fs.Close() } catch { $busy = $true }
  if ($busy) { throw "Unity already has this project open (Temp\UnityLockfile is locked) - close the editor first" }
}
if ($Clean) {
  $gen = @("Blender\out", "captures\m3", "captures\m4",
           "Assets\OpenKit3D\Models", "Assets\OpenKit3D\Prefabs", "Assets\OpenKit3D\Themes",
           "Assets\OpenKit3D\Materials", "Assets\OpenKit3D\Scenes\Demo")
  foreach ($g in $gen) {
    foreach ($p in @("$Root\$g", "$Root\$g.meta")) { if (Test-Path $p) { Remove-Item -Recurse -Force $p } }
  }
  Write-Output "[build] clean: removed generated outputs"
}
if (-not $SkipBlender) {
  $ErrorActionPreference = "Continue"   # Blender may write to stderr; judge success by exit code + log instead
  & $Blender --background --factory-startup --python-exit-code 1 --python "$Root\Blender\scripts\build_asset.py" -- --all --preview 2>&1 |
    Tee-Object "$Root\Logs\blender-build.log" | Select-String "\[okit\] (DONE|FAIL|VALIDATION|WARNING)"
  $blExit = $LASTEXITCODE
  $ErrorActionPreference = "Stop"
  $bl = Get-Content "$Root\Logs\blender-build.log" -Raw
  if ($blExit -ne 0 -or $bl -notmatch "\[okit\] DONE .*failing checks: \[\]") { throw "Blender build/validation failed - see Logs\blender-build.log" }
}
if (-not $SkipUnity) {
  $p = Start-Process -FilePath $Unity -Wait -PassThru -ArgumentList @(
    "-batchmode", "-quit", "-projectPath", "`"$Root`"",
    "-executeMethod", "OpenKit.Editor.Build.$Method",
    "-logFile", "`"$Root\Logs\unity-build.log`"")
  Select-String -Path "$Root\Logs\unity-build.log" -Pattern "^\[OpenKit\] (BUILD|VALIDATE|ImportAll|exported|contact|M3 captures|M4|ORIENTATION|MONSTER)" | ForEach-Object { $_.Line }
  $ul = Get-Content "$Root\Logs\unity-build.log" -Raw
  if ($p.ExitCode -ne 0 -or $ul -notmatch "\[OpenKit\] BUILD OK") { throw "Unity exited with $($p.ExitCode) / no BUILD OK - see Logs\unity-build.log" }
}
Write-Output "[build] OK"
