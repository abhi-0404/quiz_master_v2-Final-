<template>
  <div class="auth-view">
    <div class="container-fluid h-100">
      <div class="row h-100">
        <!-- Left side - Branding -->
        <div class="col-lg-6 auth-brand d-none d-lg-flex align-items-center" style="min-height:100vh;">
          <div class="brand-content w-100">
            <h1 class="brand-title">
              <i class="fas fa-graduation-cap me-3"></i>
              Quiz Master V2
            </h1>
            <p class="brand-subtitle">
              Your Ultimate Exam Preparation Platform
            </p>
            <div class="brand-features">
              <div class="feature-item">
                <i class="fas fa-check-circle me-2"></i>
                Multiple Choice Questions
              </div>
              <div class="feature-item">
                <i class="fas fa-clock me-2"></i>
                Timed Quizzes
              </div>
              <div class="feature-item">
                <i class="fas fa-chart-line me-2"></i>
                Performance Tracking
              </div>
              <div class="feature-item">
                <i class="fas fa-trophy me-2"></i>
                Achievement System
              </div>
            </div>
          </div>
        </div>
        
        <!-- Right side - Auth Forms -->
        <div class="col-lg-6 auth-forms">
          <div class="auth-container">
            <div class="auth-header text-center mb-4">
              <h2 class="auth-title">
                {{ isLogin ? 'Welcome Back' : 'Create Account' }}
              </h2>
              <p class="auth-description">
                {{ isLogin ? 'Sign in to your account' : 'Join Quiz Master today' }}
              </p>
            </div>
            
            <!-- Auth Tabs -->
            <div class="auth-tabs mb-4">
              <button 
                class="auth-tab" 
                :class="{ active: isLogin }"
                @click="setAuthMode(true)"
              >
                Login
              </button>
              <button 
                class="auth-tab" 
                :class="{ active: !isLogin }"
                @click="setAuthMode(false)"
              >
                Register
              </button>
            </div>
            
            <!-- Login Form -->
            <form v-if="isLogin" @submit.prevent="handleLogin" class="auth-form">
              <div class="mb-3">
                <label for="loginEmail" class="form-label">Email</label>
                <input
                  id="loginEmail"
                  v-model="loginForm.email"
                  type="email"
                  class="form-control"
                  required
                  placeholder="Enter your email"
                >
              </div>
              
              <div class="mb-3">
                <label for="loginPassword" class="form-label">Password</label>
                <input
                  id="loginPassword"
                  v-model="loginForm.password"
                  type="password"
                  class="form-control"
                  required
                  placeholder="Enter your password"
                >
              </div>
              
              <button type="submit" class="btn btn-primary w-100 mb-3">
                <i class="fas fa-sign-in-alt me-2"></i>
                Sign In
              </button>
            </form>
            
            <!-- Register Form -->
            <form v-else @submit.prevent="handleRegister" class="auth-form">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="registerFullName" class="form-label">Full Name</label>
                  <input
                    id="registerFullName"
                    v-model="registerForm.full_name"
                    type="text"
                    class="form-control"
                    required
                    placeholder="Enter your full name"
                  >
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="registerEmail" class="form-label">Email</label>
                  <input
                    id="registerEmail"
                    v-model="registerForm.email"
                    type="email"
                    class="form-control"
                    required
                    placeholder="Enter your email"
                  >
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="registerPassword" class="form-label">Password</label>
                  <input
                    id="registerPassword"
                    v-model="registerForm.password"
                    type="password"
                    class="form-control"
                    required
                    placeholder="Create a password"
                    minlength="6"
                  >
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="registerDob" class="form-label">Date of Birth</label>
                  <input
                    id="registerDob"
                    v-model="registerForm.dob"
                    type="date"
                    class="form-control"
                    required
                  >
                </div>
              </div>
              
              <div class="mb-3">
                <label for="registerQualification" class="form-label">Qualification</label>
                <input
                  id="registerQualification"
                  v-model="registerForm.qualification"
                  type="text"
                  class="form-control"
                  required
                  placeholder="Enter your qualification"
                >
              </div>
              
              <button type="submit" class="btn btn-primary w-100 mb-3">
                <i class="fas fa-user-plus me-2"></i>
                Create Account
              </button>
            </form>
            
            <!-- ...existing code... -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'

export default {
  name: 'AuthView',
  setup() {
    const store = useStore()
    const router = useRouter()
    
    const isLogin = ref(true)
    
    const loginForm = reactive({
      email: '',
      password: ''
    })
    
    const registerForm = reactive({
      full_name: '',
      email: '',
      password: '',
      qualification: '',
      dob: ''
    })
    
    const setAuthMode = (login) => {
      isLogin.value = login
      // Clear forms
      Object.keys(loginForm).forEach(key => {
        loginForm[key] = ''
      })
      Object.keys(registerForm).forEach(key => {
        registerForm[key] = ''
      })
    }
    
    const handleLogin = async () => {
      try {
        const result = await store.dispatch('auth/login', {
          email: loginForm.email,
          password: loginForm.password
        })
        
        if (result.success) {
          // Redirect based on user role
          if (result.user.role === 'admin') {
            router.push('/admin/dashboard')
          } else {
            router.push('/user/dashboard')
          }
        }
      } catch (error) {
        console.error('Login error:', error)
      }
    }
    
    const handleRegister = async () => {
      try {
        const result = await store.dispatch('auth/register', {
          full_name: registerForm.full_name,
          email: registerForm.email,
          password: registerForm.password,
          qualification: registerForm.qualification,
          dob: registerForm.dob
        })
        
        if (result.success) {
          // Switch to login form and pre-fill email
          setAuthMode(true)
          loginForm.email = registerForm.email
        }
      } catch (error) {
        console.error('Registration error:', error)
      }
    }
    
    return {
      isLogin,
      loginForm,
      registerForm,
      setAuthMode,
      handleLogin,
      handleRegister
    }
  }
}
</script>

<style scoped>
.auth-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.auth-brand {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  color: white;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.brand-content {
  text-align: center;
  max-width: 500px;
}

.brand-title {
  font-size: 3rem;
  font-weight: bold;
  margin-bottom: 1rem;
}

.brand-subtitle {
  font-size: 1.25rem;
  margin-bottom: 2rem;
  opacity: 0.9;
}

.brand-features {
  text-align: left;
}

.feature-item {
  font-size: 1.1rem;
  margin-bottom: 1rem;
  opacity: 0.95;
}

/* Auth Forms Styling */
.auth-forms {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  background-color: white;
}

/* Unified input design and white placeholder text */
/* Unified input design for all states (filled and placeholder) */
.auth-form .form-control {
  background: #f8faff;
  color: #23232b;
  border-radius: 8px;
  border: 1.5px solid #b3c2d6;
  font-size: 1rem;
  transition: border-color 0.2s;
}
.auth-form .form-control:focus {
  border-color: #2196f3;
  background: #eaf2fb;
  color: #23232b;
}
.auth-form .form-control::placeholder {
  color: #b3c2d6;
  opacity: 1;
}

.auth-container {
  width: 100%;
  max-width: 500px;
}

.auth-title {
  color: #333;
  font-weight: 600;
}

.auth-description {
  color: #666;
  margin-bottom: 0;
}

.auth-tabs {
  display: flex;
  border-radius: 0.5rem;
  overflow: hidden;
  border: 2px solid #e9ecef;
}

.auth-tab {
  flex: 1;
  padding: 0.75rem 1rem;
  background-color: #f8f9fa;
  border: none;
  color: #6c757d;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.auth-tab.active {
  background-color: var(--primary-color);
  color: white;
}

.auth-tab:hover:not(.active) {
  background-color: #e9ecef;
}

.form-control {
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  border: 1px solid #dee2e6;
  font-size: 1rem;
}

.form-control:focus {
  border-color: var(--primary-color);
  box-shadow: 0 0 0 0.2rem rgba(var(--primary-color), 0.25);
}

.btn-primary {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  font-weight: 500;
  border-radius: 0.5rem;
}

.demo-credentials {
  border-top: 1px solid #e9ecef;
  padding-top: 1rem;
}

.demo-card {
  background-color: #f8f9fa;
  padding: 1rem;
  border-radius: 0.375rem;
  font-size: 0.875rem;
  margin-bottom: 1rem;
}

@media (max-width: 991px) {
  .brand-title {
    font-size: 2rem;
  }
  
  .auth-forms {
    padding: 1rem;
  }
}
</style>
