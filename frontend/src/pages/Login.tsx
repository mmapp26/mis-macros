import { useState } from 'react'
import { useAuth } from '../store/auth'
import { Link, useNavigate } from 'react-router-dom'

export default function Login(){
  const { login } = useAuth()
  const nav = useNavigate()
  const [email,setEmail]=useState('')
  const [password,setPassword]=useState('')
  const [err,setErr]=useState<string|null>(null)
  return (
    <div className="max-w-sm mx-auto">
      <h1 className="text-xl font-semibold mb-4">Entrar</h1>
      {err && <div className="mb-2 text-red-600">{err}</div>}
      <div className="flex flex-col gap-2">
        <input className="border p-2 rounded" placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}/>
        <input className="border p-2 rounded" type="password" placeholder="Contraseña" value={password} onChange={e=>setPassword(e.target.value)}/>
        <button className="bg-blue-600 text-white p-2 rounded" onClick={async ()=>{
          try{ await login(email,password); nav('/') }catch(e:any){ setErr('Credenciales inválidas') }
        }}>Entrar</button>
      </div>
      <p className="mt-3 text-sm">¿No tienes cuenta? <Link to="/register" className="underline">Crear cuenta</Link></p>
    </div>
  )
}