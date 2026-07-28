const KEY = 'duolingo-english-app-progress';

function read() {
  try {
    const raw = localStorage.getItem(KEY);
    return raw ? JSON.parse(raw) : { xp: 0, correct: 0, attempted: 0 };
  } catch {
    return { xp: 0, correct: 0, attempted: 0 };
  }
}

function write(state) {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch {
    // ignore storage errors (e.g. private browsing)
  }
}

export function getProgress() {
  return read();
}

export function recordAttempt(wasCorrect) {
  const state = read();
  state.attempted += 1;
  if (wasCorrect) {
    state.correct += 1;
    state.xp += 10;
  }
  write(state);
  return state;
}
