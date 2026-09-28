# Synthetic fixtures

Everything here is invented for E01. `examples.json` provides one example per shared schema plus fake already-authenticated identity and model response values. API operation examples include structured errors. The telescope sentence is synthetic; hashes for that sentence use its exact UTF-8 bytes without a trailing newline.

[demo vault](vault-demo/inbox/telescope.md), [excluded note](vault-demo/_noai/excluded.md) and [denied vault](vault-denied/private.md) define later integration inputs. The current demo validates JSON fixtures only; it does not index these Markdown files or prove exclusion handling. Preserve that distinction when adding CAL-032 tests.

The fixed fixture clock is epoch 1800000000; expiry 2000000000 is synthetic. No value is an actual bearer token or production credential. [Run checks and the offline demo](../docs/development.md).
