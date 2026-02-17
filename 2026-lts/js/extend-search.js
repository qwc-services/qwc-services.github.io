const params = new URLSearchParams(window.location.search);
const q = params.get('q');

// Ensure single word query is pre- and postfixed with '*' (wildcard char)
if (q) {
  const words = q.split(/\s+/);
  if (words.length === 1) {
    const word = words[0];
    if (!word.startsWith('*') || !word.endsWith('*')) {
      words[0] = `*${word.replace(/^\*/, "").replace(/\*$/, "")}*`;
      params.set('q', words.join(' '));
      window.location.href = `${window.location.pathname}?${params.toString()}`;
    }
  }
}
