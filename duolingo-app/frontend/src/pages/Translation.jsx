import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { recordAttempt } from '../progress'

export default function Translation() {
  const [sentence, setSentence] = useState(null)
  const [translation, setTranslation] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function loadSentence() {
    setLoading(true)
    setResult(null)
    setTranslation('')
    const s = await api.getTranslationSentence()
    setSentence(s)
    setLoading(false)
  }

  async function submit() {
    const res = await api.checkTranslation(sentence.id, translation)
    setResult(res)
    recordAttempt(res.coverage_percent >= 80)
  }

  if (!sentence && !loading) {
    loadSentence()
  }

  return (
    <div>
      <Link to="/" className="back-link">&larr; Back to activities</Link>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '0.4rem' }}>Reading and translation</h2>
      <p style={{ color: 'var(--slate)', marginBottom: '1.25rem' }}>
        Translate the Hindi sentence into English.
      </p>

      {sentence && (
        <div className="card">
          <p style={{ fontSize: '1.2rem', fontWeight: 500, marginBottom: '1.1rem', lineHeight: 1.8 }}>
            {sentence.hindi}
          </p>

          <textarea
            rows={3}
            placeholder="Write your English translation here"
            value={translation}
            disabled={!!result}
            onChange={(e) => setTranslation(e.target.value)}
          />

          {!result && (
            <button
              className="btn btn-primary"
              style={{ marginTop: '0.9rem' }}
              disabled={!translation.trim()}
              onClick={submit}
            >
              Check translation
            </button>
          )}

          {result && (
            <div className={`feedback ${result.coverage_percent >= 80 ? 'good' : result.coverage_percent >= 50 ? 'neutral' : 'bad'}`}>
              <strong>{result.verdict}</strong>
              <div className="progress-track">
                <div className="progress-fill" style={{ width: `${result.coverage_percent}%` }} />
              </div>
              <p style={{ margin: '0.6rem 0 0.3rem', fontSize: '0.9rem', color: 'var(--slate)' }}>
                Reference translation:
              </p>
              <p style={{ margin: 0 }}>{result.reference}</p>

              {result.missed_keywords.length > 0 && (
                <>
                  <p style={{ margin: '0.7rem 0 0.2rem', fontSize: '0.9rem', color: 'var(--slate)' }}>
                    Ideas you could add:
                  </p>
                  <div className="pill-row">
                    {result.missed_keywords.map((kw) => (
                      <span className="pill miss" key={kw}>{kw}</span>
                    ))}
                  </div>
                </>
              )}
            </div>
          )}

          {result && (
            <button className="btn btn-primary" style={{ marginTop: '1.25rem' }} onClick={loadSentence}>
              Next sentence
            </button>
          )}
        </div>
      )}
    </div>
  )
}
