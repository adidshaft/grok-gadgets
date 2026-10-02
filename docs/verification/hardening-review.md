# Independent correction review

Reviewer: bounded medium-effort agent, read-only source review and independently executed tests. This is independent agent review, not independent human reproduction.

| Finding / acceptance | Disposition | Corrected commits / evidence |
| --- | --- | --- |
| ESP ACK repeats mutate retained JSON | Resolved; immutable parse, failure preservation, repeated success/failure/interleave/FIFO/reboot | ESP3e8ccff; actual consumer four repeats;3CTest and C124 compilation rerun |
| Input-only capabilities silently callable | Resolved; negative official MCP calls leave LED unchanged and discovery distinguishes contracts | Gateway4bb6d87;21tests and real local MCP/TCP |
| Other devices evict event deduplication | Resolved; per-device/boot256 windows and bounded64-device lifecycle | Gateway85548ea; multi-device/reconnect/boot regressions |
| Installed custom factory unreachable | Resolved; explicit trusted file route, fresh site-packages macOS/Linux | Linuxbeb69c1; actual documented registration/command/state |
| Failed activity state not persisted | Resolved; validated atomic result and owner isolation through actual file/build | Hub0078a5a; repeated failure and replacement-failure tests |
| Docs are escaped/unusable links | Resolved; safe semantic Markdown, source-relative/fragment validation, allowlist, bounded accessible diagrams | Huba9550ab;35public docs and21checkout references independently reviewed |
| P2: skipped refresh leaves old LIVE label | Accepted and resolved | Hubbddd5b9; all12website tests independently pass, including stale/future/corrupt/fixture builds |
| P2: annotated dataclass factory fails | Accepted and resolved | Linux89478e5/ce897ee; unique sys.modules registration+rollback, five CLI regressions and fresh installed ordinary/dataclass acceptance independently pass |

H5 source correctness review closed after correction reruns on 4 October2026. No material in-scope finding remains. Reviewer inspected the actual offline Linux log: both factory variants passed,20collected/15executed and5optional source-gateway integrations skipped; separate installed gateway transport exercised. Actual Linux was executed by the implementation owner; reviewer did not independently rerun the container after its local image lookup failed. Gateway/ESP source/build review remains applicable because runtime sources did not change afterward.

H6 package/provenance certification passed independently on the concrete candidate below. No actual Grok, physical board, live home device, second human or publication claim follows from this review.

## H6 assembled candidate certification

Independent Astra reviewed candidate20261004T165602-1791132962841338000, source hub9daf82d, manifestSHA256d1d4b792c34d97fe24217333c7f13c59fc2b7ada09a8049df20c0239f340c5ef. All25hashes/sizes matched; --require-current exactarchive/runtimepackage/completebundle/firmwareancestor checks passed.11integrity regressions independently passed. Extracted47pagewebsite passed local links/fragments, privacy exclusions, corrected guides, unavailableactivity and10toolkit disclosures. Fresh candidate Gateway/Linux wheels ran both archived documented/dataclass examples and the installed officialMCPdemo; HA candidate separately installed and archivedfixtureprobe passed.

An exploratory combined environment for allthree Python wheels failed because existing gatewayMCP1.26 and HAMCP2.3 pins conflict. Supported component environments are separate and passed; no shared-environment compatibility is claimed. Final closure is evidence/documentation only; finalmain candidate must be regenerated and verified against exact currentHEADs using the same unchanged reviewed tools.
