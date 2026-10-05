# Preserved implementation and launch history

This is the source snapshot after local preparation was integrated into main. The commit containing this summary follows; exact final main HEADs and source/recovery hashes are in the selected latest candidate and approval packet. No squashing, history rewrite or public push occurred. Recovery bundles remain private.

| Repository | Snapshot HEAD | Incremental commits |
| --- | --- | ---: |
| grok-gadgets | `049aa771bc2ce0597b6d6635886df743c4de8b5d` | 48 |
| grok-gadgets-gateway | `71cfecbaf1120b27e1956384861efda5f5a3eef6` | 14 |
| grok-gadgets-linux-sdk | `9c13fef60d3dd0d5feb2973bd7e51bfacfb48dec` | 12 |
| grok-gadgets-esp32-sdk | `db3fe8755364f74478bf576d9d57aabe4684eb62` | 14 |
| grok-gadgets-home-assistant | `3c8d8adba31918b051dbdbf2343f9fa6e26dedce` | 8 |

Launch preparation hub commits:4451f0a baseline;f1cff58 owner/policies/ready queue;8b362f7 resumable migration;7ac61fd source-race gate;e1a9948 newcomer docs/vectors/site;e063a38 pinned CI/forms/rulesets;3bb66cc history/tree-ref audit and standalone fixtures;4ae0072 source-archive reference support;f4ad5f9 download-pair rollback;4876c8b stage/gate reconciliation;3e2d066 bounded test trace;6fb967f public-subset/activation guide;049aa77 local stage closure and fast-forward main integration.

Gateway:dd4f50a docs and18824b0 closure,1a6c876 read-only CI,71cfecb issue forms. Linux:94b9fb9 docs/f1468b4 closure,27af8c8 CI/9c13fef forms. ESP32:ff954cc docs/a02c4e8 closure,fe7e505 CI/0a36948 forms,db3fe87 final compilation record. HA:fe2b93f docs/706c2be closure,2aa4a25 CI/3c8d8ad forms. These launch changes preserve verified runtime interfaces and license/notice bytes.

Use `git log --oneline --graph main` in each checkout for complete maintained history. Original alpha and hardening commits remain reachable. Main pushes expose historical paths and personal author metadata; the history/asset report records that explicit approval gate. Source archives contain selected current trees only; private recovery bundles additionally preserve local refs. The separate final approval packet gives runnable paths, exact hashes, verified check logs and remaining external gates.
