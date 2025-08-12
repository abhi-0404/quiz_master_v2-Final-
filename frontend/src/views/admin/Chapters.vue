<template>
  <div class="admin-chapters p-3 p-md-4">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-section bg-primary text-white p-4 rounded shadow-sm d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Manage Chapters</h2>
              <p class="mb-0 opacity-75">Organize content by chapters within subjects</p>
            </div>
            <button @click="showCreateModal" class="btn btn-outline-light">
              <i class="fas fa-plus me-2"></i>
              Add Chapter
            </button>
          </div>
        </div>
      </div>

      <!-- Chapters List -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status"></div>
                <p class="mt-2">Loading chapters...</p>
              </div>
              
              <div v-else-if="chapters.length === 0" class="text-center py-5">
                <i class="fas fa-book-open fa-4x text-muted mb-3"></i>
                <h4 class="text-muted">No chapters found</h4>
                <p class="text-muted">Create your first chapter to get started.</p>
                <button @click="showCreateModal" class="btn btn-primary mt-2">
                  <i class="fas fa-plus me-2"></i>
                  Add Chapter
                </button>
              </div>
              
              <div v-else class="table-responsive">
                <table class="table table-hover align-middle">
                  <thead class="table-light">
                    <tr>
                      <th>Name</th>
                      <th>Description</th>
                      <th>Subject</th>
                      <th>Quizzes</th>
                      <th>Created</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="chapter in chapters" :key="chapter.id">
                      <td><strong>{{ chapter.name }}</strong></td>
                      <td class="text-muted">{{ chapter.description || '-' }}</td>
                      <td>
                        <span class="badge bg-secondary-subtle text-secondary-emphasis">{{ chapter.subject_name }}</span>
                      </td>
                      <td>
                        <span class="badge bg-info-subtle text-info-emphasis">{{ chapter.quiz_count || 0 }}</span>
                      </td>
                      <td>{{ formatDate(chapter.created_at) }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button @click="openAddQuizModal(chapter)" class="btn btn-outline-success" title="Add Quiz">
                            <i class="fas fa-plus"></i>
                          </button>
                          <button @click="editChapter(chapter)" class="btn btn-outline-primary" title="Edit">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button @click="deleteChapter(chapter.id, chapter.name)" class="btn btn-outline-danger" title="Delete">
                            <i class="fas fa-trash"></i>
                          </button>
                        </div>
    <!-- Add Quiz Modal -->
    <div class="modal fade" id="addQuizModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Quiz to {{ currentChapter?.name }}</h5>
            <button type="button" class="btn-close" @click="closeAddQuizModal"></button>
          </div>
          <form @submit.prevent="saveQuiz">
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Quiz Title *</label>
                <input v-model="quizForm.title" type="text" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="quizForm.description" class="form-control" rows="2"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Date of Quiz *</label>
                <input v-model="quizForm.date_of_quiz" type="date" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Duration (minutes) *</label>
                <input v-model.number="quizForm.duration" type="number" class="form-control" min="1" required>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeAddQuizModal">Cancel</button>
              <button type="submit" class="btn btn-success" :disabled="quizSaving">
                <span v-if="quizSaving" class="spinner-border spinner-border-sm me-2"></span>
                {{ quizSaving ? 'Saving...' : 'Add Quiz' }}
              </button>
            </div>
          </form>
        </div>
      </div>
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

    <!-- Create/Edit Chapter Modal -->
    <div class="modal fade" id="chapterModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Edit Chapter' : 'Create Chapter' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <form @submit.prevent="saveChapter">
            <div class="modal-body">
              <div class="mb-3">
                <label for="subject" class="form-label">Subject *</label>
                <select v-model="form.subject_id" id="subject" class="form-select" :class="{ 'is-invalid': errors.subject_id }" required>
                  <option disabled value="">Select a subject</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
                <div v-if="errors.subject_id" class="invalid-feedback">{{ errors.subject_id }}</div>
              </div>

              <div class="mb-3">
                <label for="chapterName" class="form-label">Chapter Name *</label>
                <input v-model.trim="form.name" type="text" id="chapterName" class="form-control" :class="{ 'is-invalid': errors.name }" required>
                <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
              </div>
              
              <div class="mb-3">
                <label for="chapterDescription" class="form-label">Description</label>
                <textarea v-model.trim="form.description" id="chapterDescription" class="form-control" :class="{ 'is-invalid': errors.description }" rows="3"></textarea>
                <div v-if="errors.description" class="invalid-feedback">{{ errors.description }}</div>
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
  name: 'AdminChapters',
  data() {
    return {
      chapters: [],
      subjects: [],
      loading: true,
      saving: false,
      isEdit: false,
      form: {
        name: '',
        description: '',
        subject_id: ''
      },
      errors: {},
      currentChapterId: null,
      chapterModal: null,
      addQuizModal: null,
      currentChapter: null,
      quizForm: {
        title: '',
        description: '',
        date_of_quiz: '',
        duration: 60
      },
      quizSaving: false
    };
  },
  async mounted() {
    this.chapterModal = new Modal(document.getElementById('chapterModal'));
    await this.loadInitialData();
  },
  methods: {
    openAddQuizModal(chapter) {
      this.currentChapter = chapter;
      this.quizForm = { title: '', description: '', date_of_quiz: '', duration: 60 };
      this.quizSaving = false;
      this.$nextTick(() => {
        if (!this.addQuizModal) {
          this.addQuizModal = new Modal(document.getElementById('addQuizModal'));
        }
        this.addQuizModal.show();
      });
    },
    closeAddQuizModal() {
      if (this.addQuizModal) this.addQuizModal.hide();
    },
    async saveQuiz() {
      if (!this.quizForm.title.trim() || !this.quizForm.date_of_quiz || !this.quizForm.duration) return;
      this.quizSaving = true;
      try {
        await adminAPI.createQuiz({
          chapter_id: this.currentChapter.id,
          title: this.quizForm.title,
          description: this.quizForm.description,
          date_of_quiz: this.quizForm.date_of_quiz,
          duration: this.quizForm.duration
        });
        this.closeAddQuizModal();
        this.$store.dispatch('showAlert', {
          type: 'success',
          message: 'Quiz added.'
        });
        this.loadInitialData();
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to add quiz.'
        });
      } finally {
        this.quizSaving = false;
      }
    },
    async loadInitialData() {
      try {
        this.loading = true;
        const [chaptersResponse, subjectsResponse] = await Promise.all([
          adminAPI.getChapters(),
          adminAPI.getSubjects() // Needed for the dropdown
        ]);
        this.chapters = chaptersResponse.data;
        this.subjects = subjectsResponse.data;
      } catch (error) {
        console.error('Error loading initial data:', error);
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load chapters and subjects.'
        });
      } finally {
        this.loading = false;
      }
    },
    showCreateModal() {
      this.isEdit = false;
      this.form = { name: '', description: '', subject_id: '' };
      this.errors = {};
      this.currentChapterId = null;
      this.chapterModal.show();
    },
    editChapter(chapter) {
      this.isEdit = true;
      this.currentChapterId = chapter.id;
      this.form = {
        name: chapter.name,
        description: chapter.description || '',
        subject_id: chapter.subject_id
      };
      this.errors = {};
      this.chapterModal.show();
    },
    async saveChapter() {
      this.saving = true;
      this.errors = {};
      try {
        if (this.isEdit) {
          await adminAPI.updateChapter(this.currentChapterId, this.form);
          this.$store.dispatch('showAlert', { type: 'success', message: 'Chapter updated successfully.' });
        } else {
          await adminAPI.createChapter(this.form);
          this.$store.dispatch('showAlert', { type: 'success', message: 'Chapter created successfully.' });
        }
        this.chapterModal.hide();
        await this.loadInitialData(); // Refresh the list
      } catch (error) {
        if (error.response && error.response.data && error.response.data.errors) {
          this.errors = error.response.data.errors;
        } else {
          this.$store.dispatch('showAlert', {
            type: 'error',
            message: error.response?.data?.error || 'Failed to save chapter.'
          });
        }
      } finally {
        this.saving = false;
      }
    },
    async deleteChapter(chapterId, chapterName) {
      if (!confirm(`Are you sure you want to delete the chapter "${chapterName}"?`)) {
        return;
      }
      try {
        await adminAPI.deleteChapter(chapterId);
        this.$store.dispatch('showAlert', { type: 'success', message: 'Chapter deleted successfully.' });
        // Remove from local array to update UI instantly
        this.chapters = this.chapters.filter(c => c.id !== chapterId);
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to delete chapter.'
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
