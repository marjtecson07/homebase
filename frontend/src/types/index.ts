export interface User {
  id: string
  email: string
  full_name: string
  is_active: boolean
  household_id: string | null
  created_at: string
  updated_at: string
}

export interface Task {
  id: string
  title: string
  description: string | null
  status: 'todo' | 'in_progress' | 'done'
  priority: 'low' | 'medium' | 'high'
  due_date: string | null
  is_recurring: boolean
  recurrence_rule: string | null
  category_id: string | null
  assigned_to_id: string | null
  household_id: string
  created_by_id: string
  created_at: string
  updated_at: string
}

export interface Transaction {
  id: string
  description: string
  amount: number
  type: 'income' | 'expense'
  date: string
  is_shared: boolean
  category_id: string | null
  household_id: string
  created_by_id: string
  created_at: string
  updated_at: string
}

export interface Budget {
  id: string
  amount: number
  month: number
  year: number
  category_id: string
  household_id: string
  created_at: string
  updated_at: string
}

export interface SavingsGoal {
  id: string
  name: string
  target_amount: number
  current_amount: number
  target_date: string | null
  household_id: string
  created_at: string
  updated_at: string
}

export interface AuthToken {
  access_token: string
  token_type: string
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface RegisterData {
  email: string
  full_name: string
  password: string
}

export interface TaskCreate {
  title: string
  description?: string
  status?: 'todo' | 'in_progress' | 'done'
  priority?: 'low' | 'medium' | 'high'
  due_date?: string
  is_recurring?: boolean
  recurrence_rule?: string
  category_id?: string
  assigned_to_id?: string
}

export interface TransactionCreate {
  description: string
  amount: number
  type: 'income' | 'expense'
  date: string
  is_shared?: boolean
  category_id?: string
}