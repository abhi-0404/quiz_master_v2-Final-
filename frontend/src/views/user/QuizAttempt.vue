<template>
  <div class="quiz-attempt">
    <div class="container-fluid" v-if="!loading && quiz">
      <!-- Quiz Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="quiz-header bg-primary text-white p-4 rounded">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <h2 class="mb-1">{{ quiz.title }}</h2>
                <p class="mb-2 opacity-75">{{ quiz.subject_name }}</p>
                <p class="mb-0 small opacity-75">{{ quiz.description }}</p>
              </div>
              <div class="text-end">
                <div class="quiz-timer" :class="{ 'text-warning': timeWarning, 'text-danger': timeCritical }">
                  <i class="fas fa-clock me-2"></i>
                  <span class="h4 mb-0">{{ formatTime(timeRemaining) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Quiz Progress -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center mb-3">
                <h6 class="mb-0">Question {{ currentQuestionIndex + 1 }} of {{ quiz.questions.length }}</h6>
                <div class="quiz-progress-info">
                  <span class="badge bg-secondary me-2">{{ answeredQuestions }} answered</span>
                  <span class="badge bg-info">{{ quiz.questions.length - answeredQuestions }} remaining</span>
                </div>
              </div>
              <div class="progress" style="height: 8px;">
                <div 
                  class="progress-bar" 
                  :style="{ width: progressPercentage + '%' }"
                  role="progressbar"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Current Question -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card question-card">
            <div class="card-header">
              <h5 class="mb-0">
                <span class="question-number">Q{{ currentQuestionIndex + 1 }}.</span>
                {{ currentQuestion.question_text }}
              </h5>
            </div>
            <div class="card-body">
              <div class="options-container">
                <div 
                  v-for="option in currentQuestion.options" 
                  :key="option.id"
                  class="option-item mb-3"
                >
                  <div class="form-check">
                    <input
                      :id="`option-${option.id}`"
                      v-model="userAnswers[currentQuestion.id]"
                      :value="option.id"
                      type="radio"
                      class="form-check-input"
                      :name="`question-${currentQuestion.id}`"
                    >
                    <label 
                      :for="`option-${option.id}`" 
                      class="form-check-label w-100"
                    >
                      <div class="option-content p-3 border rounded">
                        <div class="d-flex align-items-center">
                          <span class="option-letter me-3">{{ getOptionLetter(option.id) }}</span>
                          <span>{{ option.option_text }}</span>
                        </div>
                      </div>
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div class="d-flex justify-content-between align-items-center">
                <button 
                  @click="previousQuestion"
                  :disabled="currentQuestionIndex === 0"
                  class="btn btn-outline-secondary"
                >
                  <i class="fas fa-chevron-left me-2"></i>
                  Previous
                </button>

                <div class="question-navigation">
                  <span class="me-3">Jump to question:</span>
                  <button
                    v-for="(question, index) in quiz.questions"
                    :key="question.id"
                    @click="goToQuestion(index)"
                    class="btn btn-sm me-1 mb-1"
                    :class="getQuestionButtonClass(index)"
                  >
                    {{ index + 1 }}
                  </button>
                </div>

                <div>
                  <button 
                    v-if="currentQuestionIndex < quiz.questions.length - 1"
                    @click="nextQuestion"
                    class="btn btn-primary me-2"
                  >
                    Next
                    <i class="fas fa-chevron-right ms-2"></i>
                  </button>
                  
                  <button 
                    @click="showSubmitModal"
                    class="btn btn-success"
                    :disabled="answeredQuestions === 0"
                  >
                    <i class="fas fa-check me-2"></i>
                    Submit Quiz
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-else-if="loading" class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading quiz...</span>
      </div>
      <p class="mt-3 text-muted">Loading quiz...</p>
    </div>

    <!-- Error State -->
    <div v-else class="text-center py-5">
      <i class="fas fa-exclamation-triangle fa-4x text-danger mb-3"></i>
      <h4>Quiz not found</h4>
      <p class="text-muted">The quiz you're looking for doesn't exist or has been removed.</p>
      <router-link to="/user/quizzes" class="btn btn-primary">
        Back to Quizzes
      </router-link>
    </div>

    <!-- Submit Confirmation Modal -->
    <div class="modal fade" id="submitModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Submit Quiz</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <h6>Quiz Summary</h6>
              <ul class="list-unstyled">
                <li><strong>Total Questions:</strong> {{ quiz?.questions?.length }}</li>
                <li><strong>Answered Questions:</strong> {{ answeredQuestions }}</li>
                <li><strong>Unanswered Questions:</strong> {{ (quiz?.questions?.length || 0) - answeredQuestions }}</li>
                <li><strong>Time Remaining:</strong> {{ formatTime(timeRemaining) }}</li>
              </ul>
            </div>
            
            <div v-if="answeredQuestions < (quiz?.questions?.length || 0)" class="alert alert-warning">
              <i class="fas fa-exclamation-triangle me-2"></i>
              You have {{ (quiz?.questions?.length || 0) - answeredQuestions }} unanswered questions. 
              These will be marked as incorrect.
            </div>

            <p>Are you sure you want to submit your quiz? This action cannot be undone.</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button 
              type="button" 
              class="btn btn-success" 
              @click="submitQuiz"
              :disabled="submitting"
            >
              <span v-if="submitting" class="spinner-border spinner-border-sm me-2" role="status"></span>
              {{ submitting ? 'Submitting...' : 'Submit Quiz' }}
            </button>
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
  name: 'QuizAttempt',
  data() {
    return {
      quiz: null,
      loading: true,
      submitting: false,
      currentQuestionIndex: 0,
      userAnswers: {},
      startTime: null,
      timeRemaining: 0,
      timer: null,
      submitModal: null
    }
  },
  computed: {
    currentQuestion() {
      return this.quiz?.questions?.[this.currentQuestionIndex]
    },
    answeredQuestions() {
      return Object.keys(this.userAnswers).length
    },
    progressPercentage() {
      if (!this.quiz?.questions?.length) return 0
      return (this.answeredQuestions / this.quiz.questions.length) * 100
    },
    timeWarning() {
      return this.timeRemaining <= 300 && this.timeRemaining > 60 // 5 minutes
    },
    timeCritical() {
      return this.timeRemaining <= 60 // 1 minute
    }
  },
  async mounted() {
    this.submitModal = new Modal(document.getElementById('submitModal'))
    await this.loadQuiz()
    this.startTimer()
    
    // Warn user before leaving
    window.addEventListener('beforeunload', this.handleBeforeUnload)
  },
  beforeUnmount() {
    this.clearTimer()
    window.removeEventListener('beforeunload', this.handleBeforeUnload)
  },
  methods: {
    async loadQuiz() {
      try {
        const quizId = this.$route.params.id
        const response = await api.get(`/quiz/${quizId}/start`)
        this.quiz = response.data.quiz
        this.startTime = new Date()
        this.timeRemaining = this.quiz.duration * 60 // Convert minutes to seconds
      } catch (error) {
        console.error('Error loading quiz:', error)
        this.$store.dispatch('alerts/addAlert', {
          type: 'error',
          message: 'Failed to load quiz'
        })
      } finally {
        this.loading = false
      }
    },
    startTimer() {
      this.timer = setInterval(() => {
        this.timeRemaining--
        if (this.timeRemaining <= 0) {
          this.timeUp()
        }
      }, 1000)
    },
    clearTimer() {
      if (this.timer) {
        clearInterval(this.timer)
        this.timer = null
      }
    },
    timeUp() {
      this.clearTimer()
      this.$store.dispatch('alerts/addAlert', {
        type: 'warning',
        message: 'Time is up! Submitting your quiz automatically.'
      })
      this.submitQuiz()
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.quiz.questions.length - 1) {
        this.currentQuestionIndex++
      }
    },
    previousQuestion() {
      if (this.currentQuestionIndex > 0) {
        this.currentQuestionIndex--
      }
    },
    goToQuestion(index) {
      this.currentQuestionIndex = index
    },
    getQuestionButtonClass(index) {
      const questionId = this.quiz.questions[index].id
      const isAnswered = this.userAnswers[questionId] !== undefined
      const isCurrent = index === this.currentQuestionIndex
      
      if (isCurrent) {
        return 'btn-primary'
      } else if (isAnswered) {
        return 'btn-success'
      } else {
        return 'btn-outline-secondary'
      }
    },
    getOptionLetter(optionId) {
      const letters = ['A', 'B', 'C', 'D', 'E', 'F']
      const index = this.currentQuestion.options.findIndex(opt => opt.id === optionId)
      return letters[index] || '?'
    },
    formatTime(seconds) {
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = seconds % 60
      
      if (hours > 0) {
        return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      } else {
        return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      }
    },
    showSubmitModal() {
      this.submitModal.show()
    },
    async submitQuiz() {
      try {
        this.submitting = true
        this.clearTimer()
        
        const quizId = this.$route.params.id
        const timeSpent = Math.floor((new Date() - this.startTime) / 1000)
        
        const response = await api.post(`/quiz/${quizId}/submit`, {
          answers: this.userAnswers,
          time_spent: timeSpent
        })
        
        this.submitModal.hide()
        
        // Redirect to results page
        this.$router.push(`/user/quiz/${quizId}/results?scoreId=${response.data.score_id}`)
        
      } catch (error) {
        console.error('Error submitting quiz:', error)
        this.$store.dispatch('alerts/addAlert', {
          type: 'error',
          message: 'Failed to submit quiz. Please try again.'
        })
      } finally {
        this.submitting = false
      }
    },
    handleBeforeUnload(event) {
      if (this.quiz && this.answeredQuestions > 0) {
        event.preventDefault()
        event.returnValue = ''
        return ''
      }
    }
  }
}
</script>

<style scoped>
.quiz-attempt {
  padding: 20px 0;
  min-height: 100vh;
}

.quiz-header {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
}

.quiz-timer {
  font-family: 'Courier New', monospace;
  font-weight: bold;
}

.question-card {
  border: none;
  box-shadow: 0 2px 15px rgba(0,0,0,0.1);
}

.question-number {
  color: #007bff;
  font-weight: bold;
}

.option-item .form-check-input:checked + .form-check-label .option-content {
  background-color: #e3f2fd;
  border-color: #007bff;
}

.option-content {
  transition: all 0.2s ease;
  cursor: pointer;
}

.option-content:hover {
  background-color: #f8f9fa;
  border-color: #007bff !important;
}

.option-letter {
  background-color: #007bff;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.9rem;
}

.form-check-input:checked + .form-check-label .option-letter {
  background-color: #28a745;
}

.question-navigation .btn {
  min-width: 40px;
}

.progress {
  border-radius: 10px;
}

.progress-bar {
  border-radius: 10px;
  transition: width 0.3s ease;
}

.card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.text-warning {
  color: #ffc107 !important;
}

.text-danger {
  color: #dc3545 !important;
}

@media (max-width: 768px) {
  .quiz-header .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
  
  .quiz-header .text-end {
    text-align: center !important;
  }
  
  .question-navigation {
    text-align: center;
    margin: 1rem 0;
  }
  
  .card-body .d-flex {
    flex-direction: column;
    gap: 1rem;
  }
}
</style>
