import { apiClient } from '~/api/client'
import { ENDPOINTS } from '~/api/endpoints'
import type { DivisionListResponse } from '../types/division.types'

export const divisionApi = {
  async getAll(): Promise<DivisionListResponse> {
    const response = await apiClient.get<DivisionListResponse>(ENDPOINTS.DIVISIONS.BASE)
    return response.data
  }
}
