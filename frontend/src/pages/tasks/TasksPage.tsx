import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { tasksApi } from '../../api/tasks'
import type { Task, TaskCreate } from '../../types'

const priorityColors = {
  low: 'bg-green-100 text-green-700',
  medium: 'bg-yellow-100 text-yellow-700',
  high: 'bg-red-100 text-red-700',
}

const statusColors = {
  todo: 'bg-gray-100 text-gray-600',
  in_progress: 'bg-blue-100 text-blue-700',
  done: 'bg-green-100 text-green-700',
}

export default function TasksPage() {
  const queryClient = useQueryClient()
  const [showForm, setShowForm] = useState(false)
  const [newTask, setNewTask] = useState<TaskCreate>({
    title: '',
    priority: 'medium',
    status: 'todo',
  })

  const { data: tasks = [], isLoading } = useQuery<Task[]>({
    queryKey: ['tasks'],
    queryFn: tasksApi.getAll
  })

  const createMutation = useMutation({
    mutationFn: tasksApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
      setShowForm(false)
      setNewTask({ title: '', priority: 'medium', status: 'todo' })
    }
  })

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string, data: Partial<TaskCreate> }) =>
      tasksApi.update(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    }
  })

  const deleteMutation = useMutation({
    mutationFn: tasksApi.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] })
    }
  })

  const handleCreate = (e: React.FormEvent) => {
    e.preventDefault()
    createMutation.mutate(newTask)
  }

  const toggleStatus = (task: Task) => {
    const next = task.status === 'todo' ? 'in_progress'
      : task.status === 'in_progress' ? 'done' : 'todo'
    updateMutation.mutate({ id: task.id, data: { status: next } })
  }

  if (isLoading) return (
    <div className="flex items-center justify-center h-64">
      <div className="text-gray-400">Loading tasks...</div>
    </div>
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Tasks</h2>
          <p className="text-gray-500 mt-1">
            {tasks.filter(t => t.status !== 'done').length} pending
          </p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-primary-600 hover:bg-primary-700 text-white 
            px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          + New Task
        </button>
      </div>

      {/* New Task Form */}
      {showForm && (
        <div className="bg-white rounded-xl shadow-sm border 
          border-gray-100 p-5">
          <h3 className="font-semibold text-gray-900 mb-4">
            Create New Task
          </h3>
          <form onSubmit={handleCreate} className="space-y-4">
            <input
              type="text"
              placeholder="Task title"
              value={newTask.title}
              onChange={(e) => setNewTask({ 
                ...newTask, title: e.target.value 
              })}
              className="w-full px-4 py-2.5 border border-gray-300 
                rounded-lg focus:ring-2 focus:ring-primary-500 
                focus:border-transparent outline-none"
              required
            />
            <div className="grid grid-cols-2 gap-4">
              <select
                value={newTask.priority}
                onChange={(e) => setNewTask({ 
                  ...newTask, 
                  priority: e.target.value as TaskCreate['priority'] 
                })}
                className="px-4 py-2.5 border border-gray-300 rounded-lg
                  focus:ring-2 focus:ring-primary-500 outline-none"
              >
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
              </select>
              <input
                type="date"
                value={newTask.due_date || ''}
                onChange={(e) => setNewTask({ 
                  ...newTask, due_date: e.target.value 
                })}
                className="px-4 py-2.5 border border-gray-300 rounded-lg
                  focus:ring-2 focus:ring-primary-500 outline-none"
              />
            </div>
            <div className="flex gap-3">
              <button type="submit"
                disabled={createMutation.isPending}
                className="bg-primary-600 hover:bg-primary-700 text-white 
                  px-4 py-2 rounded-lg text-sm font-medium 
                  transition-colors disabled:opacity-50"
              >
                {createMutation.isPending ? 'Creating...' : 'Create Task'}
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

      {/* Task List */}
      <div className="bg-white rounded-xl shadow-sm border 
        border-gray-100 divide-y divide-gray-50">
        {tasks.length === 0 ? (
          <div className="p-8 text-center text-gray-400">
            No tasks yet — create your first one!
          </div>
        ) : (
          tasks.map((task) => (
            <div key={task.id} 
              className="flex items-center gap-4 p-4 hover:bg-gray-50 
                transition-colors">
              <button
                onClick={() => toggleStatus(task)}
                className={`w-6 h-6 rounded-full border-2 flex-shrink-0
                  flex items-center justify-center transition-colors ${
                  task.status === 'done'
                    ? 'bg-green-500 border-green-500 text-white'
                    : 'border-gray-300 hover:border-primary-500'
                }`}
              >
                {task.status === 'done' && '✓'}
              </button>
              <div className="flex-1 min-w-0">
                <p className={`font-medium truncate ${
                  task.status === 'done' 
                    ? 'line-through text-gray-400' 
                    : 'text-gray-900'
                }`}>
                  {task.title}
                </p>
                {task.due_date && (
                  <p className="text-xs text-gray-400 mt-0.5">
                    Due {task.due_date}
                  </p>
                )}
              </div>
              <span className={`text-xs px-2 py-1 rounded-full 
                flex-shrink-0 ${priorityColors[task.priority]}`}>
                {task.priority}
              </span>
              <span className={`text-xs px-2 py-1 rounded-full 
                flex-shrink-0 ${statusColors[task.status]}`}>
                {task.status.replace('_', ' ')}
              </span>
              <button
                onClick={() => deleteMutation.mutate(task.id)}
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