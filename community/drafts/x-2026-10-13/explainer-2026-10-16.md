# Explainer thread, Fri 16 Oct 2026, 7:00 PM IST (9:30 am ET). Draft only.

## 1/5 · attach media/card-howitworks.png

how Grok Gadgets works, for builders, users and anyone curious. what's tested today and what's still planned 👇

## 2/5

today, tested on my kit: @grok @bot on my iphone and mac calls the gadget tools natively, through a gateway i run

in progress: that gateway now runs on a small always-on linux server instead of my mac. the esp32 oled connects out to it over tls and shows Online. the "phone on cellular, mac asleep" check isn't done yet

## 3/5

who sees what: the relay is the builder's server. it never gets into your Grok Bot account, Grok Bot signs in to the relay, not the other way round

it only gets the gadget calls your own Grok Bot chooses to send: device ids, commands, reported state. no chats, no wifi passwords. every sign in can be revoked

don't want a builder's relay? it's open source, run your own

## 4/5

the design: each builder runs their own relay at their own address. you add each one to your @grok @bot once, one sign in each

then one chat can drive all of them, like "dim the lamp and show the weather on the desk display". only one gadget server is tested so far

## 5/5

planned, not built yet:

users: unbox, plug in, pick your home wifi from the gadget's setup hotspot, it shows Online and a short code. tell Grok Bot "add my gadgets at <builder address>", type the code, done

builders: build with the sdk, test on the simulator, run one relay, give each gadget its identity at the factory, ship
