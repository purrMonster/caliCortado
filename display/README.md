# Calicortado display — E11

Status: ownership skeleton only. Owns responsive Capture/Search/Ask views, source navigation and a server-side session adapter. Receives configured capture/search/answers URLs; never database, model-runtime or filesystem access. Human session and delegation follow [security](../docs/security.md); framework choice is deferred to CAL-042.

Develop against [fixtures](../fixtures/README.md) and [contracts](../docs/contracts.md). Device-sized UX, CSRF/session integration, reconnect/cancellation, source links and separate-host placement need real tests in CAL-042–045. Deployment/recovery/upgrade instructions are written with that implementation; current fixture checks are in [development](../docs/development.md). No frontend has been built yet.
