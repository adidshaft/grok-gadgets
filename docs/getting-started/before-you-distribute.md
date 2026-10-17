# Before you distribute a gadget

**This is not legal advice.** It lists rules that may apply when you give or sell a gadget
that you built with Grok Gadgets. The rules depend on the country, the product and how you
supply it. The rules also change. Check them with the regulator or a qualified adviser before
you distribute anything.

**Status:** Phase 12b ([ADR 012](../decisions/012-signed-updates.md)). Sources were read on
14 October 2026. The project owner reviewed it on 17 October 2026. The project does not sell
gadgets and does not give compliance support.

## Who this is for

You build a gadget with an ESP32 radio module, for example the OLED kit. Then you give it or
sell it to someone else. If you market it under your own name or brand, you are probably the
**manufacturer**. The rules below are then yours to meet, not the module maker's and not this
project's.

A gadget that stays with you, on your own desk, is a different case. This note is about
gadgets that leave your hands.

## 1. The radio module is approved; your product is not

- The ESP32-S3-WROOM-1 module holds FCC, IC (Canada), CE, SRRC, KCC, MIC, NCC, ANATEL and
  Wi-Fi certificates ([Espressif certificates](https://www.espressif.com/en/support/documents/certificates?keys=ESP32-S3-WROOM-1)).
  Espressif lists no WPC or BIS entry for India.
- A module approval covers the transmitter only. You must follow the module's integration
  instructions, for example the antenna clearance.
- **USA.** FCC modular approval (KDB 996369) covers the module. Your product still needs its
  own Part 15 Subpart B check for unintentional emissions, usually by a Supplier's
  Declaration of Conformity (SDoC). The label says "Contains FCC ID:" with the module's ID
  ([FCC KDB 996369](https://www.fcc.gov/sites/default/files/36-KDB-996369-%E2%80%93-Modules-TCB_April_2023.pdf),
  [SDoC](https://transition.fcc.gov/oet/ea/presentations/files/nov19/12-SDoC-JS.pdf)).
- **Canada.** Host equipment with a certified module "does not usually require
  certification". It needs a host label as RSS-Gen section 9.4.4.2 describes
  ([RSS-Gen](https://ised-isde.canada.ca/site/spectrum-management-telecommunications/en/devices-and-equipment/radio-equipment-standards/radio-standards-specifications-rss/rss-gen-general-requirements-compliance-radio-apparatus)).
- **India.** Licence-exempt radios use the ETA by self-declaration. You can reuse a module's ETA. Fees and customs steps are not verified here.

## 2. Security rules for connected products

- **European Union, radio equipment.** Since 1 August 2025, Delegated Regulation 2022/30 makes
  the cybersecurity requirements of RED Article 3(3)(d), (e) and (f) mandatory. The
  harmonised standards are EN 18031-1, -2 and -3:2024, with restrictions. For example, there
  is no presumption of conformity for a product that allows "not setting or using a password"
  ([UK factsheet](https://www.gov.uk/government/publications/radio-equipment-regulations-2017/regulation-eu-202230-factsheet),
  [VDE](https://www.vde.com/tic-en/news/2025/01-cyber-security-red)). EN 18031-1 applies to
  every internet-connected radio product. EN 18031-2 probably applies too, because a gadget's
  timestamped events are personal data.
- **European Union, Cyber Resilience Act.** In force since 10 December 2024. Reporting of
  actively exploited vulnerabilities starts on 11 September 2026. The main obligations,
  security updates among them, apply from 11 December 2027
  ([Commission](https://digital-strategy.ec.europa.eu/en/policies/cyber-resilience-act)).
- **United Kingdom, PSTI.** Since 29 April 2024 a product needs four things. No universal
  default passwords. A published way to report vulnerabilities. A published minimum
  security-update period. A Statement of Compliance with the product. Anyone who markets a product under their own name or
  trademark counts as a manufacturer
  ([gov.uk](https://www.gov.uk/guidance/regulations-consumer-connectable-product-security)).

What Grok Gadgets already gives you towards these rules:

| Rule | What exists | What stays yours |
| --- | --- | --- |
| No universal default password | `factory-provision` makes a different hotspot passphrase and setup code for each gadget ([ADR 010](../decisions/010-phone-setup.md)) | Keep each label with its own gadget |
| Security updates | Signed updates over the relay, with automatic revert ([ADR 012](../decisions/012-signed-updates.md)) | Run the relay, keep the signing key, ship fixes |
| Vulnerability reports | The project's own [security policy](../../SECURITY.md) | Publish your own reporting address for your product |
| Update period | Nothing | Decide it and publish it (template below) |
| Secure boot, flash encryption, anti-rollback | Documented only; off on the kit | Turn them on for products you sell. They burn eFuses and cannot be undone |

## 3. Privacy

The relay operator decides what the relay stores and why. Under the GDPR, that makes the
operator a **controller** of personal data, and online identifiers count as personal data
([GDPR Art. 4](https://gdpr-info.eu/art-4-gdpr/)). If you run the relay for your customers,
that is you.

The relay keeps device IDs, account IDs, gadget names and rooms. Its request log holds
reported state, events, command arguments (secret fields redacted) and caller IP addresses. The
log rotates at 5 MiB and keeps 5 old files ([ADR 009 §5](../decisions/009-relay-route.md)).
The relay stores tokens and codes as hashes or not at all.

A privacy notice template to adapt:

> **Privacy notice for [product name]**
>
> [Your name or company, address, contact email] runs the server that your [product] connects
> to. It stores your gadget's ID, the name and room you give it, what it reports and the
> commands you send, with the time and your IP address. We use this only to run the gadget
> for you. We keep request logs for at most [N days / until 5 files of 5 MiB are full] and
> delete account data [N days] after you remove your gadget. We do not sell or share this
> data. Contact [email] to see or delete your data. You may complain to your data protection
> authority.

## 4. Publish an update period

A statement template:

> [Product name] receives security updates until at least [date]. Updates arrive over the
> internet through [your relay name] and install by themselves. Report a security problem to
> [address]; we reply within [N] working days.

Choose a date you can keep. Updates need your relay, your signing key and your time until
that date.

## 5. Firmware licences

A firmware binary contains code under other licences, for example the LGPL-2.1 of the
Arduino-ESP32 core. Before you ship a binary, work through the
[firmware licence checklist](firmware-licences.md).

## Checklist

- You followed the module's integration instructions (antenna clearance, enclosure).
- USA: you did the Part 15B SDoC. The label says "Contains FCC ID: …".
- Canada: the host label follows RSS-Gen 9.4.4.2.
- EU: you assessed RED Article 3(3)(d)–(f) against EN 18031-1, and -2 for personal data.
- EU: you have a plan for the CRA obligations of December 2027.
- UK: no universal default password, a vulnerability address and an update period.
- UK: a Statement of Compliance goes in the box.
- India: you checked the ETA self-declaration.
- You published your privacy notice and set the log retention.
- You published your update period. Your signing key has an offline backup.
- You did the [firmware licence checklist](firmware-licences.md) for every binary.
- You decided on secure boot, flash encryption and anti-rollback for the product.
