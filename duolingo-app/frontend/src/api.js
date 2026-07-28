const API_BASE = import.meta.env.VITE_API_BASE || "https://duolingo-app.onrender.com";

async function request(path, options) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status}`);
  }
  return res.json();
}

export const api = {
  getGrammarQuestion: () => request('/grammar/question'),
  checkGrammarAnswer: (questionId, answer) =>
    request('/grammar/check', {
      method: 'POST',
      body: JSON.stringify({ question_id: questionId, answer }),
    }),

  getTranslationSentence: () => request('/translation/sentence'),
  checkTranslation: (sentenceId, translation) =>
    request('/translation/check', {
      method: 'POST',
      body: JSON.stringify({ sentence_id: sentenceId, translation }),
    }),

  getImagePrompt: () => request('/image/prompt'),
  checkImageDescription: (imageId, description) =>
    request('/image/check', {
      method: 'POST',
      body: JSON.stringify({ image_id: imageId, description }),
    }),
};
