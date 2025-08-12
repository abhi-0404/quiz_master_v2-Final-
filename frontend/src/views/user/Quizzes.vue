/* Quiz Library subtitle white */
.quiz-library-desc {
  color: #fff;
  font-size: 1rem;
}
/* Bold quiz name */
.fw-bold {
  font-weight: bold;
}
/* Space between quiz details */
.quiz-meta-light {
  font-size: 0.875rem;
  color: #fff;
  display: flex;
  gap: 2rem;
  margin-top: 0.5rem;
}
.quiz-detail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}
/* Quiz actions spacing */
.quiz-actions {
  display: flex;
  gap: 0.5rem;
}
<template>
  <div class="user-quizzes">
    <div class="container-fluid">
      <!-- Blue Welcome Card with Search -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-card bg-primary text-white p-4 rounded d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-0">Quizzes</h2>
              <p class="mb-0 opacity-75">Create, manage and analyze your quizzes</p>
            </div>
            <div class="search-box-blue d-flex align-items-center">
              <i class="fas fa-search me-2" style="color: white;"></i>
              <input type="text" v-model="searchQuery" placeholder="Search quizzes..." class="form-control search-input-blue" />
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
      </div>

      <!-- Quiz Library -->
      <div v-else class="card bg-dark border-0 px-4 py-3" style="border-radius: 1rem; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
        <div class="card-header border-0 bg-transparent px-0 pt-2 pb-2">
          <h5 class="mb-0 fw-bold">Quiz Library</h5>
          <p class="quiz-library-desc mb-0">Browse and manage all your quizzes</p>
        </div>
        <div class="card-body px-0">
          <div v-if="filteredQuizzes.length === 0" class="text-center py-5 text-muted">
            <p>No quizzes found.</p>
          </div>
          <ul v-else class="list-group list-group-flush">
            <li v-for="quiz in filteredQuizzes" :key="quiz.id" class="list-group-item quiz-list-item d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center w-100">
                <div class="icon-box-light me-3">
                  <i class="fas fa-book-open"></i>
                </div>
                <div class="flex-grow-1">
                  <h6 class="mb-1 fw-bold quiz-title">{{ quiz.title }}</h6>
                  <p class="text-muted small mb-1">{{ quiz.description }}</p>
                  <div class="quiz-meta-light">
                    <span class="quiz-detail"><i class="fas fa-list-ul me-1"></i>{{ quiz.questions_count }} questions</span>
                    <span class="quiz-detail"><i class="fas fa-clock me-1"></i>{{ quiz.duration }} min</span>
                    <span class="quiz-detail"><i class="fas fa-calendar-alt me-1"></i>{{ formatDate(quiz.date_of_quiz) }}</span>
                  </div>
                </div>
                <div class="quiz-actions d-flex flex-row gap-2 ms-3">
                  <template v-if="getQuizStatus(quiz) === 'start'">
                    <button class="btn btn-sm btn-dark quiz-btn" @click="aboutQuiz(quiz.id)">About</button>
                    <button @click="startQuiz(quiz.id)" class="btn btn-sm btn-live quiz-btn">Live</button>
                  </template>
                  <template v-else-if="getQuizStatus(quiz) === 'result'">
                    <button class="btn btn-sm btn-dark quiz-btn" @click="viewResult(quiz.id)">Result</button>
                    <button @click="startQuiz(quiz.id)" class="btn btn-sm btn-purple quiz-btn">Restart</button>
                  </template>
                  <template v-else-if="getQuizStatus(quiz) === 'over'">
                    <button class="btn btn-sm btn-dark quiz-btn" @click="aboutQuiz(quiz.id)">About</button>
                    <button class="btn btn-sm btn-info quiz-btn" @click="showUpcomingMsg(quiz)">Upcoming</button>
                  </template>
                  <template v-else-if="getQuizStatus(quiz) === 'miss'">
                    <button class="btn btn-sm btn-dark quiz-btn" @click="aboutQuiz(quiz.id)">About</button>
                    <button class="btn btn-sm btn-miss quiz-btn" @click="showMissMsg(quiz)">Miss</button>
                  </template>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { userAPI } from '@/services/api';

export default {
  name: 'UserQuizzes',
  data() {
    return {
      quizzes: [],
      loading: true,
      searchQuery: ''
    };
  },
  computed: {
    filteredQuizzes() {
      if (!this.searchQuery) {
        return this.quizzes;
      }
      return this.quizzes.filter(quiz =>
        quiz.title.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    }
  },
  methods: {
    async loadQuizzes() {
      try {
        this.loading = true;
        const response = await userAPI.getQuizzes();
        this.quizzes = response.data;
      } catch (error) {
        console.error('Error loading quizzes:', error);
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load quizzes.'
        });
      } finally {
        this.loading = false;
      }
    },
    getQuizStatus(quiz) {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      const quizDate = new Date(quiz.date_of_quiz);
      quizDate.setHours(0, 0, 0, 0);

      if (quiz.user_has_attempted) {
        return 'result';
      }
      if (quizDate < today) {
        return 'miss';
      }
      if (quizDate > today) {
        return 'over';
      }
      return 'start';
    },
    startQuiz(quizId) {
      this.$router.push(`/user/quiz/${quizId}/attempt`);
    },
    viewResult(quizId) {
      // This will redirect to your main scores page.
      // You can build a specific result page later if needed.
      this.$router.push(`/user/scores`); 
    },
    reviewQuiz(quizId) {
      // Example: redirect to a review page for the quiz
      this.$router.push(`/user/quiz/${quizId}/review`);
    },
    aboutQuiz(quizId) {
      // Example: redirect to an about page for the quiz
      this.$router.push(`/user/quiz/${quizId}/about`);
    },
    showUpcomingMsg(quiz) {
      alert(`${quiz.title} is not yet Live`);
    },
    showMissMsg(quiz) {
      alert('Quiz deadline over.');
    },
    formatDate(dateString) {
      if (!dateString) return '';
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Date(dateString).toLocaleDateString('en-GB', options);
    }
  },
  async mounted() {
    await this.loadQuizzes();
  }
};
</script>

<style scoped>
.btn-live {
  background-color: #e74c3c;
  color: #fff;
  border: none;
}
.btn-live:hover {
  background-color: #c0392b;
  color: #fff;
}
.btn-miss {
  background-color: #3498db;
  color: #fff;
  border: none;
}
.btn-miss:hover {
  background-color: #217dbb;
  color: #fff;
}
.quiz-btn {
  min-width: 90px;
  max-width: 90px;
  text-align: center;
  white-space: nowrap;
  font-weight: 500;
  border-radius: 0.5rem;
}
.btn-purple {
  background-color: #8e44ad;
  color: #fff;
  border: none;
}
.btn-purple:hover {
  background-color: #6c3483;
  color: #fff;
}
/* Quiz Library subtitle white */
.quiz-library-desc {
  color: #fff;
  font-size: 1rem;
}
/* Bold quiz name */
.fw-bold {
  font-weight: bold;
}
.quiz-title {
  font-size: 1.1rem;
  letter-spacing: 0.5px;
  font-weight: bold;
  color: #222;
}
/* Space between quiz details */
.quiz-meta-light {
  font-size: 0.95rem;
  color: #222;
  display: flex;
  gap: 2rem;
  margin-top: 0.5rem;
}
.quiz-detail {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #222;
}
.quiz-detail i {
  color: #222 !important;
}
/* Quiz actions spacing */
.quiz-actions {
  display: flex;
  gap: 0.5rem;
}
.quiz-list-item {
  background: #fff;
  border-radius: 0.5rem;
  margin-bottom: 1rem;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}
.user-quizzes {
  padding: 2rem;
}
.search-box {
  position: relative;
  width: 250px;
}
.search-box .fa-search {
  position: absolute;
  left: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #6c757d;
}
/* Blue Welcome Card (copied from Dashboard.vue) */
.welcome-card {
  background: var(--primary-color, #04ff60ff);
  color: #fff;
  border-radius: 1rem;
  box-shadow: 0 2px 8px rgba(13, 110, 253, 0.08);
  padding: 2rem;
  margin-bottom: 1.5rem;
}

/* Blue Search Box */
.search-box-blue {
  background: var(--primary-color, #0d6efd);
  border-radius: 0.375rem;
  padding: 0.5rem 1rem;
  border: 2px solid #fff;
}
.search-input-blue {
  border: none;
  background: transparent;
  color: #fff;
  box-shadow: none;
  outline: none;
  font-size: 1rem;
  width: 180px;
}
.search-input-blue::placeholder {
  color: #fff;
  opacity: 0.8;
}
  justify-content: center;
  border-radius: 8px;
  margin-right: 1rem;
  flex-shrink: 0;
.quiz-meta-light {
  font-size: 0.875rem;
  color: #6c757d;
  display: flex;
  gap: 1.5rem;
  margin-top: 0.5rem;
}
.quiz-actions .btn {
  width: 80px;
}
</style>
