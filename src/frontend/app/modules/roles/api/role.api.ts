import { apiClient } from '~/api/client'
import { ENDPOINTS } from '~/api/endpoints'
import type { RoleItem, CreateRoleRequestPayload, RoleRequestItem } from '../types/role.types'

export const roleApi = {
  async getAll(): Promise<{ success: boolean; message: string; data: RoleItem[] }> {
    const response = await apiClient.get(ENDPOINTS.ROLES.BASE)
    return response.data
  },
  async submitRequest(
    payload: CreateRoleRequestPayload
  ): Promise<{ success: boolean; message: string; data: RoleRequestItem }> {
    const response = await apiClient.post(ENDPOINTS.ROLES.REQUESTS, payload)
    return response.data
  },
  async getMyRequest(): Promise<{
    success: boolean
    message: string
    data: RoleRequestItem | null
  }> {
    const response = await apiClient.get(ENDPOINTS.ROLES.MY_REQUEST)
    return response.data
  }
}
