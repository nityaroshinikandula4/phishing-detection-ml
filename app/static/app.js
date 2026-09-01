const form = document.querySelector('[data-form]');
const result = document.querySelector('[data-result]');
const errorBox = document.querySelector('[data-error]');
const exampleButton = document.querySelector('[data-example]');

const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));

exampleButton?.addEventListener('click', () => {
  document.querySelector('#url').value = 'http://secure-account-verify.example.test/login?continue=update';
  document.querySelector('#emailText').value = 'URGENT: Your account is suspended. Verify your password immediately within 24 hours to avoid permanent closure!';
  document.querySelector('#analyzer').scrollIntoView({ behavior: 'smooth' });
});

form?.addEventListener('reset', () => {
  errorBox.textContent = '';
  result.innerHTML = '<div class="empty"><span>↗</span><h3>Evidence appears here.</h3><p>Sentinel does not visit the URL. It reviews lexical structure and message language only.</p></div>';
});

form?.addEventListener('submit', async (event) => {
  event.preventDefault();
  errorBox.textContent = '';
  const payload = Object.fromEntries(new FormData(form).entries());
  if (!String(payload.url).trim() && !String(payload.email_text).trim()) {
    errorBox.textContent = 'Provide a URL, a message, or both.';
    return;
  }
  result.innerHTML = '<div class="empty"><span>…</span><h3>Reviewing signals</h3><p>The service analyzes text only and does not contact the destination.</p></div>';
  try {
    const response = await fetch('/api/analyze', { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Analysis failed.');
    const signalItems = data.signals.length
      ? data.signals.map((signal) => `<li><strong>${escapeHtml(signal.label)}</strong><p>${escapeHtml(signal.detail)}</p></li>`).join('')
      : '<li><strong>No configured warning signal matched.</strong><p>This is not a guarantee of safety. Verify the sender and domain independently.</p></li>';
    result.innerHTML = `
      <div class="score-head"><div class="score ${escapeHtml(data.label)}">${data.score}</div><div class="score-copy"><h3>${escapeHtml(data.label)} risk</h3><p>${data.signals.length} explainable signal${data.signals.length === 1 ? '' : 's'}</p></div></div>
      <ul class="signals">${signalItems}</ul>
      <h4>Recommended next steps</h4><ol class="actions-list">${data.actions.map((action) => `<li>${escapeHtml(action)}</li>`).join('')}</ol>
      <p class="disclaimer">${escapeHtml(data.disclaimer)}</p>`;
  } catch (error) {
    errorBox.textContent = error instanceof Error ? error.message : 'Analysis failed.';
    result.innerHTML = '<div class="empty"><span>!</span><h3>Analysis unavailable</h3><p>Confirm the local API is running and try again.</p></div>';
  }
});
