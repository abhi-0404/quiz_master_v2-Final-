<template>
  <div>
    <div class="sidebar bg-light border-end" :class="{ 'sidebar-open': sidebarOpen }">
      <div class="sidebar-header p-3 border-bottom">
        <h5 class="mb-0" style="color: #000;">
          <i class="fas fa-tachometer-alt me-2"></i>
          {{ userRole === 'admin' ? 'Admin Panel' : 'Dashboard' }}
        </h5>
      </div>
      
      <div class="sidebar-body">
  <ul class="nav nav-pills flex-column" style="min-height: 60vh;">
          <!-- User Menu Items -->
          <template v-if="userRole === 'user'">
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'UserDashboard' }"
                to="/user/dashboard"
              >
                <i class="fas fa-home me-2"></i>
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'UserQuizzes' }"
                to="/user/quizzes"
              >
                <i class="fas fa-question-circle me-2"></i>
                Take Quiz
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'UserScores' }"
                to="/user/scores"
              >
                <i class="fas fa-chart-line me-2"></i>
                My Scores
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'UserProfile' }"
                to="/user/profile"
              >
                <i class="fas fa-user me-2"></i>
                Profile
              </router-link>
            </li>
          </template>
          
          <!-- Admin Menu Items -->
          <template v-if="userRole === 'admin'">
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'AdminDashboard' }"
                to="/admin/dashboard"
              >
                <i class="fas fa-tachometer-alt me-2"></i>
                Dashboard
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'AdminSubjects' }"
                to="/admin/subjects"
              >
                <i class="fas fa-book me-2"></i>
                Subjects
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'AdminChapters' }"
                to="/admin/chapters"
              >
                <i class="fas fa-bookmark me-2"></i>
                Chapters
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'AdminQuizzes' }"
                to="/admin/quizzes"
              >
                <i class="fas fa-question-circle me-2"></i>
                Quizzes
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'AdminUsers' }"
                to="/admin/users"
              >
                <i class="fas fa-users me-2"></i>
                Users
              </router-link>
            </li>
            <li class="nav-item">
              <router-link 
                class="nav-link" 
                :class="{ active: $route.name === 'AdminProfile' }"
                to="/admin/profile"
              >
                <i class="fas fa-user me-2"></i>
                Profile
              </router-link>
            </li>
          </template>
        </ul>
      </div>
      <!-- Logout button at bottom -->
      <div class="sidebar-footer px-3 pb-3 mt-auto">
        <button class="btn btn-danger w-100" @click="logout">
          <i class="fas fa-sign-out-alt me-2"></i> Logout
        </button>
      </div>
      <!-- Mobile toggle button -->
      <button 
        class="sidebar-toggle d-lg-none" 
        @click="toggleSidebar"
        aria-label="Toggle sidebar"
      >
        <i class="fas fa-bars"></i>
      </button>
    </div>
    <!-- Sidebar overlay for mobile -->
    <div 
      v-if="sidebarOpen" 
      class="sidebar-overlay d-lg-none" 
      @click="closeSidebar"
    ></div>
  </div>
</template>

<script>
import { computed, ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'Sidebar',
  setup() {
    const store = useStore()
    const router = useRouter()
    const sidebarOpen = ref(false)

    const userRole = computed(() => store.getters['auth/userRole'])

    const toggleSidebar = () => {
      sidebarOpen.value = !sidebarOpen.value
    }

    const closeSidebar = () => {
      sidebarOpen.value = false
    }

    const logout = async () => {
      await store.dispatch('auth/logout')
      router.push('/auth')
    }

    return {
      userRole,
      sidebarOpen,
      toggleSidebar,
      closeSidebar,
      logout
    }
  }
}
</script>

<style scoped>
.sidebar-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
}
.sidebar {
  position: fixed;
  top: 60px; /* Height of navbar */
  left: 0;
  width: 250px;
  height: calc(100vh - 60px);
  z-index: 1000;
  overflow-y: auto;
  transition: transform 0.3s ease;
}

.sidebar-header {
  background-color: rgba(var(--primary-color), 0.05);
}

.sidebar-body {
  padding: 1rem;
}

.nav-link {
  color: #495057;
  border-radius: 0.375rem;
  margin-bottom: 0.25rem;
  transition: all 0.2s ease;
}

.nav-link:hover {
  background-color: rgba(var(--primary-color), 0.1);
  color: var(--primary-color);
}

.nav-link.active {
  background-color: var(--primary-color);
  color: white;
}

.sidebar-toggle {
  position: absolute;
  top: 50%;
  right: -40px;
  transform: translateY(-50%);
  background-color: var(--primary-color);
  color: white;
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 0 0.375rem 0.375rem 0;
  z-index: 1001;
}

.sidebar-overlay {
  position: fixed;
  top: 60px;
  left: 0;
  width: 100%;
  height: calc(100vh - 60px);
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

/* Mobile styles */
@media (max-width: 768px) {
  .sidebar {
    transform: translateX(-100%);
  }
  
  .sidebar.sidebar-open {
    transform: translateX(0);
  }
}

/* Desktop styles */
@media (min-width: 769px) {
  .sidebar-toggle {
    display: none;
  }
}
</style>
