<template>
  <div class="user-scores">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-card bg-primary text-white p-4 rounded d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-0">My Quiz Scores</h2>
              <p class="mb-0 opacity-75">Track your quiz performance and progress</p>
            </div>
            <div>
              <button @click="exportResults" class="btn btn-outline-light">
                <i class="fas fa-download me-2"></i>
                Export Results
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Summary Stats -->
      <div class="row g-3 g-lg-4 mb-4">
        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-primary-subtle text-primary-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2 fw-bold">{{ summary.totalAttempts }}</h3>
                <p class="mb-0 fw-bold">Attempted Quiz</p>
              </div>
              <i class="fas fa-clipboard-check fa-3x opacity-50" style="color: #0d6efd;"></i>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-info-subtle text-info-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2 fw-bold">{{ summary.averageTime }} min</h3>
                <p class="mb-0 fw-bold">Average Time</p>
              </div>
              <i class="fas fa-clock fa-3x opacity-50" style="color: #0dcaf0;"></i>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-success-subtle text-success-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2 fw-bold">{{ summary.averageScore }}%</h3>
                <p class="mb-0 fw-bold">Average Score</p>
              </div>
              <i class="fas fa-chart-line fa-3x opacity-50" style="color: #198754;"></i>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-warning-subtle text-warning-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2 fw-bold">{{ summary.bestScore }}%</h3>
                <p class="mb-0 fw-bold">Best Score</p>
              </div>
              <i class="fas fa-trophy fa-3x opacity-50" style="color: #ffc107;"></i>
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
                <div class="col-md-3">
                  <label class="form-label">Subject</label>
                  <select v-model="filters.subject" class="form-select" @change="applyFilters">
                    <option value="">All Subjects</option>
                    <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                      {{ subject.name }}
                    </option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Quiz</label>
                  <select v-model="filters.quiz" class="form-select" @change="applyFilters">
                    <option value="">All Quizzes</option>
                    <option v-for="quiz in quizzes" :key="quiz.id" :value="quiz.id">
                      {{ quiz.title }}
                    </option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Date Range</label>
                  <select v-model="filters.dateRange" class="form-select" @change="applyFilters">
                    <option value="">All Time</option>
                    <option value="today">Today</option>
                    <option value="week">This Week</option>
                    <option value="month">This Month</option>
                  </select>
                </div>
                <div class="col-md-3">
                  <label class="form-label">Sort By</label>
                  <select v-model="filters.sortBy" class="form-select" @change="applyFilters">
                    <option value="date_desc">Latest First</option>
                    <option value="date_asc">Oldest First</option>
                    <option value="score_desc">Highest Score</option>
                    <option value="score_asc">Lowest Score</option>
                  </select>
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

      <!-- Scores List -->
      <div v-else class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-header">
              <h5 class="mb-0">Quiz Attempts</h5>
            </div>
            <div class="card-body p-0">
              <div v-if="scores.length === 0" class="text-center py-5">
                <i class="fas fa-clipboard-list fa-4x text-muted mb-3"></i>
                <h4 class="text-muted">No quiz attempts found</h4>
                <p class="text-muted">Start taking quizzes to see your scores here.</p>
                <router-link to="/user/quizzes" class="btn btn-primary">
                  Take a Quiz
                </router-link>
              </div>
              
              <div v-else class="table-responsive">
                <table class="table table-hover mb-0">
                  <thead class="table-light">
                    <tr>
                      <th>Quiz</th>
                      <th>Subject</th>
                      <th>Score</th>
                      <th>Percentage</th>
                      <th>Performance</th>
                      <th>Date</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="score in scores" :key="score.id">
                      <td>
                        <div>
                          <strong>{{ score.quiz_title }}</strong>
                          <div class="small text-muted">
                            {{ score.total_questions }} questions
                          </div>
                        </div>
                      </td>
                      <td>
                        <span class="badge bg-secondary">{{ score.subject_name }}</span>
                      </td>
                      <td>
                        <strong>{{ score.score }}/{{ score.total_questions }}</strong>
                      </td>
                      <td>
                        <span class="badge" :class="getScoreBadgeClass(score.percentage)">
                          {{ score.percentage }}%
                        </span>
                      </td>
                      <td>
                        <span class="badge" :class="getPerformanceBadgeClass(score.performance_level)">
                          {{ score.performance_level }}
                        </span>
                      </td>
                      <td>
                        <div>
                          {{ formatDate(score.timestamp_of_attempt) }}
                          <div class="small text-muted">
                            {{ formatTime(score.timestamp_of_attempt) }}
                          </div>
                        </div>
                      </td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button 
                            @click="viewDetails(score)"
                            class="btn btn-outline-primary"
                            title="View Details"
                          >
                            <i class="fas fa-eye"></i>
                          </button>
                          <router-link 
                            :to="`/user/quiz/${score.quiz_id}`"
                            class="btn btn-outline-success"
                            title="Retake Quiz"
                          >
                            <i class="fas fa-redo"></i>
                          </router-link>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.totalPages > 1" class="row mt-4">
        <div class="col-12">
          <nav aria-label="Scores pagination">
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

    <!-- Score Details Modal -->
    <div class="modal fade" id="scoreDetailsModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Quiz Results Details</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body" v-if="selectedScore">
            <div class="row g-4">
              <div class="col-md-6">
                <h6>Quiz Information</h6>
                <ul class="list-unstyled">
                  <li><strong>Quiz:</strong> {{ selectedScore.quiz_title }}</li>
                  <li><strong>Subject:</strong> {{ selectedScore.subject_name }}</li>
                  <li><strong>Total Questions:</strong> {{ selectedScore.total_questions }}</li>
                  <li><strong>Date Taken:</strong> {{ formatDate(selectedScore.timestamp_of_attempt) }}</li>
                </ul>
              </div>
              <div class="col-md-6">
                <h6>Performance</h6>
                <ul class="list-unstyled">
                  <li><strong>Score:</strong> {{ selectedScore.score }}/{{ selectedScore.total_questions }}</li>
                  <li><strong>Percentage:</strong> {{ selectedScore.percentage }}%</li>
                  <li><strong>Performance Level:</strong> {{ selectedScore.performance_level }}</li>
                </ul>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <router-link 
              v-if="selectedScore"
              :to="`/user/quiz/${selectedScore.quiz_id}`"
              class="btn btn-primary"
              data-bs-dismiss="modal"
            >
              Retake Quiz
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap'
import api from '@/services/api'

export default {
  name: 'UserScores',
  data() {
    return {
      scores: [],
      subjects: [],
      quizzes: [],
      summary: {
        totalAttempts: 0,
        averageScore: 0,
        bestScore: 0,
        completedQuizzes: 0
      },
      loading: true,
      filters: {
        subject: '',
        quiz: '',
        dateRange: '',
        sortBy: 'date_desc'
      },
      pagination: {
        currentPage: 1,
        totalPages: 1,
        totalScores: 0,
        perPage: 15
      },
      selectedScore: null,
      scoreDetailsModal: null
    }
  },
  computed: {
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
    this.scoreDetailsModal = new Modal(document.getElementById('scoreDetailsModal'))
    await this.loadFiltersData()
    await this.loadSummary()
    await this.loadScores()
  },
  methods: {
    async loadFiltersData() {
      try {
        // Load subjects
        const subjectsResponse = await api.get('/admin/subjects')
        this.subjects = subjectsResponse.data.subjects || []
        
        // Load quizzes
        const quizzesResponse = await api.get('/quiz')
        this.quizzes = quizzesResponse.data.quizzes || []
      } catch (error) {
        console.error('Error loading filter data:', error)
      }
    },
    async loadSummary() {
      try {
        const response = await api.get('/user/dashboard/stats')
        this.summary = response.data || this.summary
      } catch (error) {
        console.error('Error loading summary:', error)
      }
    },
    async loadScores(page = 1) {
      try {
        this.loading = true
        const params = {
          page,
          per_page: this.pagination.perPage,
          subject_id: this.filters.subject || undefined,
          quiz_id: this.filters.quiz || undefined,
          date_range: this.filters.dateRange || undefined,
          sort_by: this.filters.sortBy
        }
        
        const response = await api.get('/user/scores', { params })
        this.scores = response.data.scores || []
        
        this.pagination = {
          currentPage: response.data.current_page || 1,
          totalPages: response.data.total_pages || 1,
          totalScores: response.data.total || 0,
          perPage: this.pagination.perPage
        }
      } catch (error) {
        console.error('Error loading scores:', error)
        this.$store.dispatch('alerts/addAlert', {
          type: 'error',
          message: 'Failed to load scores'
        })
      } finally {
        this.loading = false
      }
    },
    applyFilters() {
      this.pagination.currentPage = 1
      this.loadScores()
    },
    changePage(page) {
      if (page >= 1 && page <= this.pagination.totalPages) {
        this.pagination.currentPage = page
        this.loadScores(page)
      }
    },
    getScoreBadgeClass(percentage) {
      if (percentage >= 90) return 'bg-success'
      if (percentage >= 80) return 'bg-info'
      if (percentage >= 70) return 'bg-primary'
      if (percentage >= 60) return 'bg-warning'
      return 'bg-danger'
    },
    getPerformanceBadgeClass(level) {
      const levelMap = {
        'Excellent': 'bg-success',
        'Very Good': 'bg-info',
        'Good': 'bg-primary',
        'Average': 'bg-warning',
        'Below Average': 'bg-warning',
        'Poor': 'bg-danger'
      }
      return levelMap[level] || 'bg-secondary'
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    formatTime(dateString) {
      const date = new Date(dateString)
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    viewDetails(score) {
      this.selectedScore = score
      this.scoreDetailsModal.show()
    },
    async exportResults() {
      try {
        const response = await api.get('/user/scores/export', {
          responseType: 'blob',
          params: {
            subject_id: this.filters.subject || undefined,
            quiz_id: this.filters.quiz || undefined,
            date_range: this.filters.dateRange || undefined
          }
        })
        
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', `quiz-results-${new Date().toISOString().split('T')[0]}.csv`)
        document.body.appendChild(link)
        link.click()
        link.remove()
        window.URL.revokeObjectURL(url)
        
        this.$store.dispatch('alerts/addAlert', {
          type: 'success',
          message: 'Results exported successfully'
        })
      } catch (error) {
        console.error('Error exporting results:', error)
        this.$store.dispatch('alerts/addAlert', {
          type: 'error',
          message: 'Failed to export results'
        })
      }
    }
  }
}
</script>

<style scoped>
.user-scores {
  padding: 20px 0;
}

.stat-card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.table th {
  border-top: none;
  font-weight: 600;
  color: #495057;
}

.table-hover tbody tr:hover {
  background-color: #f8f9fa;
}

.btn-group-sm .btn {
  padding: 0.25rem 0.5rem;
}

.pagination .page-link {
  color: #007bff;
}

.pagination .page-item.active .page-link {
  background-color: #007bff;
  border-color: #007bff;
}
</style>
