const urlElement = document.querySelector('#url');
const button = document.querySelector('#analyze');
const result = document.querySelector('#result');
let activeUrl = '';

chrome.tabs.query({ active: true, currentWindow: true }, ([tab]) => {
  activeUrl = tab?.url || '';
  urlElement.textContent = activeUrl || 'No active URL is available.';
  button.disabled = !activeUrl;
});

button.addEventListener('click', async () => {
  result.textContent = 'Analyzing…';
  try {
    const response = await fetch('http://127.0.0.1:8000/api/analyze', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url:activeUrl,email_text:''})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Request failed');
    result.innerHTML = `<div class="score ${data.label}">${data.score}/100 · ${data.label} risk</div><ul>${data.signals.slice(0,4).map(s => `<li>${s.label}</li>`).join('')}</ul>`;
  } catch (error) {
    result.textContent = 'Start Sentinel locally on port 8000 and try again.';
  }
});
