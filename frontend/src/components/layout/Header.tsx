interface HeaderProps {
  user: { full_name: string } | null
  onLogout: () => void
}

export default function Header({ user, onLogout }: HeaderProps) {
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-4 
      flex items-center justify-between">
      <div />
      <div className="flex items-center gap-4">
        <span className="text-sm text-gray-600">
          👋 Hi, {user?.full_name}
        </span>
        <button
          onClick={onLogout}
          className="text-sm text-gray-500 hover:text-gray-700 
            px-3 py-1 rounded border border-gray-300 
            hover:border-gray-400 transition-colors"
        >
          Logout
        </button>
      </div>
    </header>
  )
}