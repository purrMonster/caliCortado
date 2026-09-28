# DNS discovery compatibility fixture

This file supports the Calicortado preparation tests without requiring another checkout. `dns_route_discovery.py` contains the route-discovery constants and `records` / `routes_in` functions snapshotted from the existing infrastructure DNS generator on 2026-09-29. AST serialization removed comments and formatting; the logic was preserved. It is a test fixture, not a production generator or authority for live DNS.

Source-file SHA-256: `ef4e8f7a80b3488f8e6041e5712973f88302afe185a02f091ee3a8d33dd65474`.

The five preparation tests exercise domain discovery, duplicate-owner rejection and the A/B/removal record delta against this snapshot. Passing these tests establishes compatibility with the captured implementation only. Before deployment-ready configuration is promoted to infrastructure, rerun the same cases against that repository's then-current generator and review drift. Never use this fixture to write live resolver settings.
