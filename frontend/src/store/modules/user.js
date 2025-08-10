import { userAPI } from '../../services/api'

export default {
  namespaced: true,
  
  state: {
    dashboard: null,
    quizzes: [],
    subjects: [],
    scores: [],
    scoresPagination: null
  },
  
  getters: {
    dashboard: state => state.dashboard,
    quizzes: state => state.quizzes,
    subjects: state => state.subjects,
    scores: state => state.scores,
    scoresPagination: state => state.scoresPagination
  },
  
  mutations: {
    SET_DASHBOARD(state, dashboard) {
      state.dashboard = dashboard
    },
    
    SET_QUIZZES(state, quizzes) {
      state.quizzes = quizzes
    },
    
    SET_SUBJECTS(state, subjects) {
      state.subjects = subjects
    },
    
    SET_SCORES(state, { scores, pagination }) {
      state.scores = scores
      state.scoresPagination = pagination
    }
  },
  
  actions: {
    async fetchDashboard({ commit, dispatch }) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const response = await userAPI.getDashboard()
        commit('SET_DASHBOARD', response.data)
        
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load dashboard data'
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    },
    
    async fetchQuizzes({ commit, dispatch }) {
      try {
        const response = await userAPI.getQuizzes()
        commit('SET_QUIZZES', response.data)
        
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load quizzes'
        }, { root: true })
        throw error
      }
    },
    
    async fetchSubjects({ commit, dispatch }) {
      try {
        const response = await userAPI.getSubjects()
        commit('SET_SUBJECTS', response.data)
        
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load subjects'
        }, { root: true })
        throw error
      }
    },
    
    async fetchScores({ commit, dispatch }, params = {}) {
      try {
        const response = await userAPI.getScores(params)
        commit('SET_SCORES', response.data)
        
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load scores'
        }, { root: true })
        throw error
      }
    },
    
    async updateProfile({ dispatch }, profileData) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const response = await userAPI.updateProfile(profileData)
        
        // Update user in auth store
        dispatch('auth/verifyToken', null, { root: true })
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Profile updated successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to update profile'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    }
  }
}
