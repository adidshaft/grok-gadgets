(() => {
  const dialog = document.querySelector('#donate-dialog');
  const trigger = document.querySelector('#donate-open');
  if (!dialog || !trigger || typeof dialog.showModal !== 'function') return;
  const close = document.querySelector('#donate-close');
  const feedback = document.querySelector('#donate-feedback');
  const buttons = dialog.querySelectorAll('[data-copy-address]');
  let copyRequest = 0;
  const notifyMotion = () => document.dispatchEvent(new CustomEvent('grok:dialog-change'));
  const resetCopy = () => {
    copyRequest += 1;
    feedback.textContent = '';
    buttons.forEach(button => { button.textContent = 'Copy'; });
  };

  trigger.hidden = false;
  trigger.addEventListener('click', () => {
    if (dialog.open) return;
    resetCopy();
    dialog.showModal();
    document.body.classList.add('donation-is-open');
    notifyMotion();
  });
  close.addEventListener('click', () => dialog.close());
  // Native dialog supplies Escape dismissal and keeps keyboard focus inside it.
  dialog.addEventListener('close', () => {
    resetCopy();
    document.body.classList.remove('donation-is-open');
    notifyMotion();
    trigger.focus();
  });

  buttons.forEach(button => button.addEventListener('click', async () => {
    const address = document.getElementById(button.dataset.copyAddress);
    const request = ++copyRequest;
    buttons.forEach(item => { item.textContent = 'Copy'; });
    feedback.textContent = '';
    try {
      await navigator.clipboard.writeText(address.textContent);
      if (!dialog.open || request !== copyRequest) return;
      button.textContent = 'Copied';
      feedback.textContent = `${button.dataset.network} address copied.`;
    } catch {
      if (!dialog.open || request !== copyRequest) return;
      address.focus();
      const range = document.createRange();
      range.selectNodeContents(address);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      feedback.textContent = `Copy unavailable. Select and copy the ${button.dataset.network} address shown above.`;
    }
  }));
})();
