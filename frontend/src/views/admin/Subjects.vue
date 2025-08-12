<template>
  <div class="admin-subjects">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-section bg-primary text-white p-4 rounded shadow-sm d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Manage Subjects</h2>
              <p class="mb-0 opacity-75">Create and manage quiz subjects</p>
            </div>
            <button @click="showCreateModal" class="btn btn-outline-light">
              <i class="fas fa-plus me-2"></i>
              Add Subject
            </button>
          </div>
        </div>
      </div>

      <!-- Subjects List -->
      <div class="row">
        <div class="col-12">
          <div class="card">
            <div class="card-body">
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status"></div>
              </div>
              
              <div v-else-if="subjects.length === 0" class="text-center py-5">
                <i class="fas fa-book fa-4x text-muted mb-3"></i>
                <h4 class="text-muted">No subjects found</h4>
                <p class="text-muted">Create your first subject to get started.</p>
                <button @click="showCreateModal" class="btn btn-primary">
                  <i class="fas fa-plus me-2"></i>
                  Add Subject
                </button>
              </div>
              
              <div v-else class="table-responsive">
                <table class="table table-hover">
                  <thead class="table-light">
                    <tr>
                      <th>Name</th>
                      <th>Description</th>
                      <th>Chapters</th>
                      <th>Quizzes</th>
                      <th>Created</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="subject in subjects" :key="subject.id">
                      <td>
                        <strong>{{ subject.name }}</strong>
                      </td>
                      <td>{{ subject.description || 'No description' }}</td>
                      <td>
                        <span class="badge bg-primary">{{ subject.chapters_count || 0 }}</span>
                      </td>
                      <td>
                        <span class="badge bg-success">{{ subject.quiz_count || 0 }}</span>
                      </td>
                      <td>{{ formatDate(subject.created_at) }}</td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button 
                            @click="openAddChapterModal(subject)"
                            class="btn btn-outline-success"
                            title="Add Chapter"
                          >
                            <i class="fas fa-plus"></i>
                          </button>
                          <button 
                            @click="editSubject(subject)"
                            class="btn btn-outline-primary"
                            title="Edit"
                          >
                            <i class="fas fa-edit"></i>
                          </button>
                          <button 
                            @click="deleteSubject(subject.id, subject.name)"
                            class="btn btn-outline-danger"
                            title="Delete"
                          >
                            <i class="fas fa-trash"></i>
                          </button>
                        </div>
    <!-- Add Chapter Modal -->
    <div class="modal fade" id="addChapterModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Add Chapter to {{ currentSubject?.name }}</h5>
            <button type="button" class="btn-close" @click="closeAddChapterModal"></button>
          </div>
          <form @submit.prevent="saveChapter">
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Chapter Name *</label>
                <input v-model="chapterForm.name" type="text" class="form-control" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="chapterForm.description" class="form-control" rows="2"></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeAddChapterModal">Cancel</button>
              <button type="submit" class="btn btn-success" :disabled="chapterSaving">
                <span v-if="chapterSaving" class="spinner-border spinner-border-sm me-2"></span>
                {{ chapterSaving ? 'Saving...' : 'Add Chapter' }}
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

    <!-- Create/Edit Modal -->
    <div class="modal fade" id="subjectModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Edit Subject' : 'Create Subject' }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
          </div>
          <form @submit.prevent="saveSubject">
            <div class="modal-body">
              <div class="mb-3">
                <label class="form-label">Subject Name *</label>
                <input
                  v-model="form.name"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.name }"
                  required
                >
                <div v-if="errors.name" class="invalid-feedback">{{ errors.name }}</div>
              </div>
              
              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea
                  v-model="form.description"
                  class="form-control"
                  :class="{ 'is-invalid': errors.description }"
                  rows="3"
                ></textarea>
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
import { Modal } from 'bootstrap'
import { adminAPI } from '@/services/api'

export default {
  name: 'AdminSubjects',
  data() {
    return {
      subjects: [],
      loading: true,
      saving: false,
      isEdit: false,
      form: {
        name: '',
        description: ''
      },
      errors: {},
      currentSubject: null,
      subjectModal: null,
      addChapterModal: null,
      chapterForm: {
        name: '',
        description: ''
      },
      chapterSaving: false
          }
        },
        async mounted() {
          this.subjectModal = new Modal(document.getElementById('subjectModal'))
          await this.loadSubjects()
        },
        methods: {
          openAddChapterModal(subject) {
            this.currentSubject = subject;
            this.chapterForm = { name: '', description: '' };
            this.chapterSaving = false;
            this.$nextTick(() => {
              if (!this.addChapterModal) {
                this.addChapterModal = new Modal(document.getElementById('addChapterModal'));
              }
              this.addChapterModal.show();
            });
          },
          closeAddChapterModal() {
            if (this.addChapterModal) this.addChapterModal.hide();
          },
          async saveChapter() {
            if (!this.chapterForm.name.trim()) return;
            this.chapterSaving = true;
            try {
              await adminAPI.createChapter({
                subject_id: this.currentSubject.id,
                name: this.chapterForm.name,
                description: this.chapterForm.description
              });
              this.closeAddChapterModal();
              this.$store.dispatch('showAlert', {
                type: 'success',
                message: 'Chapter added.'
              });
              this.loadSubjects();
            } catch (error) {
              this.$store.dispatch('showAlert', {
                type: 'error',
                message: 'Failed to add chapter.'
              });
            } finally {
              this.chapterSaving = false;
            }
          },
          // ...existing code...
    async loadSubjects() {
      try {
        this.loading = true
        const response = await adminAPI.getSubjects()
        this.subjects = Array.isArray(response.data) ? response.data : []
        console.log('Loaded subjects:', this.subjects.length, 'subjects')
        console.log('Subjects array:', this.subjects)
      } catch (error) {
        console.error('Error loading subjects:', error)
        console.error('Error response:', error.response)
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load subjects'
        })
      } finally {
        this.loading = false
      }
    },
    showCreateModal() {
      this.isEdit = false
      this.form = { name: '', description: '' }
      this.errors = {}
      this.subjectModal.show()
    },
    editSubject(subject) {
      this.isEdit = true
      this.currentSubject = subject
      this.form = {
        name: subject.name,
        description: subject.description || ''
      }
      this.errors = {}
      this.subjectModal.show()
    },
    async saveSubject() {
      try {
        this.saving = true
        this.errors = {}
        
        console.log('Saving subject. isEdit:', this.isEdit, 'Form data:', this.form)
        
        if (this.isEdit) {
          const response = await adminAPI.updateSubject(this.currentSubject.id, this.form)
          console.log('Update response:', response.data)
          // Update the subject in the local array
          const index = this.subjects.findIndex(s => s.id === this.currentSubject.id)
          if (index !== -1) {
            this.subjects[index] = response.data.subject
          }
          this.$store.dispatch('showAlert', {
            type: 'success',
            message: 'Subject updated successfully'
          })
        } else {
          console.log('Creating subject with data:', this.form)
          const response = await adminAPI.createSubject(this.form)
          console.log('Create subject response:', response)
          console.log('Response data:', response.data)
          
          // Check if we got the expected response structure
          if (response.data && response.data.subject) {
            // Add the new subject to the local array
            this.subjects.push(response.data.subject)
            console.log('Added subject to local array. Total subjects:', this.subjects.length)
            console.log('Current subjects:', this.subjects.map(s => ({ id: s.id, name: s.name })))
          } else {
            console.warn('Unexpected response structure, reloading subjects')
            await this.loadSubjects()
          }
          
          this.$store.dispatch('showAlert', {
            type: 'success',
            message: 'Subject created successfully'
          })
        }
        
        this.subjectModal.hide()
      } catch (error) {
        console.error('Error saving subject:', error)
        console.error('Error response:', error.response)
        console.error('Error data:', error.response?.data)
        if (error.response?.data?.errors) {
          this.errors = error.response.data.errors
        } else {
          this.$store.dispatch('showAlert', {
            type: 'error',
            message: error.response?.data?.error || 'Failed to save subject'
          })
        }
      } finally {
        this.saving = false
      }
    },
    async deleteSubject(subjectId, subjectName) {
      if (!confirm(`Are you sure you want to delete "${subjectName}"?`)) return
      
      try {
        await adminAPI.deleteSubject(subjectId)
        // Remove the subject from the local array
        this.subjects = this.subjects.filter(s => s.id !== subjectId)
        this.$store.dispatch('showAlert', {
          type: 'success',
          message: 'Subject deleted successfully'
        })
      } catch (error) {
        console.error('Error deleting subject:', error)
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to delete subject'
        })
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    },
    // Debug method - remove after testing
    async testAPI() {
      console.log('Testing API calls...')
      try {
        const response = await adminAPI.getSubjects()
        console.log('Direct API call result:', response.data)
      } catch (error) {
        console.error('Direct API call error:', error)
      }
    }
  }
}
</script>
