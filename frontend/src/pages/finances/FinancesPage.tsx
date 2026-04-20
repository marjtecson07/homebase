import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { transactionsApi } from '../../api/transactions'
import type { Transaction, TransactionCreate } from '../../types'

export default function FinancesPage() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [newTransaction, setNewTransaction] = useState<TransactionCreate>({
    description: '',
    amount: 0,
    type: 'expense',
    date: new Date().toISOString().split('T')[0],
  })

  const { data: transactions = [], isLoading } = useQuery<Transaction[]>({
    queryKey: ['transactions'],
    queryFn: transactionsApi.getAll
  })

  const createMutation = useMutation({
    mutationFn: transactionsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
      setShowForm(false)
      setNewTransaction({
        description: '',
        amount: 0,
        type: 'expense',
        date: new Date().toISOString().split('T')[0],
      })
    }
  })

  const deleteMutation = useMutation({
    mutationFn: transactionsApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] })
    }
  })

  const totalIncome = transactions
    .filter(t => t.type === 'income')
    .reduce((sum, t) => sum + t.amount, 0)
  const totalExpenses = transactions
    .filter(t => t.type === 'expense')
    .reduce((sum, t) => sum + t.amount, 0)

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(newTransaction)
  }

  if (isLoading) return (
    <div className="flex items-center justify-center h-64">
      <div className="text-gray-400">Loading finances...</div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Finances</h2>
          <p className="text-gray-500 mt-1">
            Track your income and expenses
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-primary-600 hover:bg-primary-700 text-white 
            px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          + Add Transaction
        </button>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl p-5 shadow-sm border 
          border-gray-100">
          <p className="text-sm text-gray-500">Total Income</p>
          <p className="text-2xl font-bold text-green-600 mt-1">
            ₱{totalIncome.toLocaleString()}
          </p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-sm border 
          border-gray-100">
          <p className="text-sm text-gray-500">Total Expenses</p>
          <p className="text-2xl font-bold text-red-600 mt-1">
            ₱{totalExpenses.toLocaleString()}
          </p>
        </div>
        <div className="bg-white rounded-xl p-5 shadow-sm border 
          border-gray-100">
          <p className="text-sm text-gray-500">Net Balance</p>
          <p className={`text-2xl font-bold mt-1 ${
            totalIncome - totalExpenses >= 0 
              ? 'text-green-600' 
              : 'text-red-600'
          }`}>
            ₱{(totalIncome - totalExpenses).toLocaleString()}
          </p>
        </div>
      </div>

      {/* New Transaction Form */}
      {showForm && (
        <div className="bg-white rounded-xl shadow-sm border 
          border-gray-100 p-5">
          <h3 className="font-semibold text-gray-900 mb-4">
            Add Transaction
          </h3>
          <form onSubmit={handleCreate} className="space-y-4">
            <input
              type="text"
              placeholder="Description"
              value={newTransaction.description}
              onChange={(e) => setNewTransaction({
                ...newTransaction, description: e.target.value
              })}
              className="w-full px-4 py-2.5 border border-gray-300 
                rounded-lg focus:ring-2 focus:ring-primary-500 
                focus:border-transparent outline-none"
              required
            />
            <div className="grid grid-cols-3 gap-4">
              <input
                type="number"
                placeholder="Amount"
                value={newTransaction.amount || ''}
                onChange={(e) => setNewTransaction({
                  ...newTransaction, amount: parseFloat(e.target.value)
                })}
                className="px-4 py-2.5 border border-gray-300 rounded-lg
                  focus:ring-2 focus:ring-primary-500 outline-none"
                required
                min="0"
                step="0.01"
              />
              <select
                value={newTransaction.type}
                onChange={(e) => setNewTransaction({
                  ...newTransaction,
                  type: e.target.value as 'income' | 'expense'
                })}
                className="px-4 py-2.5 border border-gray-300 rounded-lg
                  focus:ring-2 focus:ring-primary-500 outline-none"
              >
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
              <input
                type="date"
                value={newTransaction.date}
                onChange={(e) => setNewTransaction({
                  ...newTransaction, date: e.target.value
                })}
                className="px-4 py-2.5 border border-gray-300 rounded-lg
                  focus:ring-2 focus:ring-primary-500 outline-none"
                required
              />
            </div>
            <div className="flex gap-3">
              <button type="submit"
                disabled={createMutation.isPending}
                className="bg-primary-600 hover:bg-primary-700 text-white
                  px-4 py-2 rounded-lg text-sm font-medium 
                  transition-colors disabled:opacity-50"
              >
                {createMutation.isPending ? 'Adding...' : 'Add Transaction'}
              </button>
              <button type="button" onClick={() => setShowForm(false)}
                className="px-4 py-2 rounded-lg text-sm font-medium 
                  text-gray-600 hover:bg-gray-100 transition-colors"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Transactions List */}
      <div className="bg-white rounded-xl shadow-sm border 
        border-gray-100 divide-y divide-gray-50">
        {transactions.length === 0 ? (
          <div className="p-8 text-center text-gray-400">
            No transactions yet — add your first one!
          </div>
        ) : (
          transactions.map((transaction) => (
            <div key={transaction.id}
              className="flex items-center gap-4 p-4 hover:bg-gray-50 
                transition-colors">
              <div className={`w-10 h-10 rounded-full flex items-center 
                justify-center flex-shrink-0 ${
                transaction.type === 'income'
                  ? 'bg-green-100 text-green-600'
                  : 'bg-red-100 text-red-600'
              }`}>
                {transaction.type === 'income' ? '↑' : '↓'}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">
                  {transaction.description}
                </p>
                <p className="text-xs text-gray-400 mt-0.5">
                  {transaction.date}
                  {transaction.is_shared && ' · Shared'}
                </p>
              </div>
              <span className={`font-semibold flex-shrink-0 ${
                transaction.type === 'income'
                  ? 'text-green-600'
                  : 'text-red-600'
              }`}>
                {transaction.type === 'income' ? '+' : '-'}
                ₱{transaction.amount.toLocaleString()}
              </span>
              <button
                onClick={() => deleteMutation.mutate(transaction.id)}
                className="text-gray-300 hover:text-red-500 
                  transition-colors flex-shrink-0"
              >
                ✕
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  )
}