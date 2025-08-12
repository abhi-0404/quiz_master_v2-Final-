<template>
  <div class="user-dashboard">
    <div class="container-fluid">
      <!-- Header Section -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-card bg-primary text-white p-4 rounded d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-0">Welcome back, {{ user?.full_name }}!</h2>
              <p class="mb-0 opacity-75">Ready to challenge yourself with some quizzes?</p>
            </div>
            <div class="dropdown">
              <button class="btn btn-outline-light dropdown-toggle" type="button" id="userDropdown" data-bs-toggle="dropdown" aria-expanded="false">
                {{ user?.full_name || 'User' }}
              </button>
              <ul class="dropdown-menu dropdown-menu-end" aria-labelledby="userDropdown">
                <li>
                  <a class="dropdown-item" href="#" @click.prevent="logout">
                    <i class="fas fa-sign-out-alt me-2"></i> Logout
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row g-3 g-lg-4 mb-4">
        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-primary-subtle text-primary-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2 fw-bold">{{ stats.quizzes_taken }}</h3>
                <p class="mb-0">Quizzes Taken</p>
              </div>
              <i class="fas fa-check-circle fa-3x opacity-50"></i>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-success-subtle text-success-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2 fw-bold">{{ stats.average_score }}%</h3>
                <p class="mb-0">Average Score</p>
              </div>
              <i class="fas fa-percentage fa-3x opacity-50"></i>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-info-subtle text-info-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2 fw-bold">{{ stats.best_score }}%</h3>
                <p class="mb-0">Best Score</p>
              </div>
              <i class="fas fa-trophy fa-3x opacity-50"></i>
            </div>
          </div>
        </div>
        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-warning-subtle text-warning-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2 fw-bold">{{ stats.total_questions_answered }}</h3>
                <p class="mb-0">Questions Answered</p>
              </div>
              <i class="fas fa-question-circle fa-3x opacity-50"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Graphs Section -->
      <div class="row g-4 mb-4">
        <div class="col-12">
          <div class="card h-100">
            <div class="card-header">
              <h5 class="mb-0">Performance Over Time</h5>
              <p class="mb-0 text-muted small">Your scores on the last 10 quizzes</p>
            </div>
            <div class="card-body">
              <div v-if="loading" class="text-center">
                  <div class="spinner-border text-primary" role="status"></div>
              </div>
              <canvas v-else id="performanceChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import { userAPI } from '@/services/api';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'UserDashboard',
  data() {
    return {
      stats: {
        quizzes_taken: 0,
        average_score: 0,
        best_score: 0,
        total_questions_answered: 0
      },
      loading: true,
      performanceChart: null,
    };
  },
  computed: {
    ...mapState('auth', ['user'])
  },
  methods: {
    async loadDashboardData() {
      try {
        this.loading = true;
        const [statsResponse, graphResponse] = await Promise.all([
          userAPI.getDashboardStats(),
          userAPI.getDashboardGraphData()
        ]);
        
        this.stats = statsResponse.data.stats;
        this.createPerformanceChart(graphResponse.data);

      } catch (error) {
        console.error('Error loading dashboard data:', error);
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load dashboard data.'
        });
      } finally {
        this.loading = false;
      }
    },
    createPerformanceChart(graphData) {
      this.$nextTick(() => {
        const ctx = document.getElementById('performanceChart');
        if (!ctx) return;

        if (this.performanceChart) {
          this.performanceChart.destroy();
        }

        this.performanceChart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: graphData.labels,
            datasets: [{
              label: 'Score (%)',
              data: graphData.data,
              borderColor: '#007bff',
              backgroundColor: 'rgba(0, 123, 255, 0.1)',
              fill: true,
              tension: 0.3
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              y: {
                beginAtZero: true,
                max: 100,
                ticks: {
                  callback: function(value) {
                    return value + '%'
                  }
                }
              }
            }
          }
        });
      });
    },
    logout() {
      this.$store.dispatch('auth/logout').then(() => {
        this.$router.push('/auth');
      });
    }
  },
  async mounted() {
    await this.loadDashboardData();
  },
  beforeUnmount() {
    if (this.performanceChart) {
      this.performanceChart.destroy();
    }
  }
};
</script>

<style scoped>
.user-dashboard {
  padding: 20px 0;
}
.welcome-card {
  background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
  border: none;
}
.stats-card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.075);
  transition: transform 0.2s;
}
.stats-card:hover {
  transform: translateY(-3px);
}
.card {
  border: none;
  box-shadow: 0 2px 10px rgba(0,0,0,0.075);
}
.card-header {
  background-color: #fff;
  border-bottom: 1px solid #dee2e6;
}
</style>
