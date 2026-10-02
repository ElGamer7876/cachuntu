# Ubuntu review — 2026-10-01

Source candidate: Cachuntu 26.10.1.3, Ubuntu Resolute 26.04 LTS. The recovered
26.10.1.2 ISO contains the reviewed security fixes and passes artifact checks.
The next same-day patch corrects the welcome-to-Plasma compositor lifecycle;
its runtime handoff and ISO validation remain pending.

## Applicable security updates

| Notice | Package baseline for Resolute | Change |
| --- | --- | --- |
| [USN-8861-1](https://ubuntu.com/security/notices/USN-8861-1) | libssl3t64 >= 3.5.5-1ubuntu3.7 | Require before build/export and in installed QA. Reboot after updating, as instructed by Canonical. |
| [USN-8857-1](https://ubuntu.com/security/notices/USN-8857-1) | libkf6coreaddons6 >= 6.24.0-0ubuntu1.1 | Require for the Plasma base; fixes KShell argument quoting. |
| [USN-8862-1](https://ubuntu.com/security/notices/USN-8862-1) | libxpm4/xpmutils >= 1:3.5.17-1ubuntu0.26.04.2 | Check each installed architecture; do not install optional tools solely for this check. |
| [USN-8863-1](https://ubuntu.com/security/notices/USN-8863-1) | Installed GStreamer Good plugin variants >= 1.28.2-2ubuntu0.4 | Check multimedia components when present, including Qt and PulseAudio variants. |

The baseline JSON is included in cachuntu-defaults. Its checker examines the target dpkg database without executing target files or modifying packages. Absent optional packages are skipped; missing required packages, unconfigured packages and outdated installed architectures reject the gate. Debian version comparison handles epochs and Ubuntu revisions. The fixtures cover these cases.

The build now rejects stale packages before SquashFS compression and ISO export. Updating tests alone does not patch an existing ISO: apply the official Resolute security/updates packages, rerun the baseline and post-install checks, then validate reboot before release. Preserve a package manifest and downloaded package hashes for reproducibility. The prior 26.10.1.0 ISO remains unchanged and is not claimed to contain today's fixes.

## Future compatibility

[Ubuntu 26.10 Beta was released](https://discourse.ubuntu.com/t/ubuntu-26-10-stonking-stingray-beta-released/88662) on October 1. Its final release is expected October 15. This is a canary input only. No Stonking sources or packages were added to lts/26.04; this security baseline explicitly rejects a non-Resolute root.

## Environment limits

At review time C: had approximately 0.6 GB free. E: was accessible, but an earlier guest upgrade had hit Btrfs I/O errors when E: disappeared. This scheduled pass validates source, package construction and the read-only prepared-root gate. Full updated ISO generation and upgrade/reboot remain pending; the interrupted overlay is not reused or merged.

## Follow-up after the host restart

C: now has approximately 35 GB free, enabling a clean rebuild inside WSL ext4.
Eight official Resolute packages (the four security targets and version-coupled
OpenSSL/KCoreAddons companions) were resolved with isolated APT state against
the prepared root's dpkg database. APT authenticated the Ubuntu indexes with
the Ubuntu archive keyring; archive SHA256 values were matched to their index
records. `distro/security-updates.lock.json` pins every package URL, version,
architecture and hash. The builder installs the complete locked batch, blocks
service starts during that step and rejects unfinished dpkg configuration.
No host packages are installed by the resolver. The installed root retains the
lock for audit. A fresh-root build verifies the resolved dependency set before
the security gate, compression and export. Upgrade/reboot still needs VM QA.

The first clean-root attempt was stopped during extraction when Windows
paging and WSL storage growth left approximately 4 GB on C:. No package changes
or ISO export occurred in that attempt. Logs and partial scratch were retained.
Dropping the build environment's page cache restored memory headroom; Discord
and Spotify remain open at the user's request. The restarted clean build uses
a new 36 GiB ext4 filesystem in `E:/Cachuntu-build/work-26.10.1.2.ext4`, mounted
through a loop device. This is a regular virtual-disk file, not a physical disk.
Both extraction queues and compression have explicit memory/worker limits.
The official source ISO is read from E: and verified against the pinned hash.
Previous E: failures make final export verification and VM I/O checks necessary;
the interrupted upgrade overlay remains excluded.

## Build result

The fresh-root security baseline passed, so the lock installs the reviewed
fixes and their dependency companions successfully. The ISO attempt then
failed at final SHA256 reading with an E: I/O error; E: was absent at the next
check. This is an artifact-storage failure, not a completed release. The old
validated ISO is unchanged. See BUILD_STATUS.md for the recovery gate.

After reconnection, journal replay into a separate QCOW2 overlay recovered the
new ISO without changing the original virtual work image. Copy/readback SHA256
and all 693 checksum entries passed on C:. Selectively extracted package and
configuration metadata passed the security, defaults and branding checks.
UEFI live boot passed; the Try-to-desktop lifecycle defect requires the next
patch. Full installed upgrade/reboot is still pending.
