(() => {
  const page = document.querySelector('#donate-page');
  if (!page) return;
  const feedback = document.querySelector('#donate-feedback');
  const buttons = page.querySelectorAll('[data-copy-address]');
  let copyRequest = 0;

  buttons.forEach(button => button.addEventListener('click', async () => {
    const address = document.getElementById(button.dataset.copyAddress);
    const request = ++copyRequest;
    buttons.forEach(item => { item.textContent = 'Copy'; });
    feedback.textContent = '';
    try {
      await navigator.clipboard.writeText(address.textContent);
      if (request !== copyRequest) return;
      button.textContent = 'Copied';
      feedback.textContent = `${button.dataset.network} address copied.`;
    } catch {
      if (request !== copyRequest) return;
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
