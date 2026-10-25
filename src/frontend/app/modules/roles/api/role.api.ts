import { apiClient } from '~/api/client'
import { ENDPOINTS } from '~/api/endpoints'
import type { RoleItem } from '../types/role.types'

export const roleApi = {
  async getAll(): Promise<{ success: boolean; message: string; data: RoleItem[] }> {
    const response = await apiClient.get(ENDPOINTS.ROLES.BASE)
    return response.data
  }
}
