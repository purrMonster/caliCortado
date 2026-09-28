# Authorization boundary — CAL-004

Status: chosen contract design with offline policy fixtures; no production authentication implementation. [Runbook RB-20260927-06](../runbook.md) records why. APIs use audience-bound opaque bearer grants verified through authenticated [RFC 7662 introspection](https://www.rfc-editor.org/rfc/rfc7662). A broker/session adapter must translate authenticated human/machine/device identity into bounded destination grants. CAL-007 owns protocol interoperability, credential custody, revocation and live tests.

## Caller matrix

| Destination | Permitted actor | Required scopes |
|---|---|---|
| capture | display, registered device | `capture:create` |
| data | capture | `notes:create` |
| data | indexer | `notes:read`, `changes:read` according to operation |
| data | search | `notes:read` |
| data | backup | `snapshots:read` |
| embeddings | indexer, search | `embeddings:generate` |
| index | indexer | `index:write` |
| index | search | `index:query` |
| search | display, answers | `search:query` |
| inference | answers | `inference:generate` |
| answers | display | `answers:generate` |
| any custom service readiness | monitor | `health:read` for that audience |

The exact operation requirements are in the OpenAPI extensions. Actor is an authenticated application/device identity, not a claim clients may self-select. Subject identifies the originating authorized human or a narrowly provisioned system principal. Every grant binds issuer, audience, active state, expiry, scopes and allowed vaults. Receiving services authenticate the caller and validate the destination grant; the broker binds delegation to the authenticated actor. Possession of a broad network credential must not manufacture another user's subject/vault grant.

The fixture `Identity` object represents an already authenticated internal result. It is never an HTTP request body, signed token, production introspection response or trustable proxy header. Tests construct it directly only because the harness is in-process with no listener. Do not expose `authorize_fixture` as authentication middleware. Production issuer comes from trusted configuration; `.test` issuer is fixed solely for the fixture suite.

## Propagation and isolation

1. Human login ends at the display-side session adapter. Protect session cookies with Secure/HttpOnly/SameSite, CSRF protection and origin validation on state-changing routes. UI framework, cookie domain and exact IdP flow remain CAL-007/CAL-042 design work.
2. The authenticated display requests a short-lived destination grant limited to the subject's permitted vaults. Tokens remain server-side; no machine credentials in frontend bundles/local storage.
3. Capture, answers and search obtain separately audience-scoped downstream grants from the broker after authenticating themselves. Scope/vault intersection can only narrow upstream authority. Never forward an answers-audience token to data or inference unchanged.
4. The destination validates trusted issuer, active state, expiry, intended audience, actor, required scope and every accessed vault/object owner. Snapshot/request IDs and cursors are not authority. Revocation/identity outage fail closed; CAL-007 specifies any bounded cache window and tests it before use.
5. Indexer/backup get explicit system grants restricted to opted-in vaults. They never inherit wildcard household access. Backup restore/maintenance credentials remain separate from ordinary writer credentials.

Traefik strips untrusted identity headers, restricts reachable routes and verifies TLS. Every API still authorizes its own requests. Service ports must not be reachable around ingress. Browser origin checks complement authentication; CORS does not replace it. Keep third-party sync credentials separate from custom API grants and test native client constraints in CAL-009.

## Denial evidence and remaining gates

The offline suite rejects wrong audience, missing scope, forbidden vault, wrong actor/issuer, expired/revoked grants, spoofed body identity and malformed requests. Multi-vault snapshot requests must authorize every vault. These are fixture-policy results, not penetration tests or proof of authenticated introspection.

Before live or valuable data: CAL-007 must demonstrate real issuance/delegation, expiry/revocation, outage, forged headers, service impersonation, login/CSRF behavior, device credentials and rotation. CAL-009 must prove encrypted sync/bridge compatibility. CAL-032/CAL-040 must test stale-source and excluded-note denial. E02 must test TLS, hostname and direct-port isolation. If the IdP cannot support the selected broker flow, record the constraint and revise the adapter design while retaining destination authorization; do not weaken to user-supplied headers.

No tokens/private keys/personal notes belong in Git or test logs. Example configuration contains environment references only. Notes/prompts are untrusted data, and inference has no write/admin tools. Recovery must preserve authorization and capture identity state while separately restoring credentials from user custody.
