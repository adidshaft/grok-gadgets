const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const markup = fs.readFileSync(path.join(__dirname, 'donate.html'), 'utf8');
const source = fs.readFileSync(path.join(__dirname, 'donate.js'), 'utf8');
const destinations = [
  ['donate-eth', 'ETH', '0xD571210016e5AB4206D27f24bE128916E1C91047'],
  ['donate-sol', 'Solana', 'D2jV1NkjuHHmvkuZ48Woc29v5NDeKLmHeLkUcN4fDg68'],
  ['donate-btc', 'Bitcoin', 'bc1qal92xr892akwxgqrnkjhld7ar04hlld06uqyq5'],
  ['donate-zec', 'ZEC (Shielded)', 'u10hkzg65lgz6eq3arsylenag78jracfpguc3m4p6ptz8fkjlgxy6668yrjdgj2p704wp2f2wykrqv88tg9zu7fjuc9tk5s6vazvzmw5cvt5qkyzr32wqymesmcymja9zxpcwc6vcswa88yae023yj7jhypvn6n592t6z7nxqu4s59sdf9'],
];

// Exercise the event handlers without a browser dependency. Native focus trapping
// and Escape dismissal are checked separately in the browser preview.
function setup(clipboard) {
  const state = {active: null, selected: null, events: [], classes: new Set()};
  function element() {
    return {
      textContent: '', listeners: {},
      addEventListener(name, fn) { this.listeners[name] = fn; },
      fire(name) { return this.listeners[name]?.(); },
      focus() { state.active = this; },
    };
  }
  const trigger = Object.assign(element(), {hidden: true});
  const close = element();
  const feedback = element();
  const addresses = {};
  const buttons = destinations.map(([id, network]) => {
    const address = element();
    address.textContent = markup.match(new RegExp(`<code id="${id}"[^>]*>([^<]+)</code>`))[1];
    addresses[id] = address;
    return Object.assign(element(), {dataset: {copyAddress: id, network}});
  });
  const dialog = Object.assign(element(), {
    open: false,
    showModal() { this.open = true; close.focus(); },
    close() { this.open = false; this.fire('close'); },
    querySelectorAll() { return buttons; },
  });
  const nodes = {'#donate-dialog': dialog, '#donate-open': trigger, '#donate-close': close, '#donate-feedback': feedback};
  const document = {
    querySelector: selector => nodes[selector],
    getElementById: id => addresses[id],
    body: {classList: {add: name => state.classes.add(name), remove: name => state.classes.delete(name)}},
    dispatchEvent: event => state.events.push(event.type),
    createRange: () => ({selectNodeContents(address) { this.address = address; }}),
  };
  const selection = {removeAllRanges() { state.selected = null; }, addRange(range) { state.selected = range.address; }};
  vm.runInNewContext(source, {
    document, navigator: {clipboard}, window: {getSelection: () => selection},
    CustomEvent: class { constructor(type) { this.type = type; } },
  });
  return {state, trigger, close, feedback, dialog, addresses, buttons};
}

test('donation markup retains exactly the four supplied destinations and named controls', () => {
  assert.equal((markup.match(/<code /g) || []).length, 4);
  assert.match(markup, /<dialog[^>]+aria-labelledby="donate-title"[^>]+aria-describedby="donate-description"/);
  assert.match(markup, /id="donate-feedback" role="status"/);
  for (const [id, , expected] of destinations) {
    assert.equal(markup.match(new RegExp(`<code id="${id}"[^>]*>([^<]+)</code>`))[1], expected);
    assert.match(markup, new RegExp(`data-copy-address="${id}"[^>]+aria-label="Copy `));
  }
});

test('each copy action writes the exact full address and reports its network', async () => {
  const copied = [];
  const ui = setup({writeText: async value => copied.push(value)});
  assert.equal(ui.trigger.hidden, false);
  ui.trigger.fire('click');
  for (let i = 0; i < destinations.length; i++) {
    await ui.buttons[i].fire('click');
    assert.equal(copied[i], destinations[i][2]);
    assert.equal(ui.buttons[i].textContent, 'Copied');
    assert.equal(ui.feedback.textContent, `${destinations[i][1]} address copied.`);
  }
});

for (const [name, clipboard] of [
  ['missing clipboard API', undefined],
  ['denied clipboard permission', {writeText: async () => { throw new Error('Permission denied'); }}],
]) {
  test(`${name} selects the complete address and explains manual copying`, async () => {
    const ui = setup(clipboard);
    ui.trigger.fire('click');
    await ui.buttons[3].fire('click');
    assert.equal(ui.state.active, ui.addresses['donate-zec']);
    assert.equal(ui.state.selected.textContent, destinations[3][2]);
    assert.equal(ui.buttons[3].textContent, 'Copy');
    assert.match(ui.feedback.textContent, /Copy unavailable.*ZEC \(Shielded\)/);
  });
}

test('closing unlocks scrolling, restores the trigger and clears stale copy feedback', async () => {
  const ui = setup({writeText: async () => {}});
  ui.trigger.fire('click');
  assert.equal(ui.dialog.open, true);
  assert.equal(ui.state.classes.has('donation-is-open'), true);
  await ui.buttons[0].fire('click');
  ui.close.fire('click');
  assert.equal(ui.dialog.open, false);
  assert.equal(ui.state.classes.has('donation-is-open'), false);
  assert.equal(ui.state.active, ui.trigger);
  assert.equal(ui.feedback.textContent, '');
  assert.deepEqual(ui.state.events, ['grok:dialog-change', 'grok:dialog-change']);
  ui.trigger.fire('click');
  assert.equal(ui.buttons[0].textContent, 'Copy');
});

test('a clipboard promise settling after close and reopen cannot change the new dialog', async () => {
  let rejectCopy;
  const ui = setup({writeText: () => new Promise((resolve, reject) => { rejectCopy = reject; })});
  ui.trigger.fire('click');
  const copy = ui.buttons[0].fire('click');
  ui.close.fire('click');
  ui.trigger.fire('click');
  rejectCopy(new Error('Permission denied'));
  await copy;
  assert.equal(ui.feedback.textContent, '');
  assert.equal(ui.state.active, ui.close);
  assert.equal(ui.state.selected, null);
});
