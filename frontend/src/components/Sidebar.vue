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
        <ul class="nav nav-pills flex-column">
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
          </template>
        </ul>
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

export default {
  name: 'Sidebar',
  setup() {
    const store = useStore()
    const sidebarOpen = ref(false)
    
    const userRole = computed(() => store.getters['auth/userRole'])
    
    const toggleSidebar = () => {
      sidebarOpen.value = !sidebarOpen.value
    }
    
    const closeSidebar = () => {
      sidebarOpen.value = false
    }
    
    return {
      userRole,
      sidebarOpen,
      toggleSidebar,
      closeSidebar
    }
  }
}
</script>

<style scoped>
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
