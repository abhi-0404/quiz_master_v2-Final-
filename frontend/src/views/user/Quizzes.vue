<template>
  <div class="user-quizzes">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Available Quizzes</h2>
              <p class="text-muted">Choose a quiz to test your knowledge</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="row g-3">
                <div class="col-md-4">
                  <label class="form-label">Subject</label>
                  <select v-model="filters.subject" class="form-select" @change="applyFilters">
                    <option value="">All Subjects</option>
                    <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                      {{ subject.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Difficulty</label>
                  <select v-model="filters.difficulty" class="form-select" @change="applyFilters">
                    <option value="">All Levels</option>
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                  </select>
                </div>
                <div class="col-md-4">
                  <label class="form-label">Search</label>
                  <input 
                    v-model="filters.search" 
                    type="text" 
                    class="form-control" 
                    placeholder="Search quizzes..."
                    @input="debounceSearch"
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <!-- Quiz List -->
      <div v-else class="row g-4">
        <div v-if="filteredQuizzes.length === 0" class="col-12">
          <div class="text-center py-5">
            <i class="fas fa-clipboard-question fa-4x text-muted mb-3"></i>
            <h4 class="text-muted">No quizzes found</h4>
            <p class="text-muted">Try adjusting your filters or check back later.</p>
          </div>
        </div>
        
        <div v-for="quiz in filteredQuizzes" :key="quiz.id" class="col-lg-6 col-xl-4">
          <div class="card quiz-card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h6 class="mb-0 text-truncate">{{ quiz.title }}</h6>
              <span class="badge" :class="getDifficultyBadgeClass(quiz.difficulty)">
                {{ quiz.difficulty || 'Medium' }}
              </span>
            </div>
            <div class="card-body">
              <div class="mb-3">
                <small class="text-muted">
                  <i class="fas fa-book me-1"></i>
                  {{ quiz.subject_name }}
                </small>
              </div>
              
              <p class="card-text text-muted small">{{ quiz.description || 'Test your knowledge with this quiz.' }}</p>
              
              <div class="quiz-info mb-3">
                <div class="d-flex justify-content-between mb-2">
                  <span class="small text-muted">
                    <i class="fas fa-question-circle me-1"></i>
                    {{ quiz.total_questions }} questions
                  </span>
                  <span class="small text-muted">
                    <i class="fas fa-clock me-1"></i>
                    {{ quiz.duration }} min
                  </span>
                </div>
                
                <div v-if="quiz.user_attempts > 0" class="mb-2">
                  <small class="text-muted">
                    <i class="fas fa-redo me-1"></i>
                    Attempted {{ quiz.user_attempts }} time(s)
                  </small>
                  <div v-if="quiz.best_score !== null" class="small text-success">
                    <i class="fas fa-star me-1"></i>
                    Best Score: {{ quiz.best_score }}%
                  </div>
                </div>
              </div>
            </div>
            
            <div class="card-footer bg-transparent">
              <div class="d-grid gap-2">
                <router-link 
                  :to="`/user/quiz/${quiz.id}`" 
                  class="btn btn-primary"
                  :class="{ 'btn-outline-primary': quiz.user_attempts > 0 }"
                >
                  <i class="fas fa-play me-1"></i>
                  {{ quiz.user_attempts > 0 ? 'Retake Quiz' : 'Take Quiz' }}
                </router-link>
                
                <button 
                  v-if="quiz.user_attempts > 0"
                  @click="viewResults(quiz.id)"
                  class="btn btn-sm btn-outline-secondary"
                >
                  <i class="fas fa-chart-line me-1"></i>
                  View Results
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.totalPages > 1" class="row mt-4">
        <div class="col-12">
          <nav aria-label="Quiz pagination">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: pagination.currentPage === 1 }">
                <a class="page-link" href="#" @click.prevent="changePage(pagination.currentPage - 1)">
                  Previous
                </a>
              </li>
              
              <li 
                v-for="page in visiblePages" 
                :key="page" 
                class="page-item" 
                :class="{ active: page === pagination.currentPage }"
              >
                <a class="page-link" href="#" @click.prevent="changePage(page)">
                  {{ page }}
                </a>
              </li>
              
              <li class="page-item" :class="{ disabled: pagination.currentPage === pagination.totalPages }">
                <a class="page-link" href="#" @click.prevent="changePage(pagination.currentPage + 1)">
                  Next
                </a>
              </li>
            </ul>
          </nav>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'UserQuizzes',
  data() {
    return {
      quizzes: [],
      subjects: [],
      loading: true,
      filters: {
        subject: '',
        difficulty: '',
        search: ''
      },
      pagination: {
        currentPage: 1,
        totalPages: 1,
        totalQuizzes: 0,
        perPage: 12
      },
      searchTimeout: null
    }
  },
  computed: {
    filteredQuizzes() {
      return this.quizzes
    },
    visiblePages() {
      const current = this.pagination.currentPage
      const total = this.pagination.totalPages
      const delta = 2
      const range = []
      
      for (let i = Math.max(2, current - delta); 
           i <= Math.min(total - 1, current + delta); 
           i++) {
        range.push(i)
      }
      
      if (current - delta > 2) {
        range.unshift('...')
      }
      if (current + delta < total - 1) {
        range.push('...')
      }
      
      range.unshift(1)
      if (total > 1) range.push(total)
      
      return range.filter((item, index, array) => array.indexOf(item) === index)
    }
  },
  async mounted() {
    await this.loadSubjects()
    await this.loadQuizzes()
  },
  methods: {
    async loadSubjects() {
      try {
        const response = await api.get('/admin/subjects')
        this.subjects = response.data.subjects || []
      } catch (error) {
        console.error('Error loading subjects:', error)
      }
    },
    async loadQuizzes(page = 1) {
      try {
        this.loading = true
        const params = {
          page,
          per_page: this.pagination.perPage,
          subject_id: this.filters.subject || undefined,
          difficulty: this.filters.difficulty || undefined,
          search: this.filters.search || undefined
        }
        
        const response = await api.get('/quiz', { params })
        this.quizzes = response.data.quizzes || []
        
        this.pagination = {
          currentPage: response.data.current_page || 1,
          totalPages: response.data.total_pages || 1,
          totalQuizzes: response.data.total || 0,
          perPage: this.pagination.perPage
        }
      } catch (error) {
        console.error('Error loading quizzes:', error)
        this.$store.dispatch('alerts/addAlert', {
          type: 'error',
          message: 'Failed to load quizzes'
        })
      } finally {
        this.loading = false
      }
    },
    applyFilters() {
      this.pagination.currentPage = 1
      this.loadQuizzes()
    },
    debounceSearch() {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout)
      }
      this.searchTimeout = setTimeout(() => {
        this.applyFilters()
      }, 500)
    },
    changePage(page) {
      if (page >= 1 && page <= this.pagination.totalPages) {
        this.pagination.currentPage = page
        this.loadQuizzes(page)
      }
    },
    getDifficultyBadgeClass(difficulty) {
      const difficultyMap = {
        easy: 'bg-success',
        medium: 'bg-warning text-dark',
        hard: 'bg-danger'
      }
      return difficultyMap[difficulty?.toLowerCase()] || 'bg-secondary'
    },
    viewResults(quizId) {
      this.$router.push(`/user/quiz/${quizId}/results`)
    }
  }
}
</script>

<style scoped>
.user-quizzes {
  padding: 20px 0;
}

.quiz-card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.quiz-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
}

.quiz-info {
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.pagination .page-link {
  color: #007bff;
}

.pagination .page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
}
</style>
