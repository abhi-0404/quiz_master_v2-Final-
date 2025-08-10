import { authAPI } from '../../services/api'

export default {
  namespaced: true,
  
  state: {
    token: localStorage.getItem('token') || null,
    user: null,
    isAuthenticated: false
  },
  
  getters: {
    isAuthenticated: state => state.isAuthenticated,
    currentUser: state => state.user,
    userRole: state => state.user?.role || null,
    token: state => state.token
  },
  
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      if (token) {
        localStorage.setItem('token', token)
      } else {
        localStorage.removeItem('token')
      }
    },
    
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    },
    
    CLEAR_AUTH(state) {
      state.token = null
      state.user = null
      state.isAuthenticated = false
      localStorage.removeItem('token')
    }
  },
  
  actions: {
    async login({ commit, dispatch }, credentials) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const response = await authAPI.login(credentials)
        const { access_token, user } = response.data
        
        commit('SET_TOKEN', access_token)
        commit('SET_USER', user)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Login successful!'
        }, { root: true })
        
        return { success: true, user }
      } catch (error) {
        // --- FIX: Display the specific error message from the backend ---
        // This will show "Invalid credentials" instead of "Login failed".
        const message = error.response?.data?.error || 'An unknown login error occurred.'
        
        dispatch('showAlert', {
          type: 'error',
          message: message
        }, { root: true })
        
        // Return a failure object so the component knows not to redirect
        return { success: false, error: message }
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    },
    
    async register({ dispatch }, userData) {
      try {
        dispatch('setLoading', true, { root: true })
        
        await authAPI.register(userData)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Registration successful! Please login.'
        }, { root: true })
        
        return { success: true }
      } catch (error) {
        const message = error.response?.data?.error || 'Registration failed'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    },
    
    async verifyToken({ commit }) {
      try {
        const response = await authAPI.verifyToken()
        const { user } = response.data
        
        commit('SET_USER', user)
        return { success: true, user }
      } catch (error) {
        commit('CLEAR_AUTH')
        return { success: false }
      }
    },
    
    async logout({ commit, dispatch }) {
      try {
        await authAPI.logout()
      } catch (error) {
        console.error('Logout API error:', error)
      } finally {
        commit('CLEAR_AUTH')
        dispatch('showAlert', {
          type: 'success',
          message: 'Logged out successfully!'
        }, { root: true })
      }
    }
  }
}
