<template>
  <div class="admin-quizzes p-3 p-md-4">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-section bg-primary text-white p-4 rounded shadow-sm d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Manage Quizzes</h2>
              <p class="mb-0 opacity-75">Create, edit, and assign quizzes to chapters.</p>
            </div>
            <button @click="showCreateModal" class="btn btn-outline-light">
              <i class="fas fa-plus me-2"></i>
              Add Quiz
            </button>
          </div>
        </div>
      </div>

      <!-- Quizzes List -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-2">Loading quizzes...</p>
              </div>
              
              <div v-else-if="quizzes.length === 0" class="text-center py-5">
                <i class="fas fa-clipboard-list fa-4x text-muted mb-3"></i>
                <h4 class="text-muted">No quizzes found</h4>
                <p class="text-muted">Create your first quiz to get started.</p>
                <button @click="showCreateModal" class="btn btn-primary mt-2">
                  <i class="fas fa-plus me-2"></i>
                  Add Quiz
                </button>
              </div>
              
              <div v-else class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>Quiz Title</th>
                      <th>Chapter</th>
                      <th>Subject</th>
                      <th>Date</th>
                      <th>Duration (Mins)</th>
                      <th>Questions</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="quiz in quizzes" :key="quiz.id">
                      <td><strong>{{ quiz.title }}</strong></td>
                      <td>{{ quiz.chapter_name }}</td>
                      <td>
                        <span class="badge bg-secondary-subtle text-secondary-emphasis">{{ quiz.subject_name }}</span>
                      </td>
                      <td>{{ formatDate(quiz.date_of_quiz) }}</td>
                      <td>{{ quiz.duration }}</td>
                      <td>
                        <span class="badge bg-info-subtle text-info-emphasis">{{ quiz.questions_count || 0 }}</span>
                      </td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <router-link :to="`/admin/quiz/${quiz.id}/questions`" class="btn btn-outline-secondary" title="Manage Questions">
                            <i class="fas fa-list-ol"></i>
                          </router-link>
                          <button @click="editQuiz(quiz)" class="btn btn-outline-primary" title="Edit Quiz">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button @click="deleteQuiz(quiz.id, quiz.title)" class="btn btn-outline-danger" title="Delete Quiz">
                            <i class="fas fa-trash"></i>
                          </button>
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
    </div>

    <!-- Create/Edit Quiz Modal -->
    <div class="modal fade" id="quizModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Edit Quiz' : 'Create Quiz' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <form @submit.prevent="saveQuiz">
            <div class="modal-body">
              <div class="mb-3">
                <label for="chapter" class="form-label">Chapter *</label>
                <select v-model="form.chapter_id" id="chapter" class="form-select" :class="{ 'is-invalid': errors.chapter_id }" required>
                  <option disabled value="">Select a chapter</option>
                  <optgroup v-for="subject in groupedChapters" :key="subject.id" :label="subject.name">
                    <option v-for="chapter in subject.chapters" :key="chapter.id" :value="chapter.id">
                      {{ chapter.name }}
                    </option>
                  </optgroup>
                </select>
                <div v-if="errors.chapter_id" class="invalid-feedback">{{ errors.chapter_id }}</div>
              </div>

              <div class="mb-3">
                <label for="quizTitle" class="form-label">Quiz Title *</label>
                <input v-model.trim="form.title" type="text" id="quizTitle" class="form-control" :class="{ 'is-invalid': errors.title }" required>
                <div v-if="errors.title" class="invalid-feedback">{{ errors.title }}</div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="quizDate" class="form-label">Date of Quiz *</label>
                  <input v-model="form.date_of_quiz" type="date" id="quizDate" class="form-control" :class="{ 'is-invalid': errors.date_of_quiz }" required>
                  <div v-if="errors.date_of_quiz" class="invalid-feedback">{{ errors.date_of_quiz }}</div>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="quizDuration" class="form-label">Duration (in minutes) *</label>
                  <input v-model.number="form.duration" type="number" id="quizDuration" class="form-control" :class="{ 'is-invalid': errors.duration }" required min="1">
                   <div v-if="errors.duration" class="invalid-feedback">{{ errors.duration }}</div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="saving">
                <span v-if="saving" class="spinner-border spinner-border-sm me-2"></span>
                {{ saving ? 'Saving...' : (isEdit ? 'Update' : 'Create') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Modal } from 'bootstrap';
import { adminAPI } from '@/services/api';

export default {
  name: 'AdminQuizzes',
  data() {
    return {
      quizzes: [],
      chapters: [],
      loading: true,
      saving: false,
      isEdit: false,
      form: {
        title: '',
        chapter_id: '',
        date_of_quiz: '',
        duration: 30 // Default duration in minutes
      },
      errors: {},
      currentQuizId: null,
      quizModal: null
    };
  },
  computed: {
    groupedChapters() {
      const groups = {};
      this.chapters.forEach(chapter => {
        if (!groups[chapter.subject_id]) {
          groups[chapter.subject_id] = {
            id: chapter.subject_id,
            name: chapter.subject_name,
            chapters: []
          };
        }
        groups[chapter.subject_id].chapters.push(chapter);
      });
      return Object.values(groups);
    }
  },
  async mounted() {
    this.quizModal = new Modal(document.getElementById('quizModal'));
    await this.loadInitialData();
  },
  methods: {
    async loadInitialData() {
      try {
        this.loading = true;
        const [quizzesResponse, chaptersResponse] = await Promise.all([
          adminAPI.getQuizzes(),
          adminAPI.getChapters()
        ]);
        this.quizzes = quizzesResponse.data;
        this.chapters = chaptersResponse.data;
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load quizzes and chapters.'
        });
      } finally {
        this.loading = false;
      }
    },
    showCreateModal() {
      this.isEdit = false;
      this.form = {
        title: '',
        chapter_id: '',
        date_of_quiz: new Date().toISOString().split('T')[0], // Default to today
        duration: 30
      };
      this.errors = {};
      this.currentQuizId = null;
      this.quizModal.show();
    },
    editQuiz(quiz) {
      this.isEdit = true;
      this.currentQuizId = quiz.id;
      this.form = {
        title: quiz.title || '',
        chapter_id: quiz.chapter_id,
        date_of_quiz: quiz.date_of_quiz.split('T')[0], // Format for date input
        duration: quiz.duration
      };
      this.errors = {};
      this.quizModal.show();
    },
    async saveQuiz() {
      this.saving = true;
      this.errors = {};
      try {
        if (this.isEdit) {
          await adminAPI.updateQuiz(this.currentQuizId, this.form);
          this.$store.dispatch('showAlert', { type: 'success', message: 'Quiz updated successfully.' });
        } else {
          await adminAPI.createQuiz(this.form);
          this.$store.dispatch('showAlert', { type: 'success', message: 'Quiz created successfully.' });
        }
        this.quizModal.hide();
        await this.loadInitialData(); // Refresh list
      } catch (error) {
        if (error.response?.data?.errors) {
          this.errors = error.response.data.errors;
        } else {
          this.$store.dispatch('showAlert', {
            type: 'error',
            message: error.response?.data?.error || 'Failed to save quiz.'
          });
        }
      } finally {
        this.saving = false;
      }
    },
    async deleteQuiz(quizId, quizTitle) {
      const confirmMessage = `Are you sure you want to delete the quiz "${quizTitle}"? This will also delete all its questions.`;
      if (!confirm(confirmMessage)) return;
      
      try {
        await adminAPI.deleteQuiz(quizId);
        this.$store.dispatch('showAlert', { type: 'success', message: 'Quiz deleted successfully.' });
        this.quizzes = this.quizzes.filter(q => q.id !== quizId);
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to delete quiz.'
        });
      }
    },
    formatDate(dateString) {
      if (!dateString) return '-';
      return new Date(dateString).toLocaleDateString();
    }
  }
};
</script>
