<template>
  <div class="admin-questions p-3 p-md-4">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-section bg-primary text-white p-4 rounded shadow-sm d-flex justify-content-between align-items-center">
            <div>
              <p class="mb-0 opacity-75">In {{ quizName }} Quiz</p>
            </div>
            <button class="btn btn-outline-light btn-lg px-4" style="font-size:1.1rem;">
              Questions Added: {{ questions.length }}
            </button>
          </div>
        </div>
      </div>
      <!-- Add Question Form -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-body">
              <div class="d-flex align-items-center mb-3 mt-2 gap-3 flex-wrap">
                <h5 class="mb-0">Question Number: {{ questions.length + 1 }}</h5>
              </div>
              <div style="height:18px;"></div>
              <div class="d-flex align-items-center mb-3 mt-2 gap-3 flex-wrap">
                <div class="d-flex align-items-center gap-2">
                  <label class="form-label mb-0" style="min-width:60px;">Marks</label>
                  <input v-model.number="form.marks" type="number" class="form-control form-control-sm" min="1" required style="width:80px;" placeholder="Marks" />
                </div>
                <div class="d-flex align-items-center gap-2">
                  <label class="form-label mb-0" style="min-width:80px;">-Ve Marks</label>
                  <input v-model.number="form.negative_marks" type="number" class="form-control form-control-sm" :min="-100" :max="0" required style="width:80px;" placeholder="-Ve" />
                </div>
                <div class="d-flex align-items-center gap-2">
                  <label class="form-label mb-0" style="min-width:40px;">Type</label>
                  <select v-model="form.type" class="form-select form-select-sm" required style="width:130px;">
                    <option value="single">Single type</option>
                    <option value="multiple">Multiple select</option>
                  </select>
                </div>
              </div>
              <form @submit.prevent="addQuestion">
                <div class="mb-3">
                  <label class="form-label">Question Text</label>
                  <textarea v-model="form.text" class="form-control" rows="2" required></textarea>
                </div>
                <div class="mb-3">
                  <label class="form-label">Answer Options</label>
                  <div class="row g-2 mb-3">
                    <div v-for="(option, idx) in form.options" :key="idx" class="col-md-6">
                      <div class="input-group">
                        <span class="input-group-text">
                          <template v-if="form.type === 'single'">
                            <input type="radio" :checked="form.correct === idx" @change="form.correct = idx" />
                          </template>
                          <template v-else>
                            <input type="checkbox" :checked="form.correctMultiple.includes(idx)" @change="toggleCorrectMultiple(idx)" />
                          </template>
                        </span>
                        <input v-model="form.options[idx]" type="text" class="form-control" required placeholder="Option" style="width:120px;" />
                        <button type="button" class="btn btn-outline-danger" @click="removeOption(idx)">Remove</button>
                      </div>
                    </div>
                  </div>
                  <div class="d-flex justify-content-between mt-4 mb-2">
                    <button type="button" class="btn btn-primary" style="background-color:#2563eb;border-color:#2563eb;" @click="addOption">+ Add Option</button>
                    <button type="submit" class="btn btn-success">Add Question</button>
                  </div>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
      <!-- Questions List -->
      <div class="row">
        <div class="col-12">
          <div class="card shadow-sm">
            <div class="card-body">
              <h5 class="mb-3">All Questions</h5>
              <div v-if="loading" class="text-center py-4">
                <div class="spinner-border text-primary" role="status"></div>
              </div>
              <div v-else>
                <table class="table table-bordered table-hover align-middle" style="table-layout:fixed;">
                  <thead class="table-light text-center">
                    <tr>
                      <th style="width:50px;">#</th>
                      <th style="width:260px;">Question</th>
                      <th style="width:220px;">Options</th>
                      <th style="width:60px;">Marks</th>
                      <th style="width:70px;">-Ve Marks</th>
                      <th style="width:80px;">Type</th>
                      <th style="width:110px;">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(question, idx) in questions" :key="question.id">
                      <td class="text-center">{{ idx + 1 }}</td>
                      <td style="max-width:260px;white-space:pre-line;word-break:break-word;">
                        {{ question.question_statement }}
                      </td>
                      <td style="max-width:220px;">
                        <table class="w-100" style="border-collapse:collapse;">
                          <tr>
                            <td style="border-right:1px solid #ddd;vertical-align:top;padding:0 6px;">
                              <div class="form-check">
                                <template v-if="question.options[0]">
                                  <template v-if="question.type === 'single'">
                                    <input class="form-check-input" type="radio" :checked="question.correct_answer == 1" disabled />
                                    <label class="form-check-label" :class="{'fw-bold text-success': question.correct_answer == 1}">{{ question.options[0] }}</label>
                                  </template>
                                  <template v-else>
                                    <input class="form-check-input" type="checkbox" :checked="question.correct_answers && question.correct_answers.includes(1)" disabled />
                                    <label class="form-check-label" :class="{'fw-bold text-success': question.correct_answers && question.correct_answers.includes(1)}">{{ question.options[0] }}</label>
                                  </template>
                                </template>
                              </div>
                            </td>
                            <td style="vertical-align:top;padding:0 6px;">
                              <div class="form-check">
                                <template v-if="question.options[1]">
                                  <template v-if="question.type === 'single'">
                                    <input class="form-check-input" type="radio" :checked="question.correct_answer == 2" disabled />
                                    <label class="form-check-label" :class="{'fw-bold text-success': question.correct_answer == 2}">{{ question.options[1] }}</label>
                                  </template>
                                  <template v-else>
                                    <input class="form-check-input" type="checkbox" :checked="question.correct_answers && question.correct_answers.includes(2)" disabled />
                                    <label class="form-check-label" :class="{'fw-bold text-success': question.correct_answers && question.correct_answers.includes(2)}">{{ question.options[1] }}</label>
                                  </template>
                                </template>
                              </div>
                            </td>
                          </tr>
                          <tr>
                            <td style="border-right:1px solid #ddd;vertical-align:top;padding:0 6px;">
                              <div class="form-check">
                                <template v-if="question.options[2]">
                                  <template v-if="question.type === 'single'">
                                    <input class="form-check-input" type="radio" :checked="question.correct_answer == 3" disabled />
                                    <label class="form-check-label" :class="{'fw-bold text-success': question.correct_answer == 3}">{{ question.options[2] }}</label>
                                  </template>
                                  <template v-else>
                                    <input class="form-check-input" type="checkbox" :checked="question.correct_answers && question.correct_answers.includes(3)" disabled />
                                    <label class="form-check-label" :class="{'fw-bold text-success': question.correct_answers && question.correct_answers.includes(3)}">{{ question.options[2] }}</label>
                                  </template>
                                </template>
                              </div>
                            </td>
                            <td style="vertical-align:top;padding:0 6px;">
                              <div class="form-check">
                                <template v-if="question.options[3]">
                                  <template v-if="question.type === 'single'">
                                    <input class="form-check-input" type="radio" :checked="question.correct_answer == 4" disabled />
                                    <label class="form-check-label" :class="{'fw-bold text-success': question.correct_answer == 4}">{{ question.options[3] }}</label>
                                  </template>
                                  <template v-else>
                                    <input class="form-check-input" type="checkbox" :checked="question.correct_answers && question.correct_answers.includes(4)" disabled />
                                    <label class="form-check-label" :class="{'fw-bold text-success': question.correct_answers && question.correct_answers.includes(4)}">{{ question.options[3] }}</label>
                                  </template>
                                </template>
                              </div>
                            </td>
                          </tr>
                        </table>
                      </td>
                      <td class="text-center" style="width:60px;">{{ question.marks }}</td>
                      <td class="text-center" style="width:70px;">{{ question.negative_marks }}</td>
                      <td class="text-center" style="width:80px;">{{ question.type === 'multiple' ? 'Multiple' : 'Single' }}</td>
                      <td class="text-center" style="width:110px;">
                        <div class="d-flex flex-column align-items-center gap-2">
                          <button class="btn btn-sm btn-warning w-100" style="min-width:80px;" @click="openEditModal(question)"><i class="fas fa-edit"></i> Edit</button>
                          <button class="btn btn-sm btn-danger w-100" style="min-width:80px;" @click="deleteQuestion(question.id)"><i class="fas fa-trash"></i> Delete</button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
                <div v-if="questions.length === 0" class="text-center text-muted py-4">
                  <i class="fas fa-question-circle fa-3x mb-3 opacity-50"></i>
                  <p>No questions found for this quiz.</p>
                </div>
              </div>
              <!-- Edit Modal -->
              <div v-if="editModalOpen" class="modal fade show" style="display:block;background:rgba(0,0,0,0.3);">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title">Edit Question</h5>
                      <button type="button" class="btn-close" @click="closeEditModal"></button>
                    </div>
                    <div class="modal-body">
                      <form @submit.prevent="saveEdit">
                        <div class="mb-2">
                          <label class="form-label">Question Text</label>
                          <textarea v-model="editForm.text" class="form-control" rows="2" required></textarea>
                        </div>
                        <div class="mb-2">
                          <label class="form-label">Marks</label>
                          <input v-model.number="editForm.marks" type="number" class="form-control" min="1" required />
                        </div>
                        <div class="mb-2">
                          <label class="form-label">-Ve Marks</label>
                          <input v-model.number="editForm.negative_marks" type="number" class="form-control" :min="-100" :max="0" required />
                        </div>
                        <div class="mb-2">
                          <label class="form-label">Type</label>
                          <select v-model="editForm.type" class="form-select" required>
                            <option value="single">Single type</option>
                            <option value="multiple">Multiple select</option>
                          </select>
                        </div>
                        <div class="mb-2">
                          <label class="form-label">Answer Options</label>
                          <div v-for="(option, idx) in editForm.options" :key="idx" class="input-group mb-1">
                            <span class="input-group-text">
                              <template v-if="editForm.type === 'single'">
                                <input type="radio" :checked="editForm.correct === idx" @change="editForm.correct = idx" />
                              </template>
                              <template v-else>
                                <input type="checkbox" :checked="editForm.correctMultiple.includes(idx)" @change="toggleEditCorrectMultiple(idx)" />
                              </template>
                            </span>
                            <input v-model="editForm.options[idx]" type="text" class="form-control" required />
                          </div>
                        </div>
                        <div class="d-flex justify-content-end mt-3">
                          <button type="button" class="btn btn-secondary me-2" @click="closeEditModal">Cancel</button>
                          <button type="submit" class="btn btn-success">Save</button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
              <!-- End Edit Modal -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { adminAPI } from '@/services/api'

export default {
  name: 'AdminQuestions',
  data() {
    return {
      questions: [],
      loading: true,
      form: {
        text: '',
        marks: 1,
        negative_marks: 0,
        type: 'single',
        options: ['', ''],
        correct: 0,
        correctMultiple: []
      },
      editModalOpen: false,
      editForm: {
        id: null,
        text: '',
        marks: 1,
        negative_marks: 0,
        type: 'single',
        options: ['', ''],
        correct: 0,
        correctMultiple: []
      },
      quizName: ''
    }
  },
  mounted() {
    this.quizId = this.$route.params.id;
    this.loadQuestions();
    this.loadQuizName();
  },
  methods: {
    async loadQuestions() {
      this.loading = true
      try {
        const response = await adminAPI.getQuizQuestions(this.quizId)
        this.questions = response.data.questions || []
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load questions.'
        })
      } finally {
        this.loading = false
      }
    },
    async loadQuizName() {
      try {
        const response = await adminAPI.getQuiz(this.quizId)
        this.quizName = response.data.title || ''
      } catch {
        this.quizName = ''
      }
    },
    async addQuestion() {
      try {
        if (this.form.options.length !== 4) {
          this.$store.dispatch('showAlert', {
            type: 'error',
            message: 'Exactly 4 options are required.'
          })
          return
        }
        let payload = {
          text: this.form.text,
          marks: this.form.marks,
          negative_marks: this.form.negative_marks,
          type: this.form.type,
          options: this.form.options
        }
        if (this.form.type === 'single') {
          payload.correct = this.form.correct
        } else {
          if (this.form.correctMultiple.length === 0) {
            this.$store.dispatch('showAlert', {
              type: 'error',
              message: 'Select at least one correct answer.'
            })
            return
          }
          payload.correctMultiple = this.form.correctMultiple
        }
        await adminAPI.createQuestion(this.quizId, payload)
        this.form = { text: '', marks: 1, negative_marks: 0, type: 'single', options: ['', ''], correct: 0, correctMultiple: [] }
        this.loadQuestions()
        this.$store.dispatch('showAlert', {
          type: 'success',
          message: 'Question added.'
        })
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to add question.'
        })
      }
    },
    async deleteQuestion(id) {
      if (!confirm('Delete this question?')) return
      try {
        await adminAPI.deleteQuestion(id)
        this.loadQuestions()
        this.$store.dispatch('showAlert', {
          type: 'success',
          message: 'Question deleted.'
        })
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to delete question.'
        })
      }
    },
    openEditModal(question) {
      this.editForm = {
        id: question.id,
        text: question.question_statement,
        marks: question.marks,
        negative_marks: question.negative_marks,
        type: question.type,
        options: question.options.slice(),
        correct: question.type === 'single' ? (question.correct_answer - 1) : 0,
        correctMultiple: question.type === 'multiple' ? (question.correct_answers ? question.correct_answers.map(i => i - 1) : []) : []
      }
      this.editModalOpen = true
    },
    closeEditModal() {
      this.editModalOpen = false
    },
    toggleEditCorrectMultiple(idx) {
      const i = this.editForm.correctMultiple.indexOf(idx)
      if (i === -1) {
        this.editForm.correctMultiple.push(idx)
      } else {
        this.editForm.correctMultiple.splice(i, 1)
      }
    },
    async saveEdit() {
      try {
        if (this.editForm.options.length !== 4) {
          this.$store.dispatch('showAlert', {
            type: 'error',
            message: 'Exactly 4 options are required.'
          })
          return
        }
        let payload = {
          text: this.editForm.text,
          marks: this.editForm.marks,
          negative_marks: this.editForm.negative_marks,
          type: this.editForm.type,
          options: this.editForm.options
        }
        if (this.editForm.type === 'single') {
          payload.correct = this.editForm.correct
        } else {
          if (this.editForm.correctMultiple.length === 0) {
            this.$store.dispatch('showAlert', {
              type: 'error',
              message: 'Select at least one correct answer.'
            })
            return
          }
          payload.correctMultiple = this.editForm.correctMultiple
        }
        await adminAPI.updateQuestion(this.editForm.id, payload)
        this.closeEditModal()
        this.loadQuestions()
        this.$store.dispatch('showAlert', {
          type: 'success',
          message: 'Question updated.'
        })
      } catch (error) {
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to update question.'
        })
      }
    },
    addOption() {
      if (this.form.options.length < 4) {
        this.form.options.push('')
      }
    },
    removeOption(idx) {
      if (this.form.options.length > 2) {
        this.form.options.splice(idx, 1)
        if (this.form.type === 'single' && this.form.correct >= this.form.options.length) {
          this.form.correct = 0
        }
        if (this.form.type === 'multiple') {
          this.form.correctMultiple = this.form.correctMultiple.filter(i => i < this.form.options.length)
        }
      }
    },
    toggleCorrectMultiple(idx) {
      const i = this.form.correctMultiple.indexOf(idx)
      if (i === -1) {
        this.form.correctMultiple.push(idx)
      } else {
        this.form.correctMultiple.splice(i, 1)
      }
    }
  }
}
</script>
