import { createStore } from 'vuex'
import auth from './modules/auth'
import quiz from './modules/quiz'
import admin from './modules/admin'
import user from './modules/user'

export default createStore({
  state: {
    loading: false,
    alert: {
      show: false,
      type: 'info',
      message: ''
    }
  },
  
  getters: {
    isLoading: state => state.loading,
    alert: state => state.alert,
    isAuthenticated: (state, getters) => getters['auth/isAuthenticated'],
    currentUser: (state, getters) => getters['auth/currentUser'],
    userRole: (state, getters) => getters['auth/userRole']
  },
  
  mutations: {
    SET_LOADING(state, loading) {
      state.loading = loading
    },
    
    SET_ALERT(state, { type, message }) {
      state.alert = {
        show: true,
        type,
        message
      }
    },
    
    CLEAR_ALERT(state) {
      state.alert = {
        show: false,
        type: 'info',
        message: ''
      }
    }
  },
  
  actions: {
    setLoading({ commit }, loading) {
      commit('SET_LOADING', loading)
    },
    
    showAlert({ commit }, { type = 'info', message }) {
      commit('SET_ALERT', { type, message })
      
      // Auto-hide alert after 5 seconds
      setTimeout(() => {
        commit('CLEAR_ALERT')
      }, 5000)
    },
    
    clearAlert({ commit }) {
      commit('CLEAR_ALERT')
    }
  },
  
  modules: {
    auth,
    quiz,
    admin,
    user
  }
})
