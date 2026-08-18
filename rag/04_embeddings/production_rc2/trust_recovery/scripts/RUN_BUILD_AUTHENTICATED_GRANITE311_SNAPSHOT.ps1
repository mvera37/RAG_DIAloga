param(
  [Parameter(Mandatory=$true)][string]$SourceModelDir,
  [string]$OutputDir = ".\granite311_authenticated_snapshot"
)
$ErrorActionPreference="Stop"
$Py="python"
& $Py -B ".\scripts\build_authenticated_granite311_snapshot_rc2.py" `
  --source-model-dir "$SourceModelDir" `
  --output-dir "$OutputDir"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
