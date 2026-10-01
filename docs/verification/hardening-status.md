# Hardening checkpoint

H0 baseline passes; tracking commit pending. H1–H7 are not complete. No account/device/public actions authorized.

Starting repository inventory:

```json
[
  {
    "repository": "grok-gadgets",
    "head": "2e8d8df75a0d8f22e85f74e5ffb8339d4a4052f6",
    "branch": "main",
    "dirty": [
      "?? assets/",
      "?? docs/hardening-plan.md"
    ],
    "remotes": []
  },
  {
    "repository": "grok-gadgets-esp32-sdk",
    "head": "585adda7f854fd33f2d17261d2b1cfa7ec3b1179",
    "branch": "main",
    "dirty": [],
    "remotes": []
  },
  {
    "repository": "grok-gadgets-gateway",
    "head": "4cf42fffa32afa2e5ad022e3fa4797f474ba10a9",
    "branch": "main",
    "dirty": [],
    "remotes": []
  },
  {
    "repository": "grok-gadgets-home-assistant",
    "head": "a8b2370b7e82e136511b6299e1317eb80915d012",
    "branch": "main",
    "dirty": [],
    "remotes": []
  },
  {
    "repository": "grok-gadgets-linux-sdk",
    "head": "256a07e23ac4a4393066e0492847276849ac3348",
    "branch": "main",
    "dirty": [],
    "remotes": []
  }
]
```

Next exact actions: assign gateway HARD-GW-001/002, ESP32 HARD-ESP-001, Linux HARD-LIN-001 with exclusive repositories; reproduce before fixing. Coordinator owns hub status and website. Component issue additions are intentional uncommitted H0 tracking. Source assets/ remain untouched.
