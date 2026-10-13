# Troubleshooting

Find the symptom first. Check one connection at a time.
Keep tokens, household data and real hostnames out of public reports.

| Symptom | Check | Next step |
| --- | --- | --- |
| Grok Bot reports 502 | Is the Mac awake? Are the gateway and tunnel running? | Restore the current route. Failed requests during sleep do not queue. See [hosting](hosting.md). |
| Sign-in waits for approval | Did the gateway operator approve the matching code? | Follow [Connect your Grok Bot](connect-grok-bot.md). Never share a sign-in code publicly. |
| No tools or authorization fails | Does the server use the configured HTTPS URL and OAuth? | Use the connection guide. Do not substitute an unverified bearer-header setup. |
| OLED shows `Gateway...` | Is the board on the expected network? Is the private LAN listener available? | Follow the gateway [always-on guide](https://github.com/adidshaft/grok-gadgets-gateway/blob/main/docs/always-on.md). |
| OLED is blank | Are power and wiring correct for the tested board and display? | Disconnect power before moving wires. Compare the [kit wiring](experiment-kit.md). |
| Command reports success but nothing changes | Is the listed device simulated? Did the physical device acknowledge the command? | Pair the log result with a direct observation. See [how we verify](../public/how-we-verify.md). |
| No button events | Did the board disconnect or restart? Does the cursor exclude the event? Did history expire? | Repeat the guide's button step and record the observation. A button cannot wake Grok Bot. |
| Usage shows no percentage change | Does the account page round usage to whole percent? | Do not save a zero-rate calibration. Follow [track usage](track-usage.md). |
| Another board or home system fails | Is that exact setup verified? | Check [project status](../public/support-matrix.md). A compiled example is not a physical test. |

## Report a result

Include the component versions, your setup type, the failed step and the result you expected.
Separate software replies from what you observed on the hardware.
Remove tokens, sign-in codes, Wi-Fi names, hostnames, addresses and personal data from logs or screenshots.

Use [tester issue #185](https://github.com/adidshaft/grok-gadgets/issues/185) for a kit reproduction.
Use [GitHub Issues](https://github.com/adidshaft/grok-gadgets/issues) for a reproducible defect.

[Documentation](../index.md) · [Glossary](../reference/glossary.md) · [Current support](../public/support-matrix.md)
