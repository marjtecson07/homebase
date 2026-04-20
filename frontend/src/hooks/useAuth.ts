import { useState, useEffect } from 'react'
import type { User } from '../types'
import { authApi } from '../api/auth'

export const useAuth = () => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      authApi.getMe()
        .then(setUser)
        .catch(() => {
          localStorage.removeItem('access_token')
        })
        .finally(() => setLoading(false))
    } else {
      setLoading(false)
    }
  }, [])

  const login = async (email: string, password: string) => {
    const token = await authApi.login({ 
      username: email, 
      password 
    })
    localStorage.setItem('access_token', token.access_token)
    const userData = await authApi.getMe()
    setUser(userData)
    return userData
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  return { user, loading, login, logout }
}