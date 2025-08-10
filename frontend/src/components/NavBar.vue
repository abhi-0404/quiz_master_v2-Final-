<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">
        <i class="fas fa-graduation-cap me-2"></i>
        Quiz Master V2
      </router-link>
      
      <button 
        class="navbar-toggler" 
        type="button" 
        data-bs-toggle="collapse" 
        data-bs-target="#navbarNav"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <div class="navbar-nav ms-auto">
          <div class="nav-item dropdown">
            <a 
              class="nav-link dropdown-toggle" 
              href="#" 
              id="navbarDropdown" 
              role="button" 
              data-bs-toggle="dropdown"
            >
              <i class="fas fa-user me-1"></i>
              {{ currentUser?.full_name || 'User' }}
            </a>
            <ul class="dropdown-menu">
              <li v-if="userRole === 'user'">
                <router-link class="dropdown-item" to="/user/profile">
                  <i class="fas fa-user-edit me-2"></i>
                  Profile
                </router-link>
              </li>
              <li><hr class="dropdown-divider"></li>
              <li>
                <a class="dropdown-item" href="#" @click="handleLogout">
                  <i class="fas fa-sign-out-alt me-2"></i>
                  Logout
                </a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'NavBar',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const currentUser = computed(() => store.getters['auth/currentUser'])
    const userRole = computed(() => store.getters['auth/userRole'])
    
    const handleLogout = async () => {
      try {
        await store.dispatch('auth/logout')
        router.push('/auth')
      } catch (error) {
        console.error('Logout error:', error)
      }
    }
    
    return {
      currentUser,
      userRole,
      handleLogout
    }
  }
}
</script>

<style scoped>
.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
}

.dropdown-item:hover {
  background-color: rgba(var(--primary-color), 0.1);
}
</style>
