import { defineStore } from 'pinia'
import { ref } from 'vue'
import { roleApi } from '../api/role.api'
import type { RoleItem, CreateRoleRequestPayload, RoleRequestItem } from '../types/role.types'

export const useRoleStore = defineStore('role', () => {
  const roles = ref<RoleItem[]>([])
  const myRequest = ref<RoleRequestItem | null>(null)
  const isLoading = ref<boolean>(false)
  const isSubmitting = ref<boolean>(false)

  const fetchRoles = async (force = false) => {
    if (roles.value.length > 0 && !force) return roles.value

    isLoading.value = true
    try {
      const res = await roleApi.getAll()
      roles.value = res.data || []
      return roles.value
    } catch (err) {
      console.error('Failed to fetch roles:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const submitRoleRequest = async (payload: CreateRoleRequestPayload) => {
    isSubmitting.value = true
    try {
      const res = await roleApi.submitRequest(payload)
      if (res.data) {
        myRequest.value = res.data
      }
      return res
    } finally {
      isSubmitting.value = false
    }
  }

  const fetchMyRequest = async () => {
    try {
      const res = await roleApi.getMyRequest()
      myRequest.value = res.data || null
      return myRequest.value
    } catch (err) {
      console.error('Failed to fetch my role request:', err)
      return null
    }
  }
  return {
    roles,
    isLoading,
    fetchRoles,
    myRequest,
    isSubmitting,
    submitRoleRequest,
    fetchMyRequest
  }
})
