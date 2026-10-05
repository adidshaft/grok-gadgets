# Report a security problem

Use [GitHub private vulnerability reporting](https://github.com/adidshaft/grok-gadgets/security/advisories/new) or email [adidshaft@kyokasuigetsu.xyz](mailto:adidshaft@kyokasuigetsu.xyz).

Do not put credentials, household data or private exploit details in a public issue. We do not promise a response deadline.

## Information to include

- Affected version or commit.
- Minimum steps to reproduce the problem.
- Expected impact.
- Logs with private information removed.

Do not send secret values unless a maintainer requests them through a suitable private channel. Maintainers coordinate the fix and disclosure with the reporter. Do not publish exploit details before that coordination.

## Supported scope

The current 0.1.0 alpha includes the simulator, SDKs and implemented local transports. There is no public hosted gadget gateway. Each component documents its limits.

Development services use the local loopback interface. A networked device deployment needs unique credentials, credential revocation and appropriate host controls.

Enable simulation test controls only for the test. Remove them afterward. A cloud Grok Bot cannot run a local Mac file. Remote authenticated HTTPS/OAuth access is not implemented and needs review.

An MCP execution result does not prove that a physical device changed.
