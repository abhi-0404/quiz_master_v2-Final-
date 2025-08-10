import { adminAPI } from '../../services/api'

export default {
  namespaced: true,
  
  state: {
    dashboard: null,
    subjects: [],
    chapters: [],
    quizzes: [],
    questions: [],
    users: []
  },
  
  getters: {
    dashboard: state => state.dashboard,
    subjects: state => state.subjects,
    chapters: state => state.chapters,
    quizzes: state => state.quizzes,
    questions: state => state.questions,
    users: state => state.users
  },
  
  mutations: {
    SET_DASHBOARD(state, dashboard) {
      state.dashboard = dashboard
    },
    
    SET_SUBJECTS(state, subjects) {
      state.subjects = subjects
    },
    
    SET_CHAPTERS(state, chapters) {
      state.chapters = chapters
    },
    
    SET_QUIZZES(state, quizzes) {
      state.quizzes = quizzes
    },
    
    SET_QUESTIONS(state, questions) {
      state.questions = questions
    },
    
    SET_USERS(state, users) {
      state.users = users
    },
    
    ADD_SUBJECT(state, subject) {
      state.subjects.push(subject)
    },
    
    UPDATE_SUBJECT(state, updatedSubject) {
      const index = state.subjects.findIndex(s => s.id === updatedSubject.id)
      if (index !== -1) {
        state.subjects.splice(index, 1, updatedSubject)
      }
    },
    
    REMOVE_SUBJECT(state, subjectId) {
      state.subjects = state.subjects.filter(s => s.id !== subjectId)
    },
    
    ADD_CHAPTER(state, chapter) {
      state.chapters.push(chapter)
    },
    
    UPDATE_CHAPTER(state, updatedChapter) {
      const index = state.chapters.findIndex(c => c.id === updatedChapter.id)
      if (index !== -1) {
        state.chapters.splice(index, 1, updatedChapter)
      }
    },
    
    REMOVE_CHAPTER(state, chapterId) {
      state.chapters = state.chapters.filter(c => c.id !== chapterId)
    },
    
    ADD_QUIZ(state, quiz) {
      state.quizzes.push(quiz)
    },
    
    UPDATE_QUIZ(state, updatedQuiz) {
      const index = state.quizzes.findIndex(q => q.id === updatedQuiz.id)
      if (index !== -1) {
        state.quizzes.splice(index, 1, updatedQuiz)
      }
    },
    
    REMOVE_QUIZ(state, quizId) {
      state.quizzes = state.quizzes.filter(q => q.id !== quizId)
    },
    
    ADD_QUESTION(state, question) {
      state.questions.push(question)
    },
    
    UPDATE_QUESTION(state, updatedQuestion) {
      const index = state.questions.findIndex(q => q.id === updatedQuestion.id)
      if (index !== -1) {
        state.questions.splice(index, 1, updatedQuestion)
      }
    },
    
    REMOVE_QUESTION(state, questionId) {
      state.questions = state.questions.filter(q => q.id !== questionId)
    }
  },
  
  actions: {
    async fetchDashboard({ commit, dispatch }) {
      try {
        dispatch('setLoading', true, { root: true })
        
        const response = await adminAPI.getDashboard()
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
    
    // Subject actions
    async fetchSubjects({ commit, dispatch }) {
      try {
        const response = await adminAPI.getSubjects()
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
    
    async createSubject({ commit, dispatch }, subjectData) {
      try {
        const response = await adminAPI.createSubject(subjectData)
        commit('ADD_SUBJECT', response.data.subject)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Subject created successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to create subject'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    async updateSubject({ commit, dispatch }, { id, data }) {
      try {
        const response = await adminAPI.updateSubject(id, data)
        commit('UPDATE_SUBJECT', response.data.subject)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Subject updated successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to update subject'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    async deleteSubject({ commit, dispatch }, subjectId) {
      try {
        await adminAPI.deleteSubject(subjectId)
        commit('REMOVE_SUBJECT', subjectId)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Subject deleted successfully!'
        }, { root: true })
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to delete subject'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    // Chapter actions
    async fetchChapters({ commit, dispatch }) {
      try {
        const response = await adminAPI.getChapters()
        commit('SET_CHAPTERS', response.data)
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load chapters'
        }, { root: true })
        throw error
      }
    },
    
    async createChapter({ commit, dispatch }, chapterData) {
      try {
        const response = await adminAPI.createChapter(chapterData)
        commit('ADD_CHAPTER', response.data.chapter)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Chapter created successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to create chapter'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    async updateChapter({ commit, dispatch }, { id, data }) {
      try {
        const response = await adminAPI.updateChapter(id, data)
        commit('UPDATE_CHAPTER', response.data.chapter)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Chapter updated successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to update chapter'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    async deleteChapter({ commit, dispatch }, chapterId) {
      try {
        await adminAPI.deleteChapter(chapterId)
        commit('REMOVE_CHAPTER', chapterId)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Chapter deleted successfully!'
        }, { root: true })
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to delete chapter'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    // Quiz actions
    async fetchQuizzes({ commit, dispatch }) {
      try {
        const response = await adminAPI.getQuizzes()
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
    
    async createQuiz({ commit, dispatch }, quizData) {
      try {
        const response = await adminAPI.createQuiz(quizData)
        commit('ADD_QUIZ', response.data.quiz)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Quiz created successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to create quiz'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    async updateQuiz({ commit, dispatch }, { id, data }) {
      try {
        const response = await adminAPI.updateQuiz(id, data)
        commit('UPDATE_QUIZ', response.data.quiz)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Quiz updated successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to update quiz'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    async deleteQuiz({ commit, dispatch }, quizId) {
      try {
        await adminAPI.deleteQuiz(quizId)
        commit('REMOVE_QUIZ', quizId)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Quiz deleted successfully!'
        }, { root: true })
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to delete quiz'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    // Question actions
    async fetchQuizQuestions({ commit, dispatch }, quizId) {
      try {
        const response = await adminAPI.getQuizQuestions(quizId)
        commit('SET_QUESTIONS', response.data)
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load questions'
        }, { root: true })
        throw error
      }
    },
    
    async createQuestion({ commit, dispatch }, { quizId, questionData }) {
      try {
        const response = await adminAPI.createQuestion(quizId, questionData)
        commit('ADD_QUESTION', response.data.question)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Question created successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to create question'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    async updateQuestion({ commit, dispatch }, { id, data }) {
      try {
        const response = await adminAPI.updateQuestion(id, data)
        commit('UPDATE_QUESTION', response.data.question)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Question updated successfully!'
        }, { root: true })
        
        return response.data
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to update question'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    async deleteQuestion({ commit, dispatch }, questionId) {
      try {
        await adminAPI.deleteQuestion(questionId)
        commit('REMOVE_QUESTION', questionId)
        
        dispatch('showAlert', {
          type: 'success',
          message: 'Question deleted successfully!'
        }, { root: true })
      } catch (error) {
        const message = error.response?.data?.error || 'Failed to delete question'
        dispatch('showAlert', {
          type: 'error',
          message
        }, { root: true })
        throw error
      }
    },
    
    // Users
    async fetchUsers({ commit, dispatch }) {
      try {
        const response = await adminAPI.getUsers()
        commit('SET_USERS', response.data)
        return response.data
      } catch (error) {
        dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load users'
        }, { root: true })
        throw error
      }
    }
  }
}
