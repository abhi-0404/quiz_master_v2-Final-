<template>
  <div class="quiz-results">
    <div class="container-fluid">
      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading results...</span>
        </div>
        <p class="mt-3 text-muted">Loading your quiz results...</p>
      </div>

      <!-- Results Display -->
      <div v-else-if="score" class="results-container">
        <!-- Header -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="results-header text-center">
              <div class="result-icon mb-3">
                <i class="fas" :class="getResultIcon(score.percentage)" :style="{ color: getResultColor(score.percentage) }"></i>
              </div>
              <h1 class="display-4 mb-2" :style="{ color: getResultColor(score.percentage) }">
                {{ score.percentage }}%
              </h1>
              <h3 class="mb-1">{{ score.quiz_title }}</h3>
              <p class="text-muted mb-3">{{ score.subject_name }}</p>
              <div class="performance-badge">
                <span class="badge" :class="getPerformanceBadgeClass(score.performance_level)">
                  {{ score.performance_level }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <!-- Score Summary Cards -->
        <div class="row g-4 mb-4">
          <div class="col-md-3">
            <div class="summary-card card text-center">
              <div class="card-body">
                <i class="fas fa-check-circle fa-2x text-success mb-3"></i>
                <h4>{{ score.score }}</h4>
                <p class="text-muted mb-0">Correct Answers</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="summary-card card text-center">
              <div class="card-body">
                <i class="fas fa-times-circle fa-2x text-danger mb-3"></i>
                <h4>{{ score.total_questions - score.score }}</h4>
                <p class="text-muted mb-0">Incorrect Answers</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="summary-card card text-center">
              <div class="card-body">
                <i class="fas fa-clock fa-2x text-info mb-3"></i>
                <h4>{{ formatDuration(score.time_spent) }}</h4>
                <p class="text-muted mb-0">Time Spent</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="summary-card card text-center">
              <div class="card-body">
                <i class="fas fa-calendar fa-2x text-warning mb-3"></i>
                <h4>{{ formatDate(score.timestamp_of_attempt) }}</h4>
                <p class="text-muted mb-0">Completed On</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Detailed Results -->
        <div class="row mb-4">
          <div class="col-12">
            <div class="card">
              <div class="card-header d-flex justify-content-between align-items-center">
                <h5 class="mb-0">Detailed Results</h5>
                <div>
                  <button 
                    @click="toggleShowCorrectAnswers"
                    class="btn btn-sm btn-outline-primary me-2"
                  >
                    {{ showCorrectAnswers ? 'Hide' : 'Show' }} Correct Answers
                  </button>
                  <button @click="printResults" class="btn btn-sm btn-outline-secondary">
                    <i class="fas fa-print me-1"></i>
                    Print
                  </button>
                </div>
              </div>
              <div class="card-body">
                <div class="questions-review">
                  <div 
                    v-for="(question, index) in detailedResults"
                    :key="question.id"
                    class="question-review mb-4"
                  >
                    <div class="question-header d-flex align-items-start mb-3">
                      <div class="question-number me-3">
                        <span class="badge" :class="question.is_correct ? 'bg-success' : 'bg-danger'">
                          {{ index + 1 }}
                        </span>
                      </div>
                      <div class="question-content flex-grow-1">
                        <h6 class="mb-2">{{ question.question_text }}</h6>
                        <div class="result-indicator">
                          <i class="fas" :class="question.is_correct ? 'fa-check-circle text-success' : 'fa-times-circle text-danger'"></i>
                          <span class="ms-2" :class="question.is_correct ? 'text-success' : 'text-danger'">
                            {{ question.is_correct ? 'Correct' : 'Incorrect' }}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div class="answers-section">
                      <div 
                        v-for="option in question.options"
                        :key="option.id"
                        class="answer-option mb-2"
                        :class="getOptionClass(question, option)"
                      >
                        <div class="d-flex align-items-center">
                          <div class="option-indicator me-3">
                            <i class="fas" :class="getOptionIcon(question, option)"></i>
                          </div>
                          <div class="option-text">
                            {{ option.option_text }}
                          </div>
                          <div class="ms-auto">
                            <span v-if="option.id === question.user_answer" class="badge bg-primary">Your Answer</span>
                            <span v-if="showCorrectAnswers && option.is_correct" class="badge bg-success">Correct</span>
                          </div>
                        </div>
                      </div>
                    </div>

                    <!-- Explanation (if available) -->
                    <div v-if="showCorrectAnswers && question.explanation" class="explanation mt-3 p-3 bg-light rounded">
                      <h6 class="mb-2">
                        <i class="fas fa-lightbulb text-warning me-2"></i>
                        Explanation
                      </h6>
                      <p class="mb-0">{{ question.explanation }}</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Action Buttons -->
        <div class="row">
          <div class="col-12 text-center">
            <div class="action-buttons">
              <router-link to="/user/quizzes" class="btn btn-primary me-3">
                <i class="fas fa-list me-2"></i>
                Back to Quizzes
              </router-link>
              <router-link :to="`/user/quiz/${$route.params.id}`" class="btn btn-outline-success me-3">
                <i class="fas fa-redo me-2"></i>
                Retake Quiz
              </router-link>
              <router-link to="/user/scores" class="btn btn-outline-info">
                <i class="fas fa-chart-line me-2"></i>
                View All Results
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div v-else class="text-center py-5">
        <i class="fas fa-exclamation-triangle fa-4x text-danger mb-3"></i>
        <h4>Results not found</h4>
        <p class="text-muted">Unable to load quiz results. Please try again.</p>
        <router-link to="/user/quizzes" class="btn btn-primary">
          Back to Quizzes
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/services/api'

export default {
  name: 'QuizResults',
  data() {
    return {
      score: null,
      detailedResults: [],
      loading: true,
      showCorrectAnswers: false
    }
  },
  async mounted() {
    await this.loadResults()
  },
  methods: {
    async loadResults() {
      try {
        const quizId = this.$route.params.id
        const scoreId = this.$route.query.scoreId
        
        let response
        if (scoreId) {
          // Load specific attempt results
          response = await api.get(`/user/quiz/${quizId}/results/${scoreId}`)
        } else {
          // Load latest attempt results
          response = await api.get(`/user/quiz/${quizId}/results`)
        }
        
        this.score = response.data.score
        this.detailedResults = response.data.detailed_results || []
        
      } catch (error) {
        console.error('Error loading results:', error)
        this.$store.dispatch('alerts/addAlert', {
          type: 'error',
          message: 'Failed to load quiz results'
        })
      } finally {
        this.loading = false
      }
    },
    getResultIcon(percentage) {
      if (percentage >= 90) return 'fa-trophy fa-4x'
      if (percentage >= 80) return 'fa-medal fa-4x'
      if (percentage >= 70) return 'fa-thumbs-up fa-4x'
      if (percentage >= 60) return 'fa-check-circle fa-4x'
      return 'fa-times-circle fa-4x'
    },
    getResultColor(percentage) {
      if (percentage >= 90) return '#ffc107'
      if (percentage >= 80) return '#28a745'
      if (percentage >= 70) return '#17a2b8'
      if (percentage >= 60) return '#fd7e14'
      return '#dc3545'
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
    getOptionClass(question, option) {
      const classes = ['answer-option-item', 'p-3', 'border', 'rounded']
      
      if (option.id === question.user_answer && option.is_correct) {
        classes.push('border-success', 'bg-success', 'bg-opacity-10')
      } else if (option.id === question.user_answer && !option.is_correct) {
        classes.push('border-danger', 'bg-danger', 'bg-opacity-10')
      } else if (this.showCorrectAnswers && option.is_correct) {
        classes.push('border-success', 'bg-success', 'bg-opacity-10')
      } else {
        classes.push('border-light')
      }
      
      return classes.join(' ')
    },
    getOptionIcon(question, option) {
      if (option.id === question.user_answer && option.is_correct) {
        return 'fa-check-circle text-success'
      } else if (option.id === question.user_answer && !option.is_correct) {
        return 'fa-times-circle text-danger'
      } else if (this.showCorrectAnswers && option.is_correct) {
        return 'fa-check-circle text-success'
      } else {
        return 'fa-circle text-muted'
      }
    },
    toggleShowCorrectAnswers() {
      this.showCorrectAnswers = !this.showCorrectAnswers
    },
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString()
    },
    formatDuration(seconds) {
      if (!seconds) return 'N/A'
      
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      
      if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`
      } else if (minutes > 0) {
        return `${minutes}m ${secs}s`
      } else {
        return `${secs}s`
      }
    },
    printResults() {
      window.print()
    }
  }
}
</script>

<style scoped>
.quiz-results {
  padding: 20px 0;
}

.results-header {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 3rem 2rem;
  border-radius: 15px;
  margin-bottom: 2rem;
}

.result-icon {
  margin-bottom: 1rem;
}

.performance-badge .badge {
  font-size: 1rem;
  padding: 0.5rem 1rem;
}

.summary-card {
  border: none;
  box-shadow: 0 2px 15px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.summary-card:hover {
  transform: translateY(-2px);
}

.question-review {
  border-bottom: 1px solid #e9ecef;
  padding-bottom: 1.5rem;
}

.question-review:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.question-number .badge {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: bold;
}

.answer-option-item {
  transition: all 0.2s ease;
}

.explanation {
  border-left: 4px solid #ffc107;
}

.action-buttons {
  margin: 2rem 0;
}

.card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.card-header {
  background-color: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

/* Print styles */
@media print {
  .card-header button,
  .action-buttons {
    display: none !important;
  }
  
  .quiz-results {
    padding: 0;
  }
  
  .summary-card {
    box-shadow: none;
    border: 1px solid #dee2e6;
  }
}

@media (max-width: 768px) {
  .results-header {
    padding: 2rem 1rem;
  }
  
  .action-buttons .btn {
    display: block;
    width: 100%;
    margin-bottom: 0.5rem;
    margin-right: 0 !important;
  }
  
  .question-number {
    margin-bottom: 1rem;
  }
  
  .question-header {
    flex-direction: column;
  }
  
  .card-header .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
