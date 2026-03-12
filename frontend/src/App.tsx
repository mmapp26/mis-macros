import { useEffect, useState } from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import { useAuth } from './store/auth'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import DayView from './pages/DayView'
import Settings from './pages/Settings'
import Stats from './pages/Stats'

export default function App(){
  const { token, logout } = useAuth()
  const [dark, setDark] = useState<boolean>(() => localStorage.getItem('theme')==='dark')
  useEffect(()=>{ 
    document.documentElement.classList.toggle('dark', dark)
    localStorage.setItem('theme', dark?'dark':'light')
  }, [dark])

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 dark:text-gray-50">
      <header className="p-3 flex justify-between items-center border-b border-gray-200 dark:border-gray-700">
        <Link to="/" className="font-bold">Mis Macros</Link>
        <div className="flex gap-3 items-center">
          <button onClick={()=>setDark(v=>!v)} className="px-2 py-1 text-sm border rounded">
            {dark?'Tema claro':'Tema oscuro'}
          </button>
          {token ? <button onClick={logout} className="px-2 py-1 text-sm border rounded">Salir</button> : null}
        </div>
      </header>
      <main className="p-4 max-w-5xl mx-auto">
        <Routes>
          <Route path="/" element={token? <Dashboard/> : <Login/>} />
          <Route path="/register" element={<Register/>}/>
          <Route path="/day/:fecha" element={<DayView/>}/>
          <Route path="/settings" element={<Settings/>}/>
          <Route path="/stats" element={<Stats/>}/>
        </Routes>
      </main>
    </div>
  )
}