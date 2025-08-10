<template>
  <div class="user-profile">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <h2 class="mb-1">My Profile</h2>
          <p class="text-muted">Manage your account information and settings</p>
        </div>
      </div>

      <div class="row g-4">
        <!-- Profile Information -->
        <div class="col-lg-8">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Profile Information</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="updateProfile" novalidate>
                <div class="row g-3">
                  <div class="col-md-6">
                    <label for="fullName" class="form-label">Full Name</label>
                    <input
                      id="fullName"
                      v-model="profileForm.full_name"
                      type="text"
                      class="form-control"
                      :class="{ 'is-invalid': errors.full_name }"
                      required
                    >
                    <div v-if="errors.full_name" class="invalid-feedback">
                      {{ errors.full_name }}
                    </div>
                  </div>

                  <div class="col-md-6">
                    <label for="email" class="form-label">Email Address</label>
                    <input
                      id="email"
                      v-model="profileForm.email"
                      type="email"
                      class="form-control"
                      :class="{ 'is-invalid': errors.email }"
                      required
                    >
                    <div v-if="errors.email" class="invalid-feedback">
                      {{ errors.email }}
                    </div>
                  </div>

                  <div class="col-md-6">
                    <label for="qualification" class="form-label">Qualification</label>
                    <input
                      id="qualification"
                      v-model="profileForm.qualification"
                      type="text"
                      class="form-control"
                      :class="{ 'is-invalid': errors.qualification }"
                      required
                    >
                    <div v-if="errors.qualification" class="invalid-feedback">
                      {{ errors.qualification }}
                    </div>
                  </div>

                  <div class="col-md-6">
                    <label for="dob" class="form-label">Date of Birth</label>
                    <input
                      id="dob"
                      v-model="profileForm.dob"
                      type="date"
                      class="form-control"
                      :class="{ 'is-invalid': errors.dob }"
                      required
                    >
                    <div v-if="errors.dob" class="invalid-feedback">
                      {{ errors.dob }}
                    </div>
                  </div>
                </div>

                <div class="row mt-4">
                  <div class="col-12">
                    <button 
                      type="submit" 
                      class="btn btn-primary"
                      :disabled="profileLoading"
                    >
                      <span v-if="profileLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                      {{ profileLoading ? 'Updating...' : 'Update Profile' }}
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>

          <!-- Password Change -->
          <div class="card mt-4">
            <div class="card-header">
              <h5 class="mb-0">Change Password</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="changePassword" novalidate>
                <div class="row g-3">
                  <div class="col-12">
                    <label for="currentPassword" class="form-label">Current Password</label>
                    <input
                      id="currentPassword"
                      v-model="passwordForm.current_password"
                      type="password"
                      class="form-control"
                      :class="{ 'is-invalid': errors.current_password }"
                      required
                    >
                    <div v-if="errors.current_password" class="invalid-feedback">
                      {{ errors.current_password }}
                    </div>
                  </div>

                  <div class="col-md-6">
                    <label for="newPassword" class="form-label">New Password</label>
                    <input
                      id="newPassword"
                      v-model="passwordForm.new_password"
                      type="password"
                      class="form-control"
                      :class="{ 'is-invalid': errors.new_password }"
                      required
                    >
                    <div v-if="errors.new_password" class="invalid-feedback">
                      {{ errors.new_password }}
                    </div>
                    <div class="form-text">Password must be at least 6 characters long.</div>
                  </div>

                  <div class="col-md-6">
                    <label for="confirmPassword" class="form-label">Confirm New Password</label>
                    <input
                      id="confirmPassword"
                      v-model="passwordForm.confirm_password"
                      type="password"
                      class="form-control"
                      :class="{ 'is-invalid': errors.confirm_password }"
                      required
                    >
                    <div v-if="errors.confirm_password" class="invalid-feedback">
                      {{ errors.confirm_password }}
                    </div>
                  </div>
                </div>

                <div class="row mt-4">
                  <div class="col-12">
                    <button 
                      type="submit" 
                      class="btn btn-warning"
                      :disabled="passwordLoading"
                    >
                      <span v-if="passwordLoading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                      {{ passwordLoading ? 'Changing...' : 'Change Password' }}
                    </button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>

        <!-- Profile Summary -->
        <div class="col-lg-4">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Profile Summary</h5>
            </div>
            <div class="card-body">
              <div class="text-center mb-4">
                <div class="profile-avatar">
                  <i class="fas fa-user fa-4x text-muted"></i>
                </div>
                <h5 class="mt-3 mb-1">{{ user?.full_name }}</h5>
                <p class="text-muted">{{ user?.qualification }}</p>
                <span class="badge bg-primary">{{ user?.role?.toUpperCase() }}</span>
              </div>

              <div class="profile-info">
                <div class="info-item mb-3">
                  <label class="form-label small text-muted">Email</label>
                  <p class="mb-0">{{ user?.email }}</p>
                </div>
                
                <div class="info-item mb-3">
                  <label class="form-label small text-muted">Date of Birth</label>
                  <p class="mb-0">{{ formatDate(user?.dob) }}</p>
                </div>
                
                <div class="info-item mb-3">
                  <label class="form-label small text-muted">Member Since</label>
                  <p class="mb-0">{{ formatDate(user?.created_at) }}</p>
                </div>
                
                <div class="info-item">
                  <label class="form-label small text-muted">Last Login</label>
                  <p class="mb-0">{{ user?.last_login ? formatDateTime(user.last_login) : 'Never' }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Quiz Stats -->
          <div class="card mt-4">
            <div class="card-header">
              <h5 class="mb-0">Quiz Statistics</h5>
            </div>
            <div class="card-body">
              <div class="stat-item d-flex justify-content-between mb-3">
                <span class="text-muted">Total Attempts</span>
                <strong>{{ stats.totalAttempts }}</strong>
              </div>
              
              <div class="stat-item d-flex justify-content-between mb-3">
                <span class="text-muted">Average Score</span>
                <strong>{{ stats.averageScore }}%</strong>
              </div>
              
              <div class="stat-item d-flex justify-content-between mb-3">
                <span class="text-muted">Best Score</span>
                <strong>{{ stats.bestScore }}%</strong>
              </div>
              
              <div class="stat-item d-flex justify-content-between">
                <span class="text-muted">Completed Quizzes</span>
                <strong>{{ stats.completedQuizzes }}</strong>
              </div>
            </div>
          </div>

          <!-- Account Actions -->
          <div class="card mt-4">
            <div class="card-header">
              <h5 class="mb-0">Account Actions</h5>
            </div>
            <div class="card-body">
              <div class="d-grid gap-2">
                <router-link to="/user/scores" class="btn btn-outline-primary">
                  <i class="fas fa-chart-line me-2"></i>
                  View Quiz History
                </router-link>
                
                <router-link to="/user/quizzes" class="btn btn-outline-success">
                  <i class="fas fa-play me-2"></i>
                  Take a Quiz
                </router-link>
                
                <button @click="exportData" class="btn btn-outline-info">
                  <i class="fas fa-download me-2"></i>
                  Export My Data
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import api from '@/services/api'

export default {
  name: 'UserProfile',
  data() {
    return {
      profileForm: {
        full_name: '',
        email: '',
        qualification: '',
        dob: ''
      },
      passwordForm: {
        current_password: '',
        new_password: '',
        confirm_password: ''
      },
      stats: {
        totalAttempts: 0,
        averageScore: 0,
        bestScore: 0,
        completedQuizzes: 0
      },
      errors: {},
      profileLoading: false,
      passwordLoading: false
    }
  },
  computed: {
    ...mapState('auth', ['user'])
  },
  async mounted() {
    this.initializeProfileForm()
    await this.loadStats()
  },
  methods: {
    initializeProfileForm() {
      if (this.user) {
        this.profileForm = {
          full_name: this.user.full_name || '',
          email: this.user.email || '',
          qualification: this.user.qualification || '',
          dob: this.user.dob || ''
        }
      }
    },
    async loadStats() {
      try {
        const response = await api.get('/user/dashboard/stats')
        this.stats = response.data || this.stats
      } catch (error) {
        console.error('Error loading stats:', error)
      }
    },
    async updateProfile() {
      try {
        this.profileLoading = true
        this.errors = {}
        
        // Validate form
        if (!this.validateProfileForm()) {
          return
        }
        
        const response = await api.put('/user/profile', this.profileForm)
        
        // Update user in store
        await this.$store.dispatch('auth/updateUser', response.data.user)
        
        this.$store.dispatch('alerts/addAlert', {
          type: 'success',
          message: 'Profile updated successfully'
        })
      } catch (error) {
        console.error('Error updating profile:', error)
        if (error.response?.data?.errors) {
          this.errors = error.response.data.errors
        } else {
          this.$store.dispatch('alerts/addAlert', {
            type: 'error',
            message: error.response?.data?.message || 'Failed to update profile'
          })
        }
      } finally {
        this.profileLoading = false
      }
    },
    async changePassword() {
      try {
        this.passwordLoading = true
        this.errors = {}
        
        // Validate password form
        if (!this.validatePasswordForm()) {
          return
        }
        
        await api.put('/user/change-password', this.passwordForm)
        
        // Clear password form
        this.passwordForm = {
          current_password: '',
          new_password: '',
          confirm_password: ''
        }
        
        this.$store.dispatch('alerts/addAlert', {
          type: 'success',
          message: 'Password changed successfully'
        })
      } catch (error) {
        console.error('Error changing password:', error)
        if (error.response?.data?.errors) {
          this.errors = error.response.data.errors
        } else {
          this.$store.dispatch('alerts/addAlert', {
            type: 'error',
            message: error.response?.data?.message || 'Failed to change password'
          })
        }
      } finally {
        this.passwordLoading = false
      }
    },
    validateProfileForm() {
      const errors = {}
      
      if (!this.profileForm.full_name.trim()) {
        errors.full_name = 'Full name is required'
      }
      
      if (!this.profileForm.email.trim()) {
        errors.email = 'Email is required'
      } else if (!/\S+@\S+\.\S+/.test(this.profileForm.email)) {
        errors.email = 'Email is invalid'
      }
      
      if (!this.profileForm.qualification.trim()) {
        errors.qualification = 'Qualification is required'
      }
      
      if (!this.profileForm.dob) {
        errors.dob = 'Date of birth is required'
      }
      
      this.errors = errors
      return Object.keys(errors).length === 0
    },
    validatePasswordForm() {
      const errors = {}
      
      if (!this.passwordForm.current_password) {
        errors.current_password = 'Current password is required'
      }
      
      if (!this.passwordForm.new_password) {
        errors.new_password = 'New password is required'
      } else if (this.passwordForm.new_password.length < 6) {
        errors.new_password = 'Password must be at least 6 characters long'
      }
      
      if (!this.passwordForm.confirm_password) {
        errors.confirm_password = 'Please confirm your new password'
      } else if (this.passwordForm.new_password !== this.passwordForm.confirm_password) {
        errors.confirm_password = 'Passwords do not match'
      }
      
      this.errors = errors
      return Object.keys(errors).length === 0
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    formatDateTime(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    async exportData() {
      try {
        const response = await api.get('/user/export-data', {
          responseType: 'blob'
        })
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `my-quiz-data-${new Date().toISOString().split('T')[0]}.json`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
        
        this.$store.dispatch('alerts/addAlert', {
          type: 'success',
          message: 'Data exported successfully'
        })
      } catch (error) {
        console.error('Error exporting data:', error)
        this.$store.dispatch('alerts/addAlert', {
          type: 'error',
          message: 'Failed to export data'
        })
      }
    }
  },
  watch: {
    user: {
      immediate: true,
      handler() {
        this.initializeProfileForm()
      }
    }
  }
}
</script>

<style scoped>
.user-profile {
  padding: 20px 0;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: #f8f9fa;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
  border: 3px solid #e9ecef;
}

.profile-info .info-item {
  border-bottom: 1px solid #f8f9fa;
  padding-bottom: 15px;
}

.profile-info .info-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.stat-item {
  padding: 10px 0;
  border-bottom: 1px solid #f8f9fa;
}

.stat-item:last-child {
  border-bottom: none;
}

.card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.form-control:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0, 123, 255, 0.25);
}

.btn {
  border-radius: 6px;
}
</style>
