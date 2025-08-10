import axios from 'axios';

const BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000/api';

// Create axios instance
const api = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/auth';
    }
    return Promise.reject(error);
  }
);

export default api;

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  register: (userData) => api.post('/auth/register', userData),
  verifyToken: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout')
};

// User API
export const userAPI = {
  getDashboard: () => api.get('/user/dashboard'),
  getQuizzes: () => api.get('/user/quizzes'),
  getSubjects: () => api.get('/user/subjects'),
  getScores: (params = {}) => api.get('/user/scores', { params }),
  getProfile: () => api.get('/user/profile'),
  updateProfile: (data) => api.put('/user/profile', data)
};

// Quiz API
export const quizAPI = {
  getQuizDetails: (id) => api.get(`/quiz/${id}/details`),
  startQuiz: (id) => api.get(`/quiz/${id}/start`),
  submitQuiz: (id, data) => api.post(`/quiz/${id}/submit`, data),
  getQuizAttempt: (scoreId) => api.get(`/quiz/attempt/${scoreId}`)
};

// Admin API
export const adminAPI = {
  // --- CORRECTED: Dashboard Endpoints ---
  getDashboardStats: () => api.get('/admin/dashboard/stats'),
  getChartData: () => api.get('/admin/dashboard/chart-data'),
  exportUsers: () => api.get('/admin/users/export', { responseType: 'blob' }),

  // Subjects
  getSubjects: () => api.get('/admin/subjects'),
  createSubject: (data) => api.post('/admin/subjects', data),
  updateSubject: (id, data) => api.put(`/admin/subjects/${id}`, data),
  deleteSubject: (id) => api.delete(`/admin/subjects/${id}`),

  // Chapters
  getChapters: () => api.get('/admin/chapters'),
  createChapter: (data) => api.post('/admin/chapters', data),
  updateChapter: (id, data) => api.put(`/admin/chapters/${id}`, data),
  deleteChapter: (id) => api.delete(`/admin/chapters/${id}`),

  // Quizzes
  getQuizzes: () => api.get('/admin/quizzes'),
  createQuiz: (data) => api.post('/admin/quizzes', data),
  updateQuiz: (id, data) => api.put(`/admin/quizzes/${id}`, data),
  deleteQuiz: (id) => api.delete(`/admin/quizzes/${id}`),

  // Questions
  getQuizQuestions: (quizId) => api.get(`/admin/quizzes/${quizId}/questions`),
  createQuestion: (quizId, data) => api.post(`/admin/quizzes/${quizId}/questions`, data),
  updateQuestion: (id, data) => api.put(`/admin/questions/${id}`, data),
  deleteQuestion: (id) => api.delete(`/admin/questions/${id}`),

  // Users
  getUsers: () => api.get('/admin/users')
};
