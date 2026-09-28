# Access and ownership — CAL-002

Recorded 2026-09-27. References identify custody, never secret values. Decisions are in [runbook](../../runbook.md).

| Action | Authority / owner | Current boundary |
|---|---|---|
| Product and local E01 implementation | User requested E01 | Local source, fixtures, documentation and checks authorized |
| Read-only host inspection | Operator-defined authorized targets | Re-establish the private target inventory before further host access |
| Domain | Environment-provided DOMAIN | Naming authorized; DNS mutations and certificate/account changes not yet authorized |
| iPhone/Mac setup and human tests | User | Supply documented device procedure when CAL-009/CAL-014/CAL-015 are ready |
| Node sudo | User | No sudo executed by assistant; user runs required approved steps |
| Configure/restart/deploy nodes | No standing grant recorded | Block live mutations pending concrete reviewed change and authorization |
| Downtime window / spending | Unset / no spending grant | No purchased hardware/services or assumed downtime |
| Remote creation/publication | Not authorized | Local Git only; no remote or publication |
| Credential provisioning/rotation | User custody | Password manager/existing SSH context; no secret contents in tracked files |
| Live Vikunja task updates | User authorized E01 completion and next-story pickup | Replacement token works; E01 completion and CAL-005 pickup written and read back successfully |

## Deployment gates by component

| Stories requiring environment/device work | Candidate target and specific gate |
|---|---|
| CAL-005–008, CAL-046 | Existing edge/identity hosts; reconcile infrastructure history, review routes/DNS/auth changes and obtain deployment grant |
| CAL-009–013 | data-compute-host data role; authorize disposable prototype deployment, user device setup and pinned sync/bridge compatibility |
| CAL-014–017 | User iPhone/Mac plus capture host candidate data-compute-host; user setup, tested sync and ingestion deployment grant |
| CAL-018–021 | backup-host; independent healthy destination, recovery/retention choice and explicit backup deployment grant |
| CAL-022–025 | Existing network hosts and user clients; selected private transport, network change authorization, user device test |
| CAL-026–033 | data-compute-host compute/index candidates; benchmarks and deployment grant; preserve independent API ownership |
| CAL-034–037 | Inference role; working authorized access, measured hardware and owner availability/latency decision |
| CAL-038–041 | Compute role candidate data-compute-host; identity/search/inference prerequisites and deployment grant |
| CAL-042–045 | Independently selected display host; private DNS, identity and deployment grant |
| CAL-047–050 | At least separate authorized hosts/VMs for data, compute, AI and display; restore/relocation authorization and actual observation windows |

All live deployment work is explicitly blocked by the missing mutation grant; source and synthetic fixture work can proceed where story dependencies permit. No extra tracker is introduced. Resolve each gate in its owning story and record evidence in the runbook.

Infrastructure changes must be committed and pushed in the infrastructure repository, then nodes pull `main`; no direct copying of configuration. Node-local untracked files must be understood before a pull/deployment. Calicortado may link to implementation evidence there; infrastructure must not gain Calicortado references.
