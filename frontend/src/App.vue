<template>
  <div id="app">
    <NavBar v-if="$store.getters.isAuthenticated" />
    <div class="main-container" :class="{ 'with-navbar': $store.getters.isAuthenticated }">
      <Sidebar v-if="$store.getters.isAuthenticated && $route.meta.requiresSidebar !== false" />
      <main class="content" :class="{ 'with-sidebar': $store.getters.isAuthenticated && $route.meta.requiresSidebar !== false }">
        <router-view />
      </main>
    </div>
    
    <!-- Alert Component -->
    <AlertMessage />
    
    <!-- Loading Overlay -->
    <LoadingOverlay v-if="$store.getters.isLoading" />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import Sidebar from './components/Sidebar.vue'
import AlertMessage from './components/AlertMessage.vue'
import LoadingOverlay from './components/LoadingOverlay.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    Sidebar,
    AlertMessage,
    LoadingOverlay
  },
  async created() {
    // Check if user is logged in on app start
    const token = localStorage.getItem('token')
    if (token) {
      try {
        await this.$store.dispatch('auth/verifyToken')
      } catch (error) {
        // Token is invalid, remove it
        localStorage.removeItem('token')
        this.$router.push('/auth')
      }
    }
  }
}
</script>

<style lang="scss">
#app {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  min-height: 100vh;
  background-color: #f8f9fa;
}

.main-container {
  min-height: 100vh;
  
  &.with-navbar {
    padding-top: 60px; // Height of navbar
  }
}

.content {
  min-height: calc(100vh - 60px);
  padding: 20px;
  
  &.with-sidebar {
    margin-left: 250px; // Width of sidebar
    
    @media (max-width: 768px) {
      margin-left: 0;
    }
  }
  
  @media (max-width: 768px) {
    padding: 15px;
  }
}

// Custom scrollbar
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
