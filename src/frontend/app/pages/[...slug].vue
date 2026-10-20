<script setup lang="ts">
import { ref, onMounted } from 'vue'
import NotFoundView from '../components/NotFoundView.vue'

definePageMeta({
  layout: false // layout diatur dinamis di template
})

const route = useRoute()

// State lokal sementara (default: true -> simulasi user ber-sidebar)
const isLoggedIn = ref(true)

onMounted(() => {
  // Fitur testing: jika URL diberi query '?auth=0' maka render versi tanpa sidebar
  if (route.query.auth === '0' || route.query.auth === 'false') {
    isLoggedIn.value = false
    return
  }

  // Atau baca dari localStorage jika ada
  const savedAuth = localStorage.getItem('is_logged_in')
  if (savedAuth !== null) {
    isLoggedIn.value = savedAuth === 'true'
  }
})
</script>

<template>
  <NuxtLayout :name="isLoggedIn ? 'default' : 'auth'">
    <NotFoundView :is-logged-in="isLoggedIn" />
  </NuxtLayout>
</template>
