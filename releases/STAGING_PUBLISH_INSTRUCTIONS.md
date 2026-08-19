# DIAloga — GitHub Release staging publication

The binary artifacts are intentionally kept out of normal Git history. They are published as GitHub Release assets after exact SHA-256 verification.

## Current staging archive

- File: `DIAloga_GitHub_Release_Staging_Current.zip`
- Bytes: `324348878`
- SHA-256: `cb575eb4ab654db7ef8c085a78206c889af387314a2096f90966a8db755e4abd`
- Assets: `13`

See `STAGING_MANIFEST_CURRENT.json` for the complete physical asset ledger.

## Publication

After extracting the staging archive on a trusted workstation:

```powershell
.\RUN_PUBLISH_TO_GITHUB.ps1
```

The wrapper downloads the publisher from immutable repository commit:

`1ed4fbde7a963574cc5ff286ab519a4bf65bd2b5`

The publisher:

1. requires an authenticated GitHub CLI session;
2. recursively resolves assets by canonical filename and expected SHA-256;
3. reconstructs only byte-identical embedded CNEB/Dense assets when necessary;
4. verifies SHA-256 immediately before every upload;
5. creates GitHub Releases as **DRAFT**;
6. never promotes Dense RC2 to runtime authority;
7. does not publish Dense RC1;
8. does not replace existing assets unless `-ReplaceExisting` is explicitly supplied.

## Granite311 snapshot

The authenticated snapshot is not contained in the staging archive because of its size. Expected file:

`DIAloga_Granite311_Authenticated_Snapshot_RC2.zip`

Expected SHA-256:

`3e79757c748ede47e8ebe3c768a29ce0218e14949dab41177b8ce42b40fdec12`

To publish it, copy the byte-identical snapshot ZIP into the staging `assets` directory and execute:

```powershell
.\RUN_PUBLISH_TO_GITHUB.ps1 -RequireGranite
```

Do not modify the authenticated snapshot ZIP or insert additional files into it.
