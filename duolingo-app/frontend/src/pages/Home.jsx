import { Link } from 'react-router-dom'

const ACTIVITIES = [
  {
    to: '/grammar',
    icon: '✍️',
    color: '#fff4e2',
    title: 'Grammar and fun',
    description: 'Quick fill-in-the-blank and multiple-choice grammar challenges.',
  },
  {
    to: '/translation',
    icon: '🌏',
    color: '#e3f7f1',
    title: 'Reading and translation',
    description: 'Translate Hindi sentences into English and check your coverage.',
  },
  {
    to: '/image',
    icon: '🖼️',
    color: '#fdeceb',
    title: 'Image comprehension',
    description: 'Describe a picture and get feedback on vocabulary and detail.',
  },
]

export default function Home() {
  return (
    <div>
      <h1 className="display" style={{ fontSize: '2rem' }}>Practice a little English every day</h1>
      <p style={{ color: 'var(--slate)', marginTop: '0.6rem', fontSize: '1.02rem' }}>
        Three short activities, no sign-up, no waiting on an AI response — pick one and start.
      </p>

      <div className="activity-grid">
        {ACTIVITIES.map((a) => (
          <Link to={a.to} className="activity-card" key={a.to}>
            <div className="activity-icon" style={{ background: a.color }}>{a.icon}</div>
            <h3>{a.title}</h3>
            <p>{a.description}</p>
          </Link>
        ))}
      </div>
    </div>
  )
}
