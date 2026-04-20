import { useQuery } from '@tanstack/react-query'
import { tasksApi } from '../../api/tasks'
import { transactionsApi } from '../../api/transactions'
import type { Task, Transaction } from '../../types'

export default function DashboardPage() {
  const { data: tasks = [] } = useQuery<Task[]>({
    queryKey: ['tasks'],
    queryFn: tasksApi.getAll
  })

  const { data: transactions = [] } = useQuery<Transaction[]>({
    queryKey: ['transactions'],
    queryFn: transactionsApi.getAll
  })

  const pendingTasks = tasks.filter(t => t.status !== 'done')
  const totalExpenses = transactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0)
  const totalIncome = transactions
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0)

  const stats = [
    { label: 'Pending Tasks', value: pendingTasks.length, 
      icon: '✅', color: 'bg-blue-50 text-blue-700' },
    { label: 'Total Income', 
      value: `₱${totalIncome.toLocaleString()}`,
      icon: '📈', color: 'bg-green-50 text-green-700' },
    { label: 'Total Expenses', 
      value: `₱${totalExpenses.toLocaleString()}`,
      icon: '📉', color: 'bg-red-50 text-red-700' },
    { label: 'Net Balance', 
      value: `₱${(totalIncome - totalExpenses).toLocaleString()}`,
      icon: '💰', color: 'bg-purple-50 text-purple-700' },
  ]

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">Dashboard</h2>
        <p className="text-gray-500 mt-1">
          Welcome back! Here's what's going on.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} 
            className="bg-white rounded-xl p-5 shadow-sm border 
              border-gray-100">
            <div className={`inline-flex p-2 rounded-lg ${stat.color}`}>
              <span className="text-xl">{stat.icon}</span>
            </div>
            <p className="text-2xl font-bold text-gray-900 mt-3">
              {stat.value}
            </p>
            <p className="text-sm text-gray-500 mt-1">{stat.label}</p>
          </div>
        ))}
      </div>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Tasks */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
          <h3 className="font-semibold text-gray-900 mb-4">Recent Tasks</h3>
          {pendingTasks.length === 0 ? (
            <p className="text-gray-400 text-sm">No pending tasks 🎉</p>
          ) : (
            <div className="space-y-3">
              {pendingTasks.slice(0, 5).map((task) => (
                <div key={task.id} 
                  className="flex items-center gap-3 text-sm">
                  <span className={`w-2 h-2 rounded-full flex-shrink-0 ${
                    task.priority === 'high' ? 'bg-red-500' :
                    task.priority === 'medium' ? 'bg-yellow-500' : 
                    'bg-green-500'
                  }`} />
                  <span className="text-gray-700 truncate">{task.title}</span>
                  <span className={`ml-auto text-xs px-2 py-0.5 rounded-full
                    flex-shrink-0 ${
                    task.status === 'in_progress' 
                      ? 'bg-blue-100 text-blue-700' 
                      : 'bg-gray-100 text-gray-600'
                  }`}>
                    {task.status.replace('_', ' ')}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Transactions */}
        <div className="bg-white rounded-xl shadow-sm border 
          border-gray-100 p-5">
          <h3 className="font-semibold text-gray-900 mb-4">
            Recent Transactions
          </h3>
          {transactions.length === 0 ? (
            <p className="text-gray-400 text-sm">No transactions yet</p>
          ) : (
            <div className="space-y-3">
              {transactions.slice(0, 5).map((transaction) => (
                <div key={transaction.id} 
                  className="flex items-center justify-between text-sm">
                  <span className="text-gray-700 truncate">
                    {transaction.description}
                  </span>
                  <span className={`ml-4 font-medium flex-shrink-0 ${
                    transaction.type === 'income' 
                      ? 'text-green-600' 
                      : 'text-red-600'
                  }`}>
                    {transaction.type === 'income' ? '+' : '-'}
                    ₱{transaction.amount.toLocaleString()}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}