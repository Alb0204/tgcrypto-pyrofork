# Fork maintenance ledger

This fork of [Mayuri-Chan/tgcrypto-pyrofork](https://github.com/Mayuri-Chan/tgcrypto-pyrofork) is kept
alive because upstream stopped shipping (last commit 2025-10-25, no wheels for Python 3.15). Every
upstream item that has been looked at is recorded here so it is never triaged twice. Update this file
in the same commit as the work it describes.

Last upstream sync: `upstream/master` at `7884fa1` (identical to this fork's base).

## Upstream pull requests

Issues are disabled on upstream, so pull requests are the only intake.

| PR | Title | Decision | Notes |
|----|-------|----------|-------|
| [#1](https://github.com/Mayuri-Chan/tgcrypto-pyrofork/pull/1) | Support for Python >= 3.9 | Rejected | 3.9 was dropped on purpose in `91b865e` and is EOL since 2025-10. |
| [#2](https://github.com/Mayuri-Chan/tgcrypto-pyrofork/pull/2) | Don't install tests | Adopted in 1.2.9 | Bare `find_packages()` installed a top-level `tests` package into site-packages. |

## Upstream branches

| Branch | Decision | Notes |
|--------|----------|-------|
| `mac` | Superseded | 2024 CircleCI/aarch64 experiment on 1.2.7; merging it would drop 3.14 and revert the version. |
| `staging` | Superseded | 1.2.7 release candidate; everything useful landed on `master`. |

## Fork changes

| Version | Change |
|---------|--------|
| 1.2.9 | Every argument `Py_buffer` is released on validation errors too; `ctr256_*` never released `state` at all. Pinned by `tests/test_buffers.py`. |
| 1.2.9 | `malloc` failures raise `MemoryError` instead of dereferencing `NULL`; inputs over 4 GiB raise `ValueError` instead of being truncated to `uint32_t`. |
| 1.2.9 | Multi-phase module init declaring `Py_mod_gil` (no GIL needed) and per-interpreter GIL support. |
| 1.2.9 | Wheels for CPython 3.10-3.15 (+3.14t/3.15t) and PyPy on Linux/macOS/Windows, all architectures cibuildwheel offers, published as GitHub release assets rather than to PyPI (the PyPI name is upstream's). |

## Deliberately unchanged

- `ctr256_*` advances `iv` and `state` in place even when they are `bytes`. Pyrogram-based clients
  (kurigram's `tcp_abridged_o.py`) rely on that to keep the CTR stream position between calls, so
  it is part of the API.

## Telegram protocol check

Telegram's crypto needs are AES-256-IGE (MTProto 2.0), AES-256-CTR (obfuscated transports, CDN files)
and AES-256-CBC (Passport). Checked 2026-10-28 against core.telegram.org `/mtproto/description`
(IGE), `/mtproto/mtproto-transports` and `/cdn` (CTR) and `/passport` (CBC): no new primitive is
required. Re-check whenever a Telegram API layer mentions a new cipher.
