# Static website deployment preparation — inactive

The prepared manual main-only workflow is `.github/workflows/pages.yml`; its dependent deploy job uses only the tested site artifact. Exact pinned sibling sources, integrated acceptance, simulator freshness/integrity and project-prefix/deep-404 checks precede upload. No schedule or deployment has been activated.

Review `activation-guide.md` for destination, environment/token permissions, real hosted context/readback and rollback. The build preserves the last-good preview on failure and uses content-addressed kit links. After a reviewed compatibility change, build/test the new kit and site before manual promotion. Already downloaded kits are frozen copies.

The planned URL is https://adidshaft.github.io/grok-gadgets/. Live public HTTPS, canonical/social/deep-link/download behavior require verification after separate publication approval. The final approval packet identifies exact candidate/source/site hashes and excluded private/binary assets. Static hosting runs neither the gateway nor a recognition/identity backend.
