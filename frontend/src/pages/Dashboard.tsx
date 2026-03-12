import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { API } from '../api/client'

export default function Dashboard(){
  const [profile,setProfile]=useState<any>(null)
  const hoy = new Date().toISOString().slice(0,10)
  useEffect(()=>{ (async()=>{
    const {data} = await API.get('/users/me'); setProfile(data)
  })() },[])
  return (
    <div>
      <h1 className="text-xl font-semibold mb-2">¡Hola {profile?.nombre || ''}!</h1>
      <div className="flex gap-3 my-4">
        <Link to={`/day/${hoy}`} className="px-3 py-2 bg-emerald-600 text-white rounded">Registrar hoy</Link>
        <Link to="/settings" className="px-3 py-2 border rounded">Configuración</Link>
        <Link to="/stats" className="px-3 py-2 border rounded">Estadísticas</Link>
      </div>
      <p className="text-sm text-gray-500">Días low‑carb predeterminados: Lunes y Martes (configurable)</p>
    </div>
  )
}