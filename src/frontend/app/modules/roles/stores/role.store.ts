import { defineStore } from 'pinia'
import { ref } from 'vue'
import { roleApi } from '../api/role.api'
import type { RoleItem } from '../types/role.types'

export const useRoleStore = defineStore('role', () => {
  const roles = ref<RoleItem[]>([])
  const isLoading = ref<boolean>(false)

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

  return {
    roles,
    isLoading,
    fetchRoles
  }
})
