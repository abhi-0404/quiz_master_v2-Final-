<template>
  <transition name="fade">
    <div 
      v-if="alert.show" 
      class="alert-container"
      :class="`alert-${alert.type}`"
    >
      <div class="alert-content">
        <i class="alert-icon" :class="getAlertIcon(alert.type)"></i>
        <span class="alert-message">{{ alert.message }}</span>
        <button class="alert-close" @click="closeAlert">
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>
  </transition>
</template>

<script>
import { computed } from 'vue'
import { useStore } from 'vuex'

export default {
  name: 'AlertMessage',
  setup() {
    const store = useStore()
    
    const alert = computed(() => store.getters.alert)
    
    const getAlertIcon = (type) => {
      const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
      }
      return icons[type] || icons.info
    }
    
    const closeAlert = () => {
      store.dispatch('clearAlert')
    }
    
    return {
      alert,
      getAlertIcon,
      closeAlert
    }
  }
}
</script>

<style scoped>
.alert-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9999;
  min-width: 300px;
  max-width: 500px;
  border-radius: 0.375rem;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  overflow: hidden;
}

.alert-content {
  display: flex;
  align-items: center;
  padding: 1rem;
  color: white;
  font-weight: 500;
}

.alert-icon {
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.alert-message {
  flex: 1;
}

.alert-close {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  margin-left: 0.75rem;
  padding: 0.25rem;
  border-radius: 0.25rem;
  transition: background-color 0.2s ease;
}

.alert-close:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

.alert-success {
  background-color: var(--success-color);
}

.alert-error {
  background-color: var(--danger-color);
}

.alert-warning {
  background-color: var(--warning-color);
  color: #212529;
}

.alert-warning .alert-close {
  color: #212529;
}

.alert-warning .alert-close:hover {
  background-color: rgba(0, 0, 0, 0.1);
}

.alert-info {
  background-color: var(--info-color);
}

.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.fade-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

@media (max-width: 768px) {
  .alert-container {
    right: 10px;
    left: 10px;
    min-width: auto;
  }
}
</style>
