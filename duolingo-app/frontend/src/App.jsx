import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Topbar from './components/Topbar.jsx'
import Home from './pages/Home.jsx'
import Grammar from './pages/Grammar.jsx'
import Translation from './pages/Translation.jsx'
import ImageComprehension from './pages/ImageComprehension.jsx'

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Topbar />
        <main className="app-main">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/grammar" element={<Grammar />} />
            <Route path="/translation" element={<Translation />} />
            <Route path="/image" element={<ImageComprehension />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}
