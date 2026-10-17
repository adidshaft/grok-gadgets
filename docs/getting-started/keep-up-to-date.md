# Keep your gadget up to date

Your gadget gets new firmware from the relay it connects to. You do not need a cable or a
computer, and there is nothing to install.

**Status:** Phase 12b ([ADR 012](../decisions/012-signed-updates.md)). On 17 October 2026 the
owner's kit took signed updates this way ([record](https://github.com/adidshaft/grok-gadgets/blob/main/docs/verification/ota-2026-10-17.md)). Nobody
else has repeated it yet.

## What you see

1. The gadget's screen shows `Update 0%`, then counts up. This takes about a minute on home
   Wi-Fi.
2. The gadget restarts by itself.
3. The screen shows `Online` again.

Your Wi-Fi settings, your claim and the names you gave the gadget stay.

## If something goes wrong

The gadget checks each update before it uses it. It refuses an update that the builder did
not sign, or that changed on the way.

If a new version does not come Online within 5 minutes, the gadget goes back to the version
it had. The screen then shows `Reverted` for a minute, then `Online`. Tell the person who runs
your relay.

| What you see | Do this |
| --- | --- |
| `Update 42%` for more than a few minutes | Check the gadget's Wi-Fi. A download that stops starts again from the beginning later. |
| You unplugged it during `Update %` | Plug it back in. It starts on the old version and downloads again. |
| `Reverted` | Nothing. The gadget works on its old version. The relay operator sees the report. |
| The screen is dark, but Grok Bot still reaches the gadget | Unplug it for 5 seconds and plug it back in. |

## Who sends updates

Only the person who runs your relay can send an update. Only updates signed with the
builder's key run on your gadget. You cannot start or refuse an update from Grok Bot yet.
