<script setup lang="ts">
// Layout default otomatis memanggil AppSidebar dan AppNavbar
</script>

<template>
  <div class="flex h-screen w-full overflow-hidden bg-slate-50 text-slate-900">
    <!-- Sidebar -->
    <LayoutAppSidebar />

    <!-- Area Kanan (Navbar + Konten Halaman) -->
    <div class="flex flex-1 flex-col overflow-hidden">
      <!-- Navbar (Sementara bisa placeholder dulu jika belum selesai) -->
      <LayoutAppNavbar />

      <!-- Konten Halaman yang sedang aktif -->
      <main class="flex-1 overflow-y-auto p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
