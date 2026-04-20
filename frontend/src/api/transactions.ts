import apiClient from './client'
import type { Transaction, TransactionCreate } from '../types'

export const transactionsApi = {
  getAll: async (): Promise<Transaction[]> => {
    const response = await apiClient.get<Transaction[]>('/transactions/')
    return response.data
  },

  getById: async (id: string): Promise<Transaction> => {
    const response = await apiClient.get<Transaction>(`/transactions/${id}`)
    return response.data
  },

  create: async (data: TransactionCreate): Promise<Transaction> => {
    const response = await apiClient.post<Transaction>(
      '/transactions/', data
    )
    return response.data
  },

  update: async (id: string, 
    data: Partial<TransactionCreate>): Promise<Transaction> => {
    const response = await apiClient.put<Transaction>(
      `/transactions/${id}`, data
    )
    return response.data
  },

  delete: async (id: string): Promise<void> => {
    await apiClient.delete(`/transactions/${id}`)
  }
}