# Windows to Cachuntu migration

Status: command-line prototype. The graphical wizard and a real Windows SSH transfer remain pending. This feature is newer than the exported 26.10.1.0 ISO.

The first scope selected by the user is Documents, Pictures, Music and Videos. Export from explicitly selected folders on Windows, or accessible backup folders. Review the bundle before importing into a new directory. Files keep their contents and relative names; SHA256 is checked during import. Windows applications and system settings are outside this first scope.

## Local workflow

Run the exporter with Python 3 on Windows. Use the actual folder locations, including redirected OneDrive folders if applicable. Download cloud-only files locally first. Links and junctions are skipped and listed in the manifest.

```powershell
python windows-migration.py export --documents "C:\Users\you\Documents" --pictures "C:\Users\you\Pictures" --music "C:\Users\you\Music" --videos "C:\Users\you\Videos" --output "D:\cachuntu-migration.zip"
```

Copy the ZIP to Cachuntu, then inspect and import as the ordinary desktop user:

```bash
cachuntu-migrate plan /path/to/cachuntu-migration.zip
cachuntu-migrate import /path/to/cachuntu-migration.zip
```

The default destination is a new `~/Windows-import-YYYYMMDD-HHMMSS` directory. An explicit `--destination` must also be a new folder. Existing files are never overwritten. A failed integrity check leaves an `IMPORT_INCOMPLETE.txt` marker with the partial import for inspection. Export/import must run without administrator/root privileges. A bundle contains personal data; store and transport it accordingly.

## SSH workflow

Export the same ZIP first. If the source computer already exposes SSH/SFTP, Cachuntu can download it using the normal OpenSSH client and host-key verification:

```bash
cachuntu-migrate fetch-ssh --host you@windows-pc --remote-file Migration/cachuntu-migration.zip --output ./cachuntu-migration.zip
cachuntu-migrate plan ./cachuntu-migration.zip
cachuntu-migrate import ./cachuntu-migration.zip
```

The remote path is relative to the SSH account's accessible directory. Windows OpenSSH server setup, firewall access and authentication must be configured separately. The tool does not enable services or store passwords. A Windows client may alternatively upload the exported bundle to an already configured Cachuntu SSH account with `scp`.

## Planned graphical experience

1. Open **Migrate from Windows** after installation.
2. Choose local backup or SSH and explicitly select the source.
3. Show the four groups, counts, total size, free space and skipped items.
4. Review the destination and start a cancellable transfer.
5. Verify SHA256 and present a completion report with the destination.

Keep migration separate from disk partitioning. A mounted Windows source is read only. Disk decryption or NTFS repair must not be attempted automatically. The first implementation does not move/delete source files, merge into existing personal folders, migrate credentials or execute transferred programs.

## Verification

`python3 distro/qa/check-windows-migration.py` uses synthetic files to verify byte-for-byte transfer, checksum failure, destination conflicts, traversal rejection and source link exclusion. Actual SSH/SFTP, cloud files, cancellation, localized XDG folder integration and large-library performance still require integration tests.
