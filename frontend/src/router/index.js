import { createRouter, createWebHistory } from 'vue-router'
import store from '../store'

// Auth Views (keep in main bundle for faster initial load)
import AuthView from '../views/AuthView.vue'

// User Views - Lazy load non-critical views
import UserDashboard from '../views/user/Dashboard.vue'
const UserQuizzes = () => import('../views/user/Quizzes.vue')
const UserScores = () => import('../views/user/Scores.vue')
const UserProfile = () => import('../views/user/Profile.vue')
const QuizAttempt = () => import('../views/user/QuizAttempt.vue')
const QuizResults = () => import('../views/user/QuizResults.vue')

// Admin Views - Lazy load admin views
const AdminDashboard = () => import('../views/admin/Dashboard.vue')
const AdminSubjects = () => import('../views/admin/Subjects.vue')
const AdminChapters = () => import('../views/admin/Chapters.vue')
const AdminQuizzes = () => import('../views/admin/Quizzes.vue')
const AdminUsers = () => import('../views/admin/Users.vue')
const AdminQuestions = () => import('../views/admin/Questions.vue')

const routes = [
  {
    path: '/',
    redirect: '/auth'
  },
  {
    path: '/auth',
    name: 'Auth',
    component: AuthView,
    meta: { requiresAuth: false, requiresSidebar: false }
  },
  
  // User Routes
  {
    path: '/user',
    meta: { requiresAuth: true, role: 'user' },
    children: [
      {
        path: 'dashboard',
        name: 'UserDashboard',
        component: UserDashboard
      },
      {
        path: 'quizzes',
        name: 'UserQuizzes',
        component: UserQuizzes
      },
      {
        path: 'scores',
        name: 'UserScores',
        component: UserScores
      },
      {
        path: 'profile',
        name: 'UserProfile',
        component: UserProfile
      },
      {
        path: 'quiz/:id',
        name: 'QuizAttempt',
        component: QuizAttempt,
        meta: { requiresSidebar: false }
      },
      {
        path: 'quiz/:id/results',
        name: 'QuizResults',
        component: QuizResults,
        meta: { requiresSidebar: false }
      }
    ]
  },
  
  // Admin Routes
  {
    path: '/admin',
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: AdminDashboard
      },
      {
        path: 'subjects',
        name: 'AdminSubjects',
        component: AdminSubjects
      },
      {
        path: 'chapters',
        name: 'AdminChapters',
        component: AdminChapters
      },
      {
        path: 'quizzes',
        name: 'AdminQuizzes',
        component: AdminQuizzes
      },
      {
        path: 'quiz/:id/questions',
        name: 'AdminQuestions',
        component: AdminQuestions
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers
      }
    ]
  },
  
  // Catch all 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters['auth/isAuthenticated']
  const userRole = store.getters['auth/userRole']
  
  // Check if route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next('/auth')
      return
    }
    
    // Check role-based access
    if (to.meta.role && to.meta.role !== userRole) {
      // Redirect to appropriate dashboard based on role
      if (userRole === 'admin') {
        next('/admin/dashboard')
      } else {
        next('/user/dashboard')
      }
      return
    }
  }
  
  // Redirect authenticated users away from auth page
  if (to.name === 'Auth' && isAuthenticated) {
    if (userRole === 'admin') {
      next('/admin/dashboard')
    } else {
      next('/user/dashboard')
    }
    return
  }
  
  next()
})

export default router
