# Website verification — 4 October 2026

Python static build passes with 48 pages after canonical docs/community import. Every internal link references generated content; public repository URLs are intentionally absent. Default project activity is unavailable. Synthetic fixture build displays FIXTURE and escapes a malicious release-name script tag. Three activity tests cover issue/PR distinction, contributor deduplication, active-window eligibility, cache owner isolation/failure, and invalid owner rejection.

In-app browser: desktop 1265px and narrow390px reviewed visually; no measured horizontal overflow (document scroll width380 vs viewport390). Keyboard Tab reached the visible Skip to content link. Reduce motion button set aria-pressed=true, body reduced flag, and LED computed animation-name:none. OS prefers-reduced-motion CSS also suppresses animation; OS preference itself was not changed. Motion is one brief CSS entrance and a small LED pulse; no heavy animation dependency or remote asset load.

Screenshots website-desktop.jpg and website-mobile.jpg record local UI. The local preview binds127.0.0.1:4173. No deployment or live GitHub fetch occurred. Website uses original CSS illustration and no third-party proprietary visual assets.

Final browser check after motion fix: computed html scroll-behavior:auto and LED animation-name:none with explicit reduction enabled. Updated screenshots capture current local alpha claims.
