# Vendored ProPresenter `.proto` definitions

| | |
|---|---|
| Source | <https://github.com/greyshirtguy/ProPresenter7-Proto> |
| Path in source | `autogen-proto/` |
| Commit | `bf6325d243897a6c64dde46eec803ec29f5f8569` (2026-08-13) |
| Licence | MIT — Copyright (c) 2023 greyshirtguy (see `LICENSE.greyshirtguy`) |
| ProPresenter version | `21.4,352583705` (the repository's own `rv/version.txt`) |

These definitions are **unofficial and reverse-engineered**. They are not published or
supported by Renewed Vision.

The vendored version matters: `rv/version.txt` records ProPresenter **21.4, build
352583705**, which is byte-for-byte the `application_info` written by the reference
exports in `core/tests/reference/`. Field numbers used by the writer are therefore
validated against a real file produced by the same build, not inferred.

Regenerate the Python bindings with:

```
python scripts/generate_proto.py
```

Generated modules land in `generated/` and are committed so that a checkout builds
without `grpcio-tools`.
