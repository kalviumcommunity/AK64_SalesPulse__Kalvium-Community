import { createContext, useContext, useState } from 'react'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem('salespulse_auth') === 'true'
  })
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('salespulse_user')
    return savedUser ? JSON.parse(savedUser) : null
  })

  const login = (email, role, name = '') => {
    setIsAuthenticated(true)
    const newUser = { email, role, name }
    setUser(newUser)
    localStorage.setItem('salespulse_auth', 'true')
    localStorage.setItem('salespulse_user', JSON.stringify(newUser))
  }

  const logout = () => {
    setIsAuthenticated(false)
    setUser(null)
    localStorage.removeItem('salespulse_auth')
    localStorage.removeItem('salespulse_user')
  }

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
