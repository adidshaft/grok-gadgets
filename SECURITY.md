# Security reporting

Do not put credentials, household data or exploitable private details in a public issue. Email [adidshaft@kyokasuigetsu.xyz](mailto:adidshaft@kyokasuigetsu.xyz) privately. GitHub private vulnerability reporting will be enabled and verified after repository creation; until then use email. We do not promise a response deadline.

The supported alpha scope is the current 0.1.0 alpha simulator, SDKs and implemented local transports. No public hosted gateway exists. Include the affected version/commit, minimal reproduction, impact and redacted logs. Send secret values only if explicitly requested through a suitable private channel. Maintainers coordinate a fix and disclosure with the reporter; avoid publishing exploit details before that coordination.

Local services use loopback in documented development tests. Networked device deployments require unique credentials, revocation and appropriate host controls. Simulation test controls are opt-in and should be removed afterward. A cloud Grok Bot cannot run a Mac path; authenticated remote HTTPS/OAuth remains unimplemented and needs review. MCP execution does not prove physical effects. Each component documents its particular boundaries.
