import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { recordAttempt } from '../progress'

export default function Grammar() {
  const [question, setQuestion] = useState(null)
  const [selected, setSelected] = useState(null)
  const [textAnswer, setTextAnswer] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function loadQuestion() {
    setLoading(true)
    setResult(null)
    setSelected(null)
    setTextAnswer('')
    const q = await api.getGrammarQuestion()
    setQuestion(q)
    setLoading(false)
  }

  async function submit(answer) {
    const res = await api.checkGrammarAnswer(question.id, answer)
    setResult(res)
    recordAttempt(res.correct)
  }

  if (!question && !loading) {
    loadQuestion()
  }

  return (
    <div>
      <Link to="/" className="back-link">&larr; Back to activities</Link>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '0.4rem' }}>Grammar and fun</h2>
      <p style={{ color: 'var(--slate)', marginBottom: '1.25rem' }}>
        Sharpen your grammar with a quick question.
      </p>

      {question && (
        <div className="card">
          <p style={{ fontSize: '1.1rem', fontWeight: 500, marginBottom: '1.1rem' }}>
            {question.prompt}
          </p>

          {question.type === 'mcq' && (
            <div>
              {question.options.map((opt, idx) => {
                let cls = 'option-btn'
                if (result) {
                  if (idx === result.correct_answer_index) cls += ' correct'
                  else if (idx === selected && !result.correct) cls += ' incorrect'
                } else if (idx === selected) {
                  cls += ' selected'
                }
                return (
                  <button
                    key={idx}
                    className={cls}
                    disabled={!!result}
                    onClick={() => {
                      setSelected(idx)
                      submit(idx)
                    }}
                  >
                    {opt}
                  </button>
                )
              })}
            </div>
          )}

          {question.type === 'fill_blank' && (
            <div>
              <input
                type="text"
                placeholder="Type your answer"
                value={textAnswer}
                disabled={!!result}
                onChange={(e) => setTextAnswer(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && textAnswer && !result && submit(textAnswer)}
              />
              {!result && (
                <button
                  className="btn btn-primary"
                  style={{ marginTop: '0.9rem' }}
                  disabled={!textAnswer}
                  onClick={() => submit(textAnswer)}
                >
                  Check answer
                </button>
              )}
            </div>
          )}

          {result && (
            <div className={`feedback ${result.correct ? 'good' : 'bad'}`}>
              <strong>{result.correct ? 'Correct! +10 XP' : 'Not quite.'}</strong>
              <p style={{ margin: '0.5rem 0 0' }}>{result.explanation}</p>
              {!result.correct && (
                <p style={{ margin: '0.4rem 0 0', color: 'var(--slate)' }}>
                  Correct answer: <strong>{result.correct_answer}</strong>
                </p>
              )}
            </div>
          )}

          {result && (
            <button className="btn btn-primary" style={{ marginTop: '1.25rem' }} onClick={loadQuestion}>
              Next question
            </button>
          )}
        </div>
      )}
    </div>
  )
}
