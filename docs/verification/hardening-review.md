# Independent correction review

Reviewer: bounded GPT-6 Astra Medium agent, read-only source review and independently executed tests. This is independent agent review, not independent human reproduction.

| Finding / acceptance | Disposition | Corrected commits / evidence |
| --- | --- | --- |
| ESP ACK repeats mutate retained JSON | Resolved; immutable parse, failure preservation, repeated success/failure/interleave/FIFO/reboot | ESPad89e7a; actual consumer four repeats;3CTest and C124 compilation rerun |
| Input-only capabilities silently callable | Resolved; negative official MCP calls leave LED unchanged and discovery distinguishes contracts | Gatewaye0b7256;21tests and real local MCP/TCP |
| Other devices evict event deduplication | Resolved; per-device/boot256 windows and bounded64-device lifecycle | Gateway7a4ba40; multi-device/reconnect/boot regressions |
| Installed custom factory unreachable | Resolved; explicit trusted file route, fresh site-packages macOS/Linux | Linuxad3bb53; actual documented registration/command/state |
| Failed activity state not persisted | Resolved; validated atomic result and owner isolation through actual file/build | Hub0078a5a; repeated failure and replacement-failure tests |
| Docs are escaped/unusable links | Resolved; safe semantic Markdown, source-relative/fragment validation, allowlist, bounded accessible diagrams | Huba9550ab;35public docs and21checkout references independently reviewed |
| P2: skipped refresh leaves old LIVE label | Accepted and resolved | Hubbddd5b9; all12website tests independently pass, including stale/future/corrupt/fixture builds |
| P2: annotated dataclass factory fails | Accepted and resolved | Linux7d0f82b/be66ea4; unique sys.modules registration+rollback, five CLI regressions and fresh installed ordinary/dataclass acceptance independently pass |

H5 source correctness review closed after correction reruns on 4 October2026. No material in-scope finding remains. Reviewer inspected the actual offline Linux log: both factory variants passed,20collected/15executed and5optional source-gateway integrations skipped; separate installed gateway transport exercised. Actual Linux was executed by the implementation owner; reviewer did not independently rerun the container after its local image lookup failed. Gateway/ESP source/build review remains applicable because runtime sources did not change afterward.

H6 package/provenance certification passed independently on the concrete candidate below. No actual Grok, physical board, live home device, second human or publication claim follows from this review.

## H6 assembled candidate certification

Independent Astra reviewed candidate20261004T165602-1791132962841338000, source hub9daf82d, manifestSHA256d1d4b792c34d97fe24217333c7f13c59fc2b7ada09a8049df20c0239f340c5ef. All25hashes/sizes matched; --require-current exactarchive/runtimepackage/completebundle/firmwareancestor checks passed.11integrity regressions independently passed. Extracted47pagewebsite passed local links/fragments, privacy exclusions, corrected guides, unavailableactivity and10toolkit disclosures. Fresh candidate Gateway/Linux wheels ran both archived documented/dataclass examples and the installed officialMCPdemo; HA candidate separately installed and archivedfixtureprobe passed.

An exploratory combined environment for allthree Python wheels failed because existing gatewayMCP1.26 and HAMCP2.3 pins conflict. Supported component environments are separate and passed; no shared-environment compatibility is claimed. Final closure is evidence/documentation only; finalmain candidate must be regenerated and verified against exact currentHEADs using the same unchanged reviewed tools.

## S1 export-to-kit independent review

Read-only GPT-6.1 Sol High reviewed24729e0 for HARD-SIM-EXPORT-001. Node6/6, kit4/4, freshness gate and actual scene.js VM export/copy/denied-clipboard/unavailable-download probes passed. Independently matched all six acceptance.json file hashes/sizes; custom236-byte my-light.json equals actualbrowserdownload and is outside protected inventory; default bytes match both ZIP and inner manifest. Fresh installed -B -I probe validates actual custom file and resolves package from kitvenvsite-packages. Parsed MCP evidence confirms offline rejection, reconnect restored state/new boot/session, blue/status/readback,125ms requested delay/130.612msobserved, button edges/cursor, off, physical/Grokfalse. No material functional findings.

Dispositions: test dry-run ignores --config; documented that it proves filename/default integrity only, supplemented with actual fresh --install/MCP run. Stale inprogress verification note replaced by complete simulator-export-onboarding.md. Optional suggestion to extract UI transport for lighter fallback tests was not required for this filename bug; browserused pure export regression and VM/manual UI evidence retained. Agentreview is not independent human reproduction. Final currentHEADpublication certification follows closure commit.
