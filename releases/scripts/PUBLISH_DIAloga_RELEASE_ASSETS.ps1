[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$Root,
    [string]$Repository = "mvera37/RAG_DIAloga",
    [string]$TargetRef = "agent/bootstrap-rag",
    [switch]$IncludeHistoricalAudits,
    [switch]$RequireGranite,
    [switch]$ReplaceExisting
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Assert-Tool([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required tool '$Name' was not found. Install GitHub CLI and authenticate with 'gh auth login'."
    }
}

function Get-Sha256([string]$Path) {
    (Get-FileHash -Algorithm SHA256 -LiteralPath $Path).Hash.ToLowerInvariant()
}

function Find-ExactAsset {
    param(
        [string]$CanonicalName,
        [string]$ExpectedSha256,
        [string[]]$Aliases = @()
    )
    $names = @($CanonicalName) + $Aliases
    foreach ($name in $names) {
        $matches = Get-ChildItem -LiteralPath $Root -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -eq $name } | Sort-Object FullName
        foreach ($item in $matches) {
            if ((Get-Sha256 $item.FullName) -eq $ExpectedSha256.ToLowerInvariant()) {
                if ($item.Name -eq $CanonicalName) { return $item.FullName }
                $staging = Join-Path $Root "_dialoga_release_staging"
                New-Item -ItemType Directory -Force -Path $staging | Out-Null
                $dest = Join-Path $staging $CanonicalName
                Copy-Item -LiteralPath $item.FullName -Destination $dest -Force
                if ((Get-Sha256 $dest) -ne $ExpectedSha256.ToLowerInvariant()) {
                    throw "Canonical alias copy failed SHA verification: $CanonicalName"
                }
                return $dest
            }
        }
    }
    return $null
}

function Extract-EmbeddedAsset {
    param(
        [string]$ContainerZip,
        [string]$Member,
        [string]$CanonicalName,
        [string]$ExpectedSha256
    )
    $existing = Find-ExactAsset -CanonicalName $CanonicalName -ExpectedSha256 $ExpectedSha256
    if ($existing) { return $existing }
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $zip = [System.IO.Compression.ZipFile]::OpenRead($ContainerZip)
    try {
        $entry = $zip.Entries | Where-Object { $_.FullName -eq $Member }
        if (-not $entry) { throw "Embedded member not found: $Member" }
        $staging = Join-Path $Root "_dialoga_release_staging"
        New-Item -ItemType Directory -Force -Path $staging | Out-Null
        $dest = Join-Path $staging $CanonicalName
        [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $dest, $true)
        if ((Get-Sha256 $dest) -ne $ExpectedSha256.ToLowerInvariant()) {
            throw "Embedded asset failed SHA verification: $CanonicalName"
        }
        return $dest
    }
    finally { $zip.Dispose() }
}

function Prepare-DerivedAssets {
    $rc4 = Find-ExactAsset -CanonicalName "DIAloga_RAG_Canonical_V4_Integrated_RC4.zip" -ExpectedSha256 "f45eb3a90b73dadb14d9c73bc87fde64f1b1a49d298395e93fe8a8e7555214d1"
    if ($rc4) {
        Extract-EmbeddedAsset -ContainerZip $rc4 -Member "dependencies/DIAloga_RAG_Canonical_V4_phase1_RC3.zip" -CanonicalName "DIAloga_RAG_Canonical_V4_phase1_RC3.zip" -ExpectedSha256 "bf242b4e37cdb91e75ecd8fd0a2660c2dfdc08bc429a954d1ea166907d47c7da" | Out-Null
        Extract-EmbeddedAsset -ContainerZip $rc4 -Member "dependencies/DIAloga_RAG_Canonical_V4_Primaria_RC6.zip" -CanonicalName "DIAloga_RAG_Canonical_V4_Primaria_RC6.zip" -ExpectedSha256 "4e534683c5fac26d321c004c755abbcc7185bccdf328279b2d90cdcd72d0bec5" | Out-Null
        Extract-EmbeddedAsset -ContainerZip $rc4 -Member "dependencies/DIAloga_RAG_Canonical_V4_Secundaria_RC7.zip" -CanonicalName "DIAloga_RAG_Canonical_V4_Secundaria_RC7.zip" -ExpectedSha256 "471648192628656c4a39ef32caebb6292f013d80bffac76b836c4163b226b9bd" | Out-Null
    }

    $denseAudit = Find-ExactAsset -CanonicalName "DIAloga_Dense_Index_Build_RC2_External_Audit_Bundle.zip" -ExpectedSha256 "8e10f52a8ce63db6129969c2fcaf3e4c3ef43ace3448ba1a76ba1260913df662"
    if ($denseAudit) {
        Extract-EmbeddedAsset -ContainerZip $denseAudit -Member "candidate/DIAloga_Dense_Index_Build_RC2_Candidate.zip" -CanonicalName "DIAloga_Dense_Index_Build_RC2_Candidate.zip" -ExpectedSha256 "f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8" | Out-Null
    }
}

function Ensure-DraftRelease {
    param([string]$Tag,[string]$Title,[switch]$Prerelease)
    & gh release view $Tag --repo $Repository *> $null
    if ($LASTEXITCODE -eq 0) { return }
    $args = @(
        "release","create",$Tag,
        "--repo",$Repository,
        "--target",$TargetRef,
        "--title",$Title,
        "--notes","DIAloga controlled artifact archive. Verify SHA-256 against releases/RELEASE_UPLOAD_INVENTORY.json before use.",
        "--draft"
    )
    if ($Prerelease) { $args += "--prerelease" }
    & gh @args
    if ($LASTEXITCODE -ne 0) { throw "Could not create draft release: $Tag" }
}

function Upload-Group {
    param([string]$Tag,[string]$Title,[array]$Assets,[switch]$Prerelease)
    Ensure-DraftRelease -Tag $Tag -Title $Title -Prerelease:$Prerelease
    foreach ($a in $Assets) {
        $path = Find-ExactAsset -CanonicalName $a.Name -ExpectedSha256 $a.Sha -Aliases $a.Aliases
        if (-not $path) {
            if ($a.Required) { throw "Required asset not found with expected SHA-256: $($a.Name)" }
            Write-Warning "Optional asset not found: $($a.Name)"
            continue
        }
        $actual = Get-Sha256 $path
        if ($actual -ne $a.Sha) { throw "SHA mismatch before upload: $($a.Name)" }
        Write-Host "VERIFIED $($a.Name) $actual"
        $args = @("release","upload",$Tag,$path,"--repo",$Repository)
        if ($ReplaceExisting) { $args += "--clobber" }
        & gh @args
        if ($LASTEXITCODE -ne 0) {
            throw "Upload failed for $($a.Name). No release promotion was performed."
        }
    }
}

Assert-Tool "gh"
if (-not (Test-Path -LiteralPath $Root -PathType Container)) { throw "Root directory does not exist: $Root" }
& gh auth status
if ($LASTEXITCODE -ne 0) { throw "GitHub CLI is not authenticated." }

Prepare-DerivedAssets

$cneb = @(
    @{Name="DIAloga_RAG_Canonical_V4_phase1_RC3.zip"; Sha="bf242b4e37cdb91e75ecd8fd0a2660c2dfdc08bc429a954d1ea166907d47c7da"; Required=$true; Aliases=@()},
    @{Name="DIAloga_RAG_Canonical_V4_Primaria_RC6.zip"; Sha="4e534683c5fac26d321c004c755abbcc7185bccdf328279b2d90cdcd72d0bec5"; Required=$true; Aliases=@()},
    @{Name="DIAloga_RAG_Canonical_V4_Secundaria_RC7.zip"; Sha="471648192628656c4a39ef32caebb6292f013d80bffac76b836c4163b226b9bd"; Required=$true; Aliases=@()}
)

$frozenCore = @(
    @{Name="DIAloga_RAG_Canonical_V4_Integrated_RC4.zip"; Sha="f45eb3a90b73dadb14d9c73bc87fde64f1b1a49d298395e93fe8a8e7555214d1"; Required=$true; Aliases=@()},
    @{Name="DIAloga_Hybrid_Index_V4_Design_RC9.zip"; Sha="e7f9eb8da031a56752e89c0cd357aa3dd6a244fac365743b38574fb80a90e8f5"; Required=$true; Aliases=@()},
    @{Name="DIAloga_Hybrid_Index_V4_Lexical_Index_RC1.zip"; Sha="67edda46bb3e0465921c254ae05df4a1b6a30926b6a26f45574b69f97dd2cdac"; Required=$true; Aliases=@()},
    @{Name="DIAloga_Hybrid_Index_V4_Lexical_Runtime_Integration_RC2.zip"; Sha="f2ff25c2129e9065a6ab3e9fbfe2fcdf3c7b7bee6bd5a7dc6874028a5ecfe36f"; Required=$true; Aliases=@()},
    @{Name="DIAloga_Production_Embeddings_RC2_Candidate.zip"; Sha="67d0804361c2cb594216c5c33de330cc7c22c5f5988372eabd9988ba8f86ae2a"; Required=$true; Aliases=@()}
)

$prodEvidence = @(
    @{Name="DIAloga_Production_Embeddings_RC2_Candidate_FRESH_REGEN.zip"; Sha="1a06c0d1779f043bfcd75ec04b575b85d491c4ff6dddcac4c9b9db6e95ae8db4"; Required=$true; Aliases=@("DIAloga_Production_Embeddings_RC2_Candidate(1).zip")},
    @{Name="DIAloga_Production_Embedding_Generation_RC2_Execution_Bundle.zip"; Sha="e5bf137afcdb782d11de7fdc455cdc10bfbf12e4dc8db4ba3e75469dc8bfdb6c"; Required=$true; Aliases=@()},
    @{Name="DIAloga_Production_Embeddings_RC2_Supplemental_External_Audit_Bundle.zip"; Sha="31937db6a7d028a3b75610ae01920cf9665e5e3d394269ab6ee6f26f9cb5a6ef"; Required=$true; Aliases=@()}
)

$denseRc2 = @(
    @{Name="DIAloga_Dense_Index_Build_RC2_Candidate.zip"; Sha="f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8"; Required=$true; Aliases=@()},
    @{Name="DIAloga_Dense_Index_Build_RC2_External_Audit_Bundle.zip"; Sha="8e10f52a8ce63db6129969c2fcaf3e4c3ef43ace3448ba1a76ba1260913df662"; Required=$true; Aliases=@()}
)

$historicalAudits = @(
    @{Name="DIAloga_RAG_Canonical_V4_Integrated_RC4_Audit_Bundle.zip"; Sha="46cd654e69316d115e53627132843c841b993b2ae39142dbfc4b217afa6e9ec9"; Required=$false; Aliases=@()},
    @{Name="DIAloga_Hybrid_Index_V4_Design_RC9_External_Audit_Bundle.zip"; Sha="c7364ad53a841e72a4114784ba06be7c93a64b3152e6725a37cf0958d7516ff1"; Required=$false; Aliases=@()},
    @{Name="DIAloga_Hybrid_Index_V4_Lexical_Build_RC1_Audit_Bundle.zip"; Sha="5e7023f427e8b719cc1ea38128d16a1c13ad732da6577fd535b8d0bedb472020"; Required=$false; Aliases=@()},
    @{Name="DIAloga_Hybrid_Index_V4_Lexical_Runtime_Integration_RC2_Audit_Bundle.zip"; Sha="3f4043237cac50245caa02e13d86679080aebb3edd776f7f2b80e640449ddd3c"; Required=$false; Aliases=@()},
    @{Name="DIAloga_Embedding_Model_Benchmark_RC2_External_Audit_Bundle.zip"; Sha="a26cb3e998edab6d581fa5307ffb78dd0d2c4682290366a8699930e8859e1c21"; Required=$false; Aliases=@()},
    @{Name="DIAloga_Production_Embeddings_RC2_External_Audit_Bundle.zip"; Sha="e32f442fd2b39573842604692f51a3f9c67fd96b808b0e0e0cddde4328a334dd"; Required=$false; Aliases=@()}
)

Upload-Group -Tag "cneb-assets-2026-08" -Title "CNEB reusable canonical assets" -Assets $cneb
Upload-Group -Tag "rag-frozen-core-2026-08" -Title "DIAloga RAG frozen core assets" -Assets $frozenCore
Upload-Group -Tag "production-embeddings-rc2-evidence" -Title "Production Embeddings RC2 reproducibility and audit evidence" -Assets $prodEvidence -Prerelease
Upload-Group -Tag "dense-index-rc2-audit-candidate" -Title "Dense Index RC2 external-audit candidate" -Assets $denseRc2 -Prerelease

if ($IncludeHistoricalAudits) {
    Upload-Group -Tag "rag-audit-archive-2026-08" -Title "DIAloga RAG historical external audit archive" -Assets $historicalAudits -Prerelease
}

$granite = Find-ExactAsset -CanonicalName "DIAloga_Granite311_Authenticated_Snapshot_RC2.zip" -ExpectedSha256 "3e79757c748ede47e8ebe3c768a29ce0218e14949dab41177b8ce42b40fdec12"
if ($granite) {
    $model = @(@{Name="DIAloga_Granite311_Authenticated_Snapshot_RC2.zip"; Sha="3e79757c748ede47e8ebe3c768a29ce0218e14949dab41177b8ce42b40fdec12"; Required=$true; Aliases=@()})
    Upload-Group -Tag "granite311-authenticated-snapshot-r2" -Title "Authenticated Granite311 snapshot for DIAloga" -Assets $model -Prerelease
} elseif ($RequireGranite) {
    throw "Authenticated Granite311 snapshot not found with expected SHA-256."
} else {
    Write-Warning "Granite311 snapshot not found under Root; skipped."
}

Write-Host "SUCCESS: all transferred assets were verified by SHA-256 before upload. Releases remain DRAFT and must be reviewed before publication."
