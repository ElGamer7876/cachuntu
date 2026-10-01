# Ubuntu review — 2026-10-01

Source candidate: Cachuntu 26.10.1.2, Ubuntu Resolute 26.04 LTS. The same-day patch increments for an urgent security release gate; no new ISO has been produced.

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
