# ThryveCTF 2026 — Nova Vault (DFIR)

**Challenge:** Nova Vault — 500 pts, 9 solves
**Category:** Forensics / DFIR
**Flag:** `Thryve{n0v40x_k33p4ss_m3m0ry_sh4rd5_l34k3d_th3_v4ult_k3y_wh1l3_4ws_4f4n3h_0m4r_4nd_m0h_ch4s3d_th3_r0t4t3d_h1st0ry_4cr0ss_th3_cr4sh_4rt1f4ct_2026}`

## Method
1. **Hints from `ops-chat.log`:** master keys start with `N`; recycle-bin entry rotated but **history not scrubbed**; REDACTED fields are decoys.
2. **Dump analysis:** `NovaVault_DMP.dmp` is a crafted minidump. Master key encoded as `N`×`\xcf\x25` marker pairs + char + `\x00\x00\x00` (pair count = char index). Decoded: `0va0x_Aws_MemorySplit_2026!` (a second garbled region is a decoy).
3. **Key assembly:** prefix `N` → `N0va0x_Aws_MemorySplit_2026!`.
4. **Vault open:** `pykeepass.PyKeePass(kdbx, password=key)`. All visible entries are decoys (incl. fake flag in `old-breakglass-linux`).
5. **Flag:** in the **History** of Recycle Bin entry `vault-recovery-backdoor` (pre-rotation password).

## Key insight
KeePass entry History preserves old field values after rotation — check history of recycled entries. Crafted dumps can hide keys in count-encoded byte patterns.

See `D:\CTF\data\research\forensics\keepass_vault_recovery_crash_dump.md` for the reusable technique.