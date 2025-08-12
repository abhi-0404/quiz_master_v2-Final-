<template>
  <div class="admin-profile">
    <div class="container-fluid">
      <!-- Blue Rectangle Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-section bg-primary text-white p-4 rounded shadow-sm d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Admin Profile</h2>
              <p class="mb-0 opacity-75">Manage your account information and settings</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row g-4">
        <div class="col-12">
          <div class="card bg-dark text-white p-4 d-flex flex-row align-items-stretch" style="min-height:220px;">
            <!-- Avatar and Info Left -->
            <div class="profile-left d-flex flex-column align-items-center justify-content-center border-end" style="min-width:260px; border-right: 3px solid #2196f3;">
              <div class="profile-avatar mb-2">
                <i class="fas fa-user-circle fa-5x" style="color:#bdbdbd;"></i>
              </div>
              <div class="fw-bold" style="font-size:1.2rem;">{{ profileForm.full_name }}</div>
              <span class="badge bg-primary mt-1" style="font-size:0.85rem;">ADMIN</span>
            </div>
            <!-- Form Right -->
            <div class="profile-form flex-grow-1 ps-4 d-flex flex-column justify-content-center">
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
                <div class="mt-4">
                  <button type="submit" class="btn btn-primary">Update Profile</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <!-- Password Change Section Below -->
      <div class="row mt-4">
        <div class="col-12">
          <div class="card bg-dark text-white p-4">
            <h5 class="mb-3">Change Password</h5>
            <form @submit.prevent="changePassword" novalidate>
              <div class="row g-3">
                <div class="col-md-4">
                  <label for="currentPassword" class="form-label">Current Password</label>
                  <input id="currentPassword" v-model="passwordForm.current_password" type="password" class="form-control" required>
                </div>
                <div class="col-md-4">
                  <label for="newPassword" class="form-label">New Password</label>
                  <input id="newPassword" v-model="passwordForm.new_password" type="password" class="form-control" required>
                </div>
                <div class="col-md-4">
                  <label for="confirmPassword" class="form-label">Confirm New Password</label>
                  <input id="confirmPassword" v-model="passwordForm.confirm_password" type="password" class="form-control" required>
                </div>
              </div>
              <div class="mt-4">
                <button type="submit" class="btn btn-warning">Change Password</button>
              </div>
            </form>
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
  name: 'AdminProfile',
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
      errors: {}
    }
  },
  computed: {
    ...mapState('auth', ['user'])
  },
  mounted() {
    if (this.user) {
      this.profileForm.full_name = this.user.full_name
      this.profileForm.email = this.user.email
      this.profileForm.qualification = this.user.qualification
      this.profileForm.dob = this.user.dob ? this.user.dob.split('T')[0] : ''
    }
  },
  methods: {
    async updateProfile() {
      this.errors = {}
      try {
        const response = await api.put('/admin/profile', this.profileForm)
        this.$store.dispatch('alerts/addAlert', {
          type: 'success',
          message: 'Profile updated successfully!'
        })
        // Optionally update user in store
        this.$store.commit('auth/setUser', response.data.user)
      } catch (error) {
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors
        } else {
          this.$store.dispatch('alerts/addAlert', {
            type: 'error',
            message: 'Failed to update profile.'
          })
        }
      }
    }
  }
}
</script>

<style scoped>
/* Profile page styles */
.user-profile, .admin-profile {
  padding: 20px 0;
}
.profile-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: #23232b;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}
</style>
