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
              <h1 class="display-4 mb-2">{{ score.percentage }}%</h1>
              <h3 class="mb-1">{{ score.quiz_title }}</h3>
            </div>
          </div>
        </div>

        <!-- Score Summary Cards -->
        <div class="row g-4 mb-4">
          <div class="col-md-3">
            <div class="summary-card card text-center">
              <div class="card-body">
                <i class="fas fa-check-circle fa-2x text-success mb-3"></i>
                <h4>{{ score.total_scored }}</h4>
                <p class="text-muted mb-0">Correct Answers</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="summary-card card text-center">
              <div class="card-body">
                <i class="fas fa-times-circle fa-2x text-danger mb-3"></i>
                <h4>{{ score.total_questions - score.total_scored }}</h4>
                <p class="text-muted mb-0">Incorrect Answers</p>
              </div>
            </div>
          </div>
          <div class="col-md-3">
            <div class="summary-card card text-center">
              <div class="card-body">
                <i class="fas fa-clock fa-2x text-info mb-3"></i>
                <h4>{{ formatDuration(score.time_taken) }}</h4>
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
              <div class="card-header">
                <h5 class="mb-0">Detailed Results</h5>
              </div>
              <div class="card-body">
                <div v-for="(result, index) in results" :key="index" class="question-review mb-4">
                  <div class="question-header d-flex align-items-start mb-3">
                    <div class="question-number me-3">
                      <span class="badge" :class="result.is_correct ? 'bg-success' : 'bg-danger'">
                        {{ index + 1 }}
                      </span>
                    </div>
                    <div class="question-content flex-grow-1">
                      <h6 class="mb-2">{{ result.question_statement }}</h6>
                    </div>
                  </div>
                  <div class="answers-section">
                    <div v-for="(option, optIndex) in result.options" :key="optIndex" class="answer-option mb-2 p-3 border rounded" :class="getOptionClass(result, optIndex + 1)">
                      {{ option }}
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
import { userAPI } from '@/services/api';

export default {
  name: 'QuizResults',
  data() {
    return {
      score: null,
      results: [],
      loading: true,
    };
  },
  async mounted() {
    await this.loadResults();
  },
  methods: {
    async loadResults() {
      try {
        const scoreId = this.$route.params.id;
        const response = await userAPI.getScoreDetails(scoreId);
        this.score = response.data.score;
        this.results = response.data.results;
      } catch (error) {
        console.error('Error loading results:', error);
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString();
    },
    formatDuration(seconds) {
      if (!seconds) return 'N/A';
      const minutes = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${minutes}m ${secs}s`;
    },
    getOptionClass(result, optionIndex) {
      const isCorrect = optionIndex === result.correct_answer;
      const isSelected = optionIndex === result.selected_answer;

      if (isSelected && isCorrect) return 'bg-success-subtle border-success';
      if (isSelected && !isCorrect) return 'bg-danger-subtle border-danger';
      if (isCorrect) return 'border-success';
      return '';
    },
  },
};
</script>

<style scoped>
.quiz-results {
  padding: 2rem;
}
</style>
