<template>
  <div class="user-dashboard">
    <div class="container-fluid">
      <!-- Header Section -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-card bg-primary text-white p-4 rounded">
            <h2 class="mb-0">Welcome back, {{ user?.full_name }}!</h2>
            <p class="mb-0 opacity-75">Ready to challenge yourself with some quizzes?</p>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row g-4 mb-4">
        <div class="col-md-3">
          <div class="stats-card card h-100">
            <div class="card-body text-center">
              <i class="fas fa-clipboard-list fa-2x text-primary mb-3"></i>
              <h4 class="card-title">{{ stats.totalQuizzes }}</h4>
              <p class="card-text text-muted">Total Quizzes</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stats-card card h-100">
            <div class="card-body text-center">
              <i class="fas fa-check-circle fa-2x text-success mb-3"></i>
              <h4 class="card-title">{{ stats.completedQuizzes }}</h4>
              <p class="card-text text-muted">Completed</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stats-card card h-100">
            <div class="card-body text-center">
              <i class="fas fa-star fa-2x text-warning mb-3"></i>
              <h4 class="card-title">{{ stats.averageScore }}%</h4>
              <p class="card-text text-muted">Average Score</p>
            </div>
          </div>
        </div>
        <div class="col-md-3">
          <div class="stats-card card h-100">
            <div class="card-body text-center">
              <i class="fas fa-trophy fa-2x text-gold mb-3"></i>
              <h4 class="card-title">{{ stats.bestScore }}%</h4>
              <p class="card-text text-muted">Best Score</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activities & Available Quizzes -->
      <div class="row g-4">
        <!-- Recent Quiz Attempts -->
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Recent Quiz Attempts</h5>
              <router-link to="/user/scores" class="btn btn-sm btn-outline-primary">
                View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="recentAttempts.length === 0" class="text-center text-muted py-4">
                <i class="fas fa-clipboard-list fa-3x mb-3 opacity-50"></i>
                <p>No recent quiz attempts</p>
                <router-link to="/user/quizzes" class="btn btn-primary">
                  Take Your First Quiz
                </router-link>
              </div>
              <div v-else>
                <div v-for="attempt in recentAttempts" :key="attempt.id" class="attempt-item mb-3 p-3 border rounded">
                  <div class="d-flex justify-content-between align-items-start">
                    <div>
                      <h6 class="mb-1">{{ attempt.quiz_title }}</h6>
                      <p class="text-muted small mb-1">{{ attempt.subject_name }}</p>
                      <small class="text-muted">{{ formatDate(attempt.timestamp_of_attempt) }}</small>
                    </div>
                    <div class="text-end">
                      <span class="badge" :class="getScoreBadgeClass(attempt.percentage)">
                        {{ attempt.percentage }}%
                      </span>
                      <div class="small text-muted mt-1">
                        {{ attempt.score }}/{{ attempt.total_questions }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Available Quizzes -->
        <div class="col-lg-6">
          <div class="card h-100">
            <div class="card-header d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Available Quizzes</h5>
              <router-link to="/user/quizzes" class="btn btn-sm btn-outline-primary">
                View All
              </router-link>
            </div>
            <div class="card-body">
              <div v-if="availableQuizzes.length === 0" class="text-center text-muted py-4">
                <i class="fas fa-clipboard-question fa-3x mb-3 opacity-50"></i>
                <p>No quizzes available</p>
              </div>
              <div v-else>
                <div v-for="quiz in availableQuizzes" :key="quiz.id" class="quiz-item mb-3 p-3 border rounded">
                  <div class="d-flex justify-content-between align-items-start">
                    <div>
                      <h6 class="mb-1">{{ quiz.title }}</h6>
                      <p class="text-muted small mb-1">{{ quiz.subject_name }}</p>
                      <div class="small text-muted">
                        <i class="fas fa-question-circle me-1"></i>
                        {{ quiz.total_questions }} questions
                        <span class="ms-2">
                          <i class="fas fa-clock me-1"></i>
                          {{ quiz.duration }} min
                        </span>
                      </div>
                    </div>
                    <div>
                      <router-link 
                        :to="`/user/quiz/${quiz.id}`" 
                        class="btn btn-sm btn-primary"
                      >
                        Take Quiz
                      </router-link>
                    </div>
                  </div>
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
import { mapState, mapGetters } from 'vuex'
import api from '@/services/api'

export default {
  name: 'UserDashboard',
  data() {
    return {
      stats: {
        totalQuizzes: 0,
        completedQuizzes: 0,
        averageScore: 0,
        bestScore: 0
      },
      recentAttempts: [],
      availableQuizzes: [],
      loading: true
    }
  },
  computed: {
    ...mapState('auth', ['user'])
  },
  async mounted() {
    await this.loadDashboardData()
  },
  methods: {
    async loadDashboardData() {
      try {
        this.loading = true
        
        // Load dashboard stats
        const statsResponse = await api.get('/user/dashboard/stats')
        this.stats = statsResponse.data

        // Load recent attempts
        const attemptsResponse = await api.get('/user/scores?limit=5')
        this.recentAttempts = attemptsResponse.data.scores || []

        // Load available quizzes
        const quizzesResponse = await api.get('/quiz?limit=5')
        this.availableQuizzes = quizzesResponse.data.quizzes || []

      } catch (error) {
        console.error('Error loading dashboard data:', error)
        this.$store.dispatch('alerts/addAlert', {
          type: 'error',
          message: 'Failed to load dashboard data'
        })
      } finally {
        this.loading = false
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    },
    getScoreBadgeClass(percentage) {
      if (percentage >= 90) return 'bg-success'
      if (percentage >= 80) return 'bg-info'
      if (percentage >= 70) return 'bg-primary'
      if (percentage >= 60) return 'bg-warning'
      return 'bg-danger'
    }
  }
}
</script>

<style scoped>
.user-dashboard {
  padding: 20px 0;
}

.welcome-card {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border: none;
}

.stats-card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.stats-card:hover {
  transform: translateY(-2px);
}

.text-gold {
  color: #ffc107;
}

.attempt-item, .quiz-item {
  transition: all 0.2s;
}

.attempt-item:hover, .quiz-item:hover {
  background-color: #f8f9fa;
  border-color: #007bff !important;
}

.card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}
</style>
