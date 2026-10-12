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

function setup(clipboard) {
  const state = {active: null, selected: null};
  function element() {
    return {
      textContent: '', listeners: {},
      addEventListener(name, fn) { this.listeners[name] = fn; },
      fire(name) { return this.listeners[name]?.(); },
      focus() { state.active = this; },
    };
  }
  const feedback = element();
  const addresses = {};
  const buttons = destinations.map(([id, network]) => {
    const address = element();
    address.textContent = markup.match(new RegExp(`<code id="${id}"[^>]*>([^<]+)</code>`))[1];
    addresses[id] = address;
    return Object.assign(element(), {dataset: {copyAddress: id, network}});
  });
  const page = {querySelectorAll() { return buttons; }};
  const document = {
    querySelector(selector) { return {'#donate-page': page, '#donate-feedback': feedback}[selector]; },
    getElementById(id) { return addresses[id]; },
    createRange: () => ({selectNodeContents(address) { this.address = address; }}),
  };
  const selection = {removeAllRanges() { state.selected = null; }, addRange(range) { state.selected = range.address; }};
  vm.runInNewContext(source, {
    document, navigator: {clipboard}, window: {getSelection: () => selection},
  });
  return {state, feedback, addresses, buttons};
}

test('standalone donation page retains exactly the four supplied destinations', () => {
  assert.equal((markup.match(/<code /g) || []).length, 4);
  assert.match(markup, /<section id="donate-page"[^>]+aria-labelledby="donate-title"/);
  assert.match(markup, /<h1 id="donate-title">Support Grok Gadgets\.<\/h1>/);
  assert.match(markup, /id="donate-feedback" role="status"/);
  for (const [id, , expected] of destinations) {
    assert.equal(markup.match(new RegExp(`<code id="${id}"[^>]*>([^<]+)</code>`))[1], expected);
    assert.match(markup, new RegExp(`data-copy-address="${id}"[^>]+aria-label="Copy `));
  }
});

test('each copy action writes the exact full address and reports its network', async () => {
  const copied = [];
  const ui = setup({writeText: async value => copied.push(value)});
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
    await ui.buttons[3].fire('click');
    assert.equal(ui.state.active, ui.addresses['donate-zec']);
    assert.equal(ui.state.selected.textContent, destinations[3][2]);
    assert.equal(ui.buttons[3].textContent, 'Copy');
    assert.match(ui.feedback.textContent, /Copy unavailable.*ZEC \(Shielded\)/);
  });
}

test('a stale clipboard request cannot change the latest copy feedback', async () => {
  let rejectCopy;
  const ui = setup({writeText: value => value === destinations[0][2]
    ? new Promise((resolve, reject) => { rejectCopy = reject; })
    : Promise.resolve()});
  const first = ui.buttons[0].fire('click');
  await ui.buttons[1].fire('click');
  rejectCopy(new Error('Permission denied'));
  await first;
  assert.equal(ui.feedback.textContent, 'Solana address copied.');
  assert.equal(ui.state.selected, null);
});
