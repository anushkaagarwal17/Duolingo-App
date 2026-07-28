import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { getProgress } from '../progress'

export default function Topbar() {
  const [xp, setXp] = useState(0)

  useEffect(() => {
    setXp(getProgress().xp)
    const onFocus = () => setXp(getProgress().xp)
    window.addEventListener('focus', onFocus)
    return () => window.removeEventListener('focus', onFocus)
  }, [])

  return (
    <header className="topbar">
      <div className="topbar-inner">
        <Link to="/" className="brand">
          <span className="brand-mark">D</span>
          <span className="brand-name">Duolingo English App</span>
        </Link>
        <span className="streak-badge">⚡ {xp} XP</span>
      </div>
    </header>
  )
}
