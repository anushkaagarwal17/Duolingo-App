import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import { recordAttempt } from '../progress'

export default function ImageComprehension() {
  const [prompt, setPrompt] = useState(null)
  const [description, setDescription] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  async function loadPrompt() {
    setLoading(true)
    setResult(null)
    setDescription('')
    const p = await api.getImagePrompt()
    setPrompt(p)
    setLoading(false)
  }

  async function submit() {
    const res = await api.checkImageDescription(prompt.id, description)
    setResult(res)
    const didWell = res.word_count >= 15 && res.matched_keywords.length > res.missed_keywords.length
    recordAttempt(didWell)
  }

  if (!prompt && !loading) {
    loadPrompt()
  }

  return (
    <div>
      <Link to="/" className="back-link">&larr; Back to activities</Link>
      <h2 style={{ fontSize: '1.5rem', marginBottom: '0.4rem' }}>Image comprehension</h2>
      <p style={{ color: 'var(--slate)', marginBottom: '1.25rem' }}>
        Describe what you see in as much detail as you can.
      </p>

      {prompt && (
        <div className="card">
          <img src={prompt.image_url} alt="Describe this scene" className="page-image" />

          <textarea
            rows={4}
            placeholder="Describe the image in a few sentences"
            value={description}
            disabled={!!result}
            onChange={(e) => setDescription(e.target.value)}
          />

          {!result && (
            <button
              className="btn btn-primary"
              style={{ marginTop: '0.9rem' }}
              disabled={!description.trim()}
              onClick={submit}
            >
              Get feedback
            </button>
          )}

          {result && (
            <div className="feedback neutral">
              <strong>Feedback</strong>
              <ul style={{ margin: '0.6rem 0 0', paddingLeft: '1.2rem' }}>
                {result.feedback.map((line, i) => (
                  <li key={i} style={{ marginBottom: '0.3rem' }}>{line}</li>
                ))}
              </ul>

              <p style={{ margin: '0.7rem 0 0.2rem', fontSize: '0.9rem', color: 'var(--slate)' }}>
                One way to describe this image:
              </p>
              <p style={{ margin: 0 }}>{result.reference_description}</p>
            </div>
          )}

          {result && (
            <button className="btn btn-primary" style={{ marginTop: '1.25rem' }} onClick={loadPrompt}>
              Try another image
            </button>
          )}
        </div>
      )}
    </div>
  )
}
