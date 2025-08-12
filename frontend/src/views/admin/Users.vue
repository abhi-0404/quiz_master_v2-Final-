<template>
  <div class="admin-users">
    <div class="container-fluid">
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-section bg-primary text-white p-4 rounded shadow-sm d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Manage Users</h2>
              <p class="mb-0 opacity-75">View and manage user accounts</p>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status"></div>
              </div>
              <div v-else>
                <table class="table table-bordered table-hover">
                  <thead class="table-light text-center">
                    <tr>
                      <th>S.No</th>
                      <th>Name</th>
                      <th>Email</th>
                      <th>Role</th>
                      <th>Join</th>
                      <th>Total Attempts</th>
                      <th>Average Score (%)</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(user, idx) in users" :key="user.id">
                      <td class="text-center">{{ idx + 1 }}</td>
                      <td>{{ user.full_name }}</td>
                      <td>{{ user.email }}</td>
                      <td>
                        <select v-model="user.role" @change="updateUserRole(user)" class="form-select form-select-sm">
                          <option value="user">User</option>
                          <option value="admin">Admin</option>
                        </select>
                      </td>
                      <td>{{ formatDate(user.created_at) }}</td>
                      <td class="text-center">{{ user.total_attempts || 0 }}</td>
                      <td class="text-center">{{ user.average_score != null ? user.average_score.toFixed(2) : '-' }}</td>
                      <td class="text-center">
                        <button class="btn btn-sm btn-danger" @click="removeUser(user.id)">
                          <i class="fas fa-trash-alt"></i> Remove
                        </button>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="users.length === 0" class="text-center text-muted py-4">
                  <i class="fas fa-users fa-3x mb-3 opacity-50"></i>
                  <p>No users found.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI } from '@/services/api'

export default {
  name: 'AdminUsers',
  data() {
    return {
      users: [],
      loading: true
    }
  },
  async mounted() {
    await this.loadUsers()
  },
  methods: {
    async loadUsers() {
      this.loading = true
      try {
        const response = await adminAPI.getUsers()
        this.users = response.data.users || []
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load users.'
        })
      } finally {
        this.loading = false
      }
    },
    async removeUser(userId) {
      if (!confirm('Are you sure you want to remove this user and all their data?')) return
      try {
        await adminAPI.deleteUserAndData(userId)
        this.users = this.users.filter(u => u.id !== userId)
        this.$store.dispatch('showAlert', {
          type: 'success',
          message: 'User and all related data removed successfully.'
        })
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to remove user and data.'
        })
      }
    },
    async updateUserRole(user) {
      try {
        const response = await adminAPI.updateUserRole(user.id, { role: user.role })
        // Optionally update local user data with response
        user.role = response.data.user.role
        this.$store.dispatch('showAlert', {
          type: 'success',
          message: 'User role updated.'
        })
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to update user role.'
        this.$store.dispatch('showAlert', {
          type: 'error',
          message
        })
      }
    },
    formatDate(dateStr) {
      const date = new Date(dateStr)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  }
}
</script>
