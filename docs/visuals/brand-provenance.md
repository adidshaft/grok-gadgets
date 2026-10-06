# Community identity provenance

The user supplied the original Grok Gadgets raster logo and icon. The source generation notes describe built-in image generation followed by macOS raster resizing/cropping; these are PNG artwork, not vector masters. The brief requested an original monochrome community identity with a bot/device motif, distinct from the official product/company marks. The reviewed brand masters are published in [`docs/visuals/brand/`](https://github.com/adidshaft/grok-gadgets/tree/main/docs/visuals/brand) (see below).

The approved website copies are unchanged: `website/media/grok-gadgets-icon.png` (SHA256 `6d0b4c7cd981d7895bc1763fc55d1c9dae13ad27dbd9c9398ead8a8690b8f56f`) and `website/media/grok-gadgets-logo.png` (SHA256 `e984b8c1dcffeb9517b9e4d34effcb5178a95352f249765aca6d64fe1f2000b3`). Original project artwork is distributed under the project's Apache-2.0 terms; that license grants no trademark rights.

Official Grok and SpaceXAI reference marks have separate origin/checksum records in [media provenance](../../website/media/provenance.json) and [third-party notices](../../THIRD_PARTY_NOTICES.md). Their owner's usage guidelines apply; being publicly downloadable does not make them Apache-licensed. Retained project names and any public branding require a recorded brand-review disposition before activation.

## Repository banner and navigation badges

`project-banner.png` is an unchanged copy of the user-supplied `banner-wide-master.png`. It includes the original project logo and name. SHA-256: `cfd861189767d4b8e970ff6dc24089467254e3d2047cb168569087fcc5e3a32c`. It was visually reviewed before publication. No source artwork archive or generation metadata is included.

The four `badge-*.svg` files are original project navigation graphics. They use static labels and do not claim live counts or passing CI. Their links lead to the relevant status, license, checks and contribution pages.

## Website share preview

The current `website/media/grok-gadgets-share-v3.png` card is 1200×630. The Grok Gadgets project logo and large two-line name lead the composition. A single oversized outline Grok Bot face sits behind the website-inspired wireframe hardware scene. Navigation, numbered node labels and other small copy were removed; the lower-left open-source/non-affiliation note remains.

Built-in image generation used the user-supplied website screenshot, original project logo, and two user-supplied round-face Grok Bot references. A second edit removed a duplicate Bot face and connected the remaining face to the conceptual gateway. macOS sips normalized the final dimensions. The supplied round-face artwork supersedes the desktop app icon used in v2; it is not represented as an independently verified official asset. The hardware scene illustrates the intended architecture and is not evidence of a live connection. The checksum and sources are recorded in `website/media/provenance.json`. Versions 1 and 2 remain available for caches requesting their earlier URLs.

## Brand masters (HUB-RED-001)

Published on 6 October 2026 after an individual review of each file: artwork only, no
personal data. The PNGs keep their C2PA content credentials, which record generation with
ChatGPT's image model (`gpt-image`), and plain EXIF size fields. The source zip is not
published because it only duplicates these files. Prompts and resizing steps are in
[generation-notes.txt](https://github.com/adidshaft/grok-gadgets/blob/main/docs/visuals/brand/generation-notes.txt). The Reddit avatar and banner are the
files applied to r/GrokGadgets; `banner-wide-master.png` is byte-identical to
`project-banner.png`.

| File | Size | SHA-256 |
| --- | --- | --- |
| `banner-master.png` | 2032×774 | `3de90811410943145ddfe6c8e95986f09a9ce3fb59d2f6856e1253110a5e5da0` |
| `banner-wide-master.png` | 2032×243 | `cfd861189767d4b8e970ff6dc24089467254e3d2047cb168569087fcc5e3a32c` |
| `icon-64.png` | 64×64 | `6d0b4c7cd981d7895bc1763fc55d1c9dae13ad27dbd9c9398ead8a8690b8f56f` |
| `logo-1024.png` | 1024×1024 | `e984b8c1dcffeb9517b9e4d34effcb5178a95352f249765aca6d64fe1f2000b3` |
| `logo-master-1254.png` | 1254×1254 | `44a417607cab81cf752ee713026f023e3cee9c2c72c9fadf35ace23ac58724b6` |
| `reddit-avatar-256.png` | 256×256 | `fc473005ae248afea553ebcb159a2dcfd9ad56bd432f031e9eb6245ef02d6def` |
| `reddit-banner-1072x128.png` | 1072×128 | `35be337db5608253ded8db108ed497decfa7bf2c3402ad174bc211062cad598f` |
