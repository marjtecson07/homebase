import { Link, useLocation } from 'react-router-dom'

const navigation = [
  { name: 'Dashboard', href: '/', icon: '📊' },
  { name: 'Tasks', href: '/tasks', icon: '✅' },
  { name: 'Finances', href: '/finances', icon: '💰' },
]

export default function Sidebar() {
  const location = useLocation()

  return (
    <aside className="w-64 bg-slate-900 min-h-screen flex flex-col">
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-white text-xl font-bold">🏠 HomeBase</h1>
        <p className="text-slate-400 text-sm mt-1">Home Manager</p>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {navigation.map((item) => {
          const isActive = location.pathname === item.href
          return (
            <Link
              key={item.name}
              to={item.href}
              className={`flex items-center gap-3 px-4 py-3 rounded-lg 
                text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-primary-600 text-white'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <span>{item.icon}</span>
              {item.name}
            </Link>
          )
        })}
      </nav>
    </aside>
  )
}