import apiClient from './client'
import type { AuthToken, LoginCredentials, RegisterData, User } from '../types'

export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthToken> => {
    const formData = new FormData()
    formData.append('username', credentials.username)
    formData.append('password', credentials.password)
    const response = await apiClient.post<AuthToken>('/auth/login', 
      formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      }
    )
    return response.data
  },

  register: async (data: RegisterData): Promise<User> => {
    const response = await apiClient.post<User>('/auth/register', data)
    return response.data
  },

  getMe: async (): Promise<User> => {
    const response = await apiClient.get<User>('/users/me')
    return response.data
  },

  getHouseholdMembers: async (): Promise<User[]> => {
    const response = await apiClient.get<User[]>('/users/household')
    return response.data
  }
}