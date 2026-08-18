# add_subtitles.ps1 -- put subtitles_en.srt onto the recorded demo video.
#
#   .\add_subtitles.ps1 -Video ..\..\raw\demo_raw.mp4                  # burn in (default)
#   .\add_subtitles.ps1 -Video raw.mp4 -Mode soft                      # soft track, no re-encode
#   .\add_subtitles.ps1 -Video raw.mp4 -Out demo_subtitled.mp4 -Mode both
#
# Burned-in subtitles are the safe choice for a reviewer: they survive Outlook preview,
# OneDrive playback and any player that ignores subtitle tracks. Soft subtitles keep the
# original video stream untouched (no quality loss, seconds instead of minutes).
#
# ASCII only -- PowerShell 5.1 reads a BOM-less .ps1 as ANSI.

param(
  [Parameter(Mandatory = $true)][string]$Video,
  [string]$Srt = "$PSScriptRoot\subtitles_en.srt",
  [string]$Out = "",
  [ValidateSet('burn', 'soft', 'both')][string]$Mode = 'burn',
  [int]$FontSize = 18,
  [string]$FontName = 'Segoe UI',
  [int]$Crf = 23              # 20 = visually lossless here; 23 keeps a 7-minute screencast near 20 MB
)

$ErrorActionPreference = 'Stop'

$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpeg) {
  Write-Host "ffmpeg is not installed. Install it once with:" -ForegroundColor Yellow
  Write-Host "    winget install --id Gyan.FFmpeg -e" -ForegroundColor Yellow
  Write-Host "Then open a NEW terminal (PATH is refreshed only for new processes)."
  exit 1
}

$Video = (Resolve-Path $Video).Path
$Srt = (Resolve-Path $Srt).Path
if (-not $Out) {
  $Out = [IO.Path]::Combine([IO.Path]::GetDirectoryName($Video),
    [IO.Path]::GetFileNameWithoutExtension($Video) + '_sub.mp4')
}

# The subtitles filter parses ':' and '\' itself, so a Windows path has to be handed to it
# as forward slashes with the drive colon escaped, quoted inside the filter argument:
#   subtitles='D\:/path/to/subs.srt'
# Relative names are not an option here: Set-Location/Push-Location do NOT change the
# working directory a child process inherits, so a bare filename resolves against whatever
# directory the shell was started in and the filter fails with a bare "Option not found".
$srtArg = ($Srt -replace '\\', '/') -replace ':', '\:'

function Invoke-Burn {
  param([string]$Target)
  $style = "FontName=$FontName,FontSize=$FontSize,PrimaryColour=&H00FFFFFF," +
           "OutlineColour=&H90000000,BorderStyle=3,Outline=1,Shadow=0,MarginV=42"
  & ffmpeg -hide_banner -y -i $Video `
    -vf "subtitles='$srtArg':force_style='$style'" `
    -c:v libx264 -preset medium -crf $Crf -pix_fmt yuv420p `
    -c:a aac -b:a 160k `
    $Target
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed (burn), exit $LASTEXITCODE" }
  Write-Host "burned-in -> $Target" -ForegroundColor Green
}

function Invoke-Soft {
  param([string]$Target)
  & ffmpeg -hide_banner -y -i $Video -i $Srt `
    -c copy -c:s mov_text -metadata:s:s:0 language=eng -disposition:s:0 default `
    $Target
  if ($LASTEXITCODE -ne 0) { throw "ffmpeg failed (soft), exit $LASTEXITCODE" }
  Write-Host "soft track -> $Target" -ForegroundColor Green
}

switch ($Mode) {
  'burn' { Invoke-Burn -Target $Out }
  'soft' { Invoke-Soft -Target $Out }
  'both' {
    $softOut = [IO.Path]::Combine([IO.Path]::GetDirectoryName($Out),
      [IO.Path]::GetFileNameWithoutExtension($Out) + '_soft.mp4')
    Invoke-Burn -Target $Out
    Invoke-Soft -Target $softOut
  }
}
