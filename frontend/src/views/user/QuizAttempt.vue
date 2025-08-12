<template>
  <div class="quiz-attempt-fullscreen">
    <div v-if="loading" class="loading-state">
      <div class="spinner-border" role="status"></div>
    </div>

    <div v-else-if="quiz" class="quiz-container">
      <!-- Top Stats Bar -->
      <div class="stats-header">
        <div class="stat-item"><strong>{{ answeredQuestions }}</strong> Answered</div>
        <div class="stat-item"><strong>{{ questions.length - answeredQuestions }}</strong> Unanswered</div>
  <div class="stat-item">{{ (currentQuestion.type || 'Single').charAt(0).toUpperCase() + (currentQuestion.type || 'Single').slice(1).toLowerCase() }} Type</div>
        <div class="stat-item">{{ currentQuestion.marks || 1 }} Marks</div>
        <div class="stat-item">{{ currentQuestion.negative_marks || 0 }} ve marks</div>
        <div class="timer" :class="{ critical: timeRemaining <= 60 }">
          <i class="fas fa-clock me-2"></i>
          <span>{{ formatTime(timeRemaining) }}</span>
        </div>
      </div>

      <!-- Progress Bar -->
      <div class="progress-container">
        <div class="progress-info">
          <span>Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}</span>
        </div>
        <div class="progress mx-3">
          <div class="progress-bar" :style="{ width: progressPercentage + '%' }"></div>
        </div>
        <div class="progress-percentage">
          <span>{{ Math.round(progressPercentage) }}% Complete</span>
        </div>
      </div>

      <!-- Question Box -->
      <div class="question-box" v-if="currentQuestion">
        <p class="question-statement">{{ currentQuestion.question_statement }}</p>
        <div class="options-grid">
          <div
            v-for="(option, index) in currentQuestion.options"
            :key="index"
            class="option-btn"
            :class="{ selected: isSelected(currentQuestion.id, index + 1) }"
            @click="selectAnswer(currentQuestion.id, index + 1, currentQuestion.type)"
          >
            <span :class="[currentQuestion.type === 'Single' ? 'option-circle' : 'option-square', 'option-letter']">
              {{ String.fromCharCode(65 + index) }}
            </span>
            <span class="option-text">{{ option }}</span>
          </div>
        </div>
      </div>

      <!-- Navigation Footer -->
      <div class="navigation-footer">
        <button @click="previousQuestion" :disabled="currentQuestionIndex === 0" class="btn btn-nav">
          <i class="fas fa-chevron-left me-2"></i> Prev
        </button>
        <button @click="showSubmitModal" class="btn btn-submit">Submit</button>
        <button @click="nextQuestion" :disabled="currentQuestionIndex >= questions.length - 1" class="btn btn-nav">
          Next <i class="fas fa-chevron-right ms-2"></i>
        </button>
      </div>
    </div>
    
    <!-- Submit Modal -->
    <div class="modal fade" id="submitModal" tabindex="-1">
       <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content bg-dark text-white">
          <div class="modal-header border-secondary">
            <h5 class="modal-title">Submit Quiz</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
          </div>
          <div class="modal-body">Are you sure you want to submit your answers?</div>
          <div class="modal-footer border-secondary">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-primary" @click="submitQuiz">Submit</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { quizAPI } from '@/services/api';

export default {
  name: 'QuizAttempt',
  data() {
    return {
      quiz: null,
      questions: [],
      loading: true,
      submitting: false,
      currentQuestionIndex: 0,
      userAnswers: {},
      startTime: null,
      timeRemaining: 0,
      timer: null,
      submitModal: null,
    };
  },
  computed: {
    currentQuestion() {
      return this.questions[this.currentQuestionIndex];
    },
    answeredQuestions() {
      return Object.values(this.userAnswers).filter(ans => (Array.isArray(ans) ? ans.length > 0 : ans !== null)).length;
    },
    progressPercentage() {
      if (!this.questions.length) return 0;
      return ((this.currentQuestionIndex + 1) / this.questions.length) * 100;
    }
  },
  methods: {
    async loadQuiz() {
      try {
        const quizId = this.$route.params.id;
        const response = await quizAPI.startQuiz(quizId);
        this.quiz = response.data.quiz;
        this.questions = response.data.questions || [];
        this.startTime = new Date(response.data.start_time);
        this.timeRemaining = this.quiz.duration * 60;
        this.startTimer();
      } catch (error) {
        console.error('Error loading quiz:', error);
      } finally {
        this.loading = false;
      }
    },
    startTimer() {
      this.timer = setInterval(() => {
        if (this.timeRemaining > 0) {
          this.timeRemaining--;
        } else {
          this.submitQuiz();
        }
      }, 1000);
    },
    selectAnswer(questionId, optionIndex, questionType) {
      if (questionType === 'multiple') {
        if (!this.userAnswers[questionId] || !Array.isArray(this.userAnswers[questionId])) {
          this.userAnswers[questionId] = [];
        }
        const answers = this.userAnswers[questionId];
        const index = answers.indexOf(optionIndex);
        if (index > -1) {
          answers.splice(index, 1);
        } else {
          answers.push(optionIndex);
        }
        if (answers.length === 0) {
          delete this.userAnswers[questionId];
        }
      } else {
        this.userAnswers[questionId] = optionIndex;
      }
    },
    isSelected(questionId, optionIndex) {
      const answer = this.userAnswers[questionId];
      if (Array.isArray(answer)) {
        return answer.includes(optionIndex);
      }
      return answer === optionIndex;
    },
    previousQuestion() {
      if (this.currentQuestionIndex > 0) this.currentQuestionIndex--;
    },
    nextQuestion() {
      if (this.currentQuestionIndex < this.questions.length - 1) this.currentQuestionIndex++;
    },
    formatTime(seconds) {
      const minutes = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    },
    showSubmitModal() {
      this.submitModal.show();
    },
    async submitQuiz() {
      if (this.timer) clearInterval(this.timer);
      this.submitting = true;
      try {
        const formattedAnswers = {};
        for (const qId in this.userAnswers) {
          const answer = this.userAnswers[qId];
          formattedAnswers[qId] = Array.isArray(answer) ? answer.sort().join(',') : answer;
        }
        const response = await quizAPI.submitQuiz(this.quiz.id, {
          answers: formattedAnswers,
          start_time: this.startTime.toISOString(),
        });
        this.submitModal.hide();
        this.$router.push(`/user/scores/${response.data.results.score.id}`);
      } catch (error) {
        console.error('Error submitting quiz:', error);
      } finally {
        this.submitting = false;
      }
    },
  },
  async mounted() {
    this.submitModal = new Modal(document.getElementById('submitModal'));
    await this.loadQuiz();
  },
  beforeUnmount() {
    if (this.timer) clearInterval(this.timer);
  },
};
</script>

<style scoped>
.quiz-attempt-fullscreen {
  background: #0D0C0F;
  color: #e0e0e0;
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}
.quiz-container {
  width: 100%;
  max-width: 1100px;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.stats-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #1A1A1A;
  border: 1px solid #2c2c2c;
  padding: 0.75rem 1.5rem;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
}
.stat-item { color: #a0a0a0; }
.timer { font-weight: 500; color: white; }
.timer.critical { color: #EF4444; }
.progress-container {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem 1.5rem;
  background-color: #1A1A1A;
  border: 1px solid #2c2c2c;
  border-radius: 0.5rem;
  margin-bottom: 2rem;
}
.progress-info {
  color: #a0a0a0;
  white-space: nowrap;
}
.progress {
  flex-grow: 1; /* Make the progress bar take up available space */
  height: 8px;
  background-color: #2c2c2c;
  border-radius: 4px;
}
.progress-percentage {
    color: #a0a0a0;
    white-space: nowrap;
}
.progress-bar { background-color: #8B5CF6; }
.question-box {
  background-color: #1A1A1A;
  border: 1px solid #2c2c2c;
  border-radius: 0.75rem;
  padding: 2rem;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden; /* Prevent internal content from overflowing */
}
.question-statement {
  font-size: 1.4rem;
  color: white;
  margin-bottom: 2rem;
  word-wrap: break-word;
  white-space: pre-wrap;
  overflow-y: auto; /* Allow scrolling for very long questions */
  flex-shrink: 1;
}
.options-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
  margin-top: auto; /* Push options to the bottom */
}
.option-btn {
  background-color: #2c2c2c;
  border: 1px solid #444;
  color: #e0e0e0;
  padding: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
}
.option-text {
  word-break: break-word;
}
.option-btn:hover { border-color: #8B5CF6; }
.option-btn.selected { background-color: #8B5CF6; border-color: #8B5CF6; color: white; }
.option-letter {
  width: 24px;
  height: 24px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 1rem;
  font-size: 0.8rem;
  flex-shrink: 0;
}
.option-circle {
  border: 2px solid #8B5CF6;
  border-radius: 50%;
  background: #222;
}
.option-square {
  border: 2px solid #8B5CF6;
  border-radius: 4px;
  background: #222;
}
.navigation-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 2rem;
  flex-shrink: 0;
}
.btn-nav { background-color: #1A1A1A; border: 1px solid #444; color: #a0a0a0; }
.btn-submit { background-color: #8B5CF6; border: none; color: white; padding: 0.75rem 2rem; border-radius: 0.5rem; }
.loading-state { color: #a0a0a0; }
</style>
