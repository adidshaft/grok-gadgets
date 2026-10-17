# Capability vocabulary

Grok Bot uses a gadget through its capabilities: commands it can send, events it can read,
and the state it can ask for. These names mean the same thing on every Grok Gadgets gadget.
Use them when they fit, so Grok Bot and the people who use it meet familiar words. Other
names are fine when none fits.

**Status:** Phase 12a ([ADR 013 §5](../decisions/013-builder-kit.md)). The ESP32 examples and
the Linux climate sensor use these names.

## Names

| Name | Kind | Arguments or data | Notes |
| --- | --- | --- | --- |
| `display.text` | command | `{"text": "1 to 32 printable characters"}` | OLED kit |
| `display.clear` | command | `{}` | OLED kit |
| `rgb.set` | command | `{"r", "g", "b": 0–255, "on": true}` | Canonical schema |
| `switch.set` | command | `{"on": true}` | State `switch.on`; off at boot and after a link loss |
| `servo.move` | command | `{"angle": 0–180}` | The acknowledgement comes after the move ends |
| `threshold.set` | command | `{"above_c": -40–85}` | Sets when `threshold.crossed` fires |
| `climate` | state | `temperature_c`, `humidity_pct`, `above_c` | One decimal |
| `threshold.crossed` | event | `{"reading", "value", "above"}` | Once per crossing |
| `button` | event | `{"pressed": true}` | Canonical; `state.button.pressed` too |

## Schemas

Each command takes a JSON Schema for its arguments. Grok Bot reads the schema and its
description. Keep `additionalProperties` false, and give numbers a range:

```json
{
  "type": "object",
  "description": "Move the servo to an angle; the result comes when the move ends",
  "properties": {"angle": {"type": "integer", "minimum": 0, "maximum": 180}},
  "required": ["angle"],
  "additionalProperties": false
}
```

An event's schema carries `"x-grok-gadgets-kind": "event"` (the SDKs add it). Describe the
data in its `description`.

## Descriptions

- One sentence, at most 300 characters. Say what happens in the room, not in the code: "Turn
  the desk fan on or off", not "Set GPIO5".
- Say the limits that matter to a person: the range, the time it takes, and what happens on a
  link loss.
- Never put an instruction to Grok Bot in a description. The gateway shows it as information
  from the gadget.

## Safety

- A command must be safe to repeat. A retry with the same command ID never runs twice, but a
  new request may repeat it.
- Put actuators in a safe state at boot and on shutdown.
- Mains voltage is out of scope for every example. The switch example is for low-voltage loads
  only.
