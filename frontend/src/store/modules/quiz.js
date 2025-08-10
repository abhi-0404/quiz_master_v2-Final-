import { quizAPI } from '../../services/api'

export default {
  namespaced: true,
  
  state: {
    currentQuiz: null,
    quizQuestions: [],
    quizResults: null,
    quizAttempt: null,
    answers: {},
    startTime: null,
    timeRemaining: 0
  },
  
  getters: {
    currentQuiz: state => state.currentQuiz,
    quizQuestions: state => state.quizQuestions,
    quizResults: state => state.quizResults,
    quizAttempt: state => state.quizAttempt,
    answers: state => state.answers,
    startTime: state => state.startTime,
    timeRemaining: state => state.timeRemaining
  },
  
  mutations: {
    SET_CURRENT_QUIZ(state, quiz) {
      state.currentQuiz = quiz
    },
    
    SET_QUIZ_QUESTIONS(state, questions) {
      state.quizQuestions = questions
    },
    
    SET_QUIZ_RESULTS(state, results) {
      state.quizResults = results
    },
    
    SET_QUIZ_ATTEMPT(state, attempt) {
      state.quizAttempt = attempt
    },
    
    SET_ANSWER(state, { questionId, answer }) {
      state.answers = {
        ...state.answers,
        [questionId]: answer
      }
    },
    
    SET_START_TIME(state, startTime) {
      state.startTime = startTime
    },
    
    SET_TIME_REMAINING(state, time) {
      state.timeRemaining = time
    },
    
    CLEAR_QUIZ_STATE(state) {
      state.currentQuiz = null
      state.quizQuestions = []
      state.quizResults = null
      state.answers = {}
      state.startTime = null
      state.timeRemaining = 0
    }
  },
  
  actions: {
    async fetchQuizDetails({ commit, dispatch }, quizId) {
      try {
        const response = await quizAPI.getQuizDetails(quizId)
        commit('SET_CURRENT_QUIZ', response.data)
        
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load quiz details'
        }, { root: true })
        throw error
      }
    },
    
    async startQuiz({ commit, dispatch }, quizId) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const response = await quizAPI.startQuiz(quizId)
        const { quiz, questions, start_time } = response.data
        
        commit('SET_CURRENT_QUIZ', quiz)
        commit('SET_QUIZ_QUESTIONS', questions)
        commit('SET_START_TIME', start_time)
        commit('SET_TIME_REMAINING', quiz.duration * 60) // Convert minutes to seconds
        
        // Clear any previous answers
        commit('CLEAR_QUIZ_STATE')
        commit('SET_CURRENT_QUIZ', quiz)
        commit('SET_QUIZ_QUESTIONS', questions)
        commit('SET_START_TIME', start_time)
        commit('SET_TIME_REMAINING', quiz.duration * 60)
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to start quiz'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    },
    
    async submitQuiz({ commit, dispatch, state }, quizId) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const submitData = {
          answers: state.answers,
          start_time: state.startTime
        }
        
        const response = await quizAPI.submitQuiz(quizId, submitData)
        commit('SET_QUIZ_RESULTS', response.data.results)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Quiz submitted successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to submit quiz'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      } finally {
        dispatch('setLoading', false, { root: true })
      }
    },
    
    async fetchQuizAttempt({ commit, dispatch }, scoreId) {
      try {
        const response = await quizAPI.getQuizAttempt(scoreId)
        commit('SET_QUIZ_ATTEMPT', response.data)
        
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load quiz attempt details'
        }, { root: true })
        throw error
      }
    },
    
    setAnswer({ commit }, { questionId, answer }) {
      commit('SET_ANSWER', { questionId, answer })
    },
    
    updateTimeRemaining({ commit }, time) {
      commit('SET_TIME_REMAINING', time)
    },
    
    clearQuizState({ commit }) {
      commit('CLEAR_QUIZ_STATE')
    }
  }
}
