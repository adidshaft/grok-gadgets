# Glossary

Use these terms consistently. Commands and API identifiers keep their exact spelling.

| Term | Meaning |
| --- | --- |
| Gadget | A device with declared capabilities, such as a display or button |
| Builder | A person who develops, configures or supplies a gadget |
| Operator | A person who runs the gateway and manages its access |
| End user | A person who uses a configured gadget through Grok Bot |
| Gateway | The service that exposes tools and routes commands to gadgets |
| Relay | The proposed gateway on an always-on host outside the Mac's daily path |
| SDK | Software development kit: reusable code for gadget applications |
| Capability | An action or value a gadget declares, such as `display.text` |
| MCP | Model Context Protocol: the tool interface used by Grok Bot |
| Native call | Grok Bot calls an MCP tool itself; no approved shell command is needed |
| Rehearsal | A local test through `grok-gadgets-gateway rehearse` |
| OAuth | The sign-in authorization used by the verified remote Grok Bot route |
| Tunnel | A connection that makes the gateway reachable over HTTPS; it does not replace authorization |
| TLS | Transport Layer Security: encryption and certificate checks for a connection |
| CA | Certificate authority: the issuer a device trusts for its server certificate |
| Provisioning | Writing device identity, connection and Wi-Fi settings to a gadget |
| Claim code | A proposed way to bind a gadget to an account; not available yet |
| Acknowledgement | A device's reply about command execution; not proof of a physical effect |
| State | Values reported by a device or simulator |
| Event | A recorded change, such as a button press; it does not wake Grok Bot |
| Simulator | Software that models a gadget without operating physical hardware |

[Documentation](../index.md) · [Architecture](../architecture/overview.md) · [Evidence levels](../public/how-we-verify.md)
