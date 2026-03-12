import { useState } from 'react'
import { useAuth } from '../store/auth'
import { useNavigate } from 'react-router-dom'

export default function Register(){
  const { register } = useAuth()
  const nav = useNavigate()
  const [form, set] = useState<any>({
    email:'', password:'', nombre:'', sexo:'Mujer',
    altura_cm:165, fecha_nacimiento:'1990-01-01', peso_actual_kg:65,
    actividad:'ligera', objetivo:'mantener', agua_obj_ml: null
  })
  const handle = (k:string,v:any)=> set((s:any)=>({...s,[k]:v}))
  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-xl font-semibold mb-4">Crear cuenta</h1>
      <div className="grid grid-cols-2 gap-2">
        <input className="border p-2 rounded col-span-2" placeholder="Email" onChange={e=>handle('email',e.target.value)}/>
        <input className="border p-2 rounded col-span-2" type="password" placeholder="Contraseña" onChange={e=>handle('password',e.target.value)}/>
        <input className="border p-2 rounded" placeholder="Nombre" onChange={e=>handle('nombre',e.target.value)}/>
        <select className="border p-2 rounded" onChange={e=>handle('sexo',e.target.value)}><option>Mujer</option><option>Hombre</option></select>
        <input className="border p-2 rounded" type="number" placeholder="Altura (cm)" onChange={e=>handle('altura_cm',Number(e.target.value))}/>
        <input className="border p-2 rounded" placeholder="Nacimiento (YYYY-MM-DD)" onChange={e=>handle('fecha_nacimiento',e.target.value)}/>
        <input className="border p-2 rounded" type="number" placeholder="Peso (kg)" onChange={e=>handle('peso_actual_kg',Number(e.target.value))}/>
        <select className="border p-2 rounded" onChange={e=>handle('actividad',e.target.value)}>
          <option value="sedentaria">sedentaria</option><option value="ligera">ligera</option>
          <option value="moderada">moderada</option><option value="alta">alta</option><option value="muy_alta">muy alta</option>
        </select>
        <select className="border p-2 rounded" onChange={e=>handle('objetivo',e.target.value)}>
          <option value="perder">perder</option><option value="mantener">mantener</option>
          <option value="ganar">ganar</option><option value="recomposicion">recomposición</option>
        </select>
      </div>
      <button className="bg-blue-600 text-white p-2 rounded mt-3" onClick={async()=>{
        await register(form); nav('/')
      }}>Crear</button>
    </div>
  )
}