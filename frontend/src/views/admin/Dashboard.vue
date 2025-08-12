<template>
  <div class="admin-dashboard p-3 p-md-4">
    <div class="container-fluid">
      <!-- Header -->
      <div class="row mb-4">
        <div class="col-12">
          <div class="welcome-section bg-primary text-white p-4 rounded shadow-sm d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Admin Dashboard</h2>
              <p class="mb-0 opacity-75">Manage your quiz platform efficiently</p>
            </div>
                  <div class="d-flex align-items-center gap-2">
                    <button class="btn btn-light text-primary fw-bold d-flex align-items-center" @click="downloadUserReport">
                      <i class="fas fa-download me-2"></i> User Report
                    </button>
                  </div>
          </div>
        </div>
      </div>

      <!-- Stats Overview -->
      <div class="row g-3 g-lg-4 mb-4">
        <div class="col-xl-3 col-md-6">
          <!-- FIX: Used bg-primary-subtle and text-primary-emphasis for better visibility -->
          <div class="stats-card card h-100 bg-primary-subtle text-primary-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <!-- FIX: Reduced font size for better fit -->
                <h3 class="mb-0 h2">{{ stats.totalUsers }}</h3>
                <p class="mb-0">Total Users</p>
              </div>
              <i class="fas fa-users fa-3x opacity-50"></i>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-success-subtle text-success-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2">{{ stats.totalQuizzes }}</h3>
                <p class="mb-0">Total Quizzes</p>
              </div>
              <i class="fas fa-clipboard-list fa-3x opacity-50"></i>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-info-subtle text-info-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2">{{ stats.totalSubjects }}</h3>
                <p class="mb-0">Subjects</p>
              </div>
              <i class="fas fa-book fa-3x opacity-50"></i>
            </div>
          </div>
        </div>

        <div class="col-xl-3 col-md-6">
          <div class="stats-card card h-100 bg-warning-subtle text-warning-emphasis">
            <div class="card-body d-flex justify-content-between align-items-center p-3">
              <div>
                <h3 class="mb-0 h2">{{ stats.totalAttempts }}</h3>
                <p class="mb-0">Quiz Attempts</p>
              </div>
              <i class="fas fa-chart-line fa-3x opacity-50"></i>
            </div>
          </div>
        </div>
      </div>

      <!-- Charts Row (No Quick Actions) -->
      <div class="row g-4">
        <!-- Quiz Attempts Chart -->
        <div class="col-lg-12">
          <div class="card h-100">
            <div class="card-header">
              <h5 class="mb-0">Quiz Attempts Over Time</h5>
            </div>
            <div class="card-body d-flex align-items-center justify-content-center">
              <canvas id="attemptsChart"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Using Chart.js for summary charts as required by the project doc
import { Chart, registerables } from 'chart.js';
// NOTE: Assuming your API service is correctly configured at @/services/api
import { adminAPI } from '@/services/api';

Chart.register(...registerables);

export default {
  name: 'AdminDashboard',
  data() {
    return {
      stats: {
        totalUsers: 0,
        totalQuizzes: 0,
        totalSubjects: 0,
        totalAttempts: 0
      },
      chartData: null,
      attemptsChart: null,
      loading: true
    };
  },
  computed: {
    user() {
      return this.$store.state.auth.user;
    }
  },
  async mounted() {
    // Load only the necessary data for the dashboard
    await this.loadDashboardData();
    // Initialize charts after data is loaded
    if (this.chartData) {
      this.initializeCharts();
    }
  },
  beforeUnmount() {
    // Clean up the chart instance to prevent memory leaks
    if (this.attemptsChart) {
      this.attemptsChart.destroy();
    }
  },
  methods: {
    async loadDashboardData() {
      try {
        this.loading = true;
        // Fetch only the stats and chart data required for the simplified dashboard
        const [statsResponse, chartResponse] = await Promise.all([
          adminAPI.getDashboardStats(), // Assuming an endpoint like this exists
          adminAPI.getChartData()      // Assuming an endpoint like this exists
        ]);

        this.stats = statsResponse.data;
        this.chartData = chartResponse.data;

      } catch (error) {
        console.error('Error loading dashboard data:', error);
        // Dispatch a global alert for user feedback
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to load dashboard data. Please try again later.'
        });
      } finally {
        this.loading = false;
      }
    },
            downloadUserReport() {
              // TODO: Implement user report download logic
              alert('User Report download triggered!');
            },
    initializeCharts() {
      // Use $nextTick to ensure the canvas element is rendered before creating the chart
      this.$nextTick(() => {
        this.createAttemptsChart();
      });
    },
    createAttemptsChart() {
      const ctx = document.getElementById('attemptsChart');
      if (!ctx || !this.chartData) return;

      // Destroy previous chart instance if it exists
      if (this.attemptsChart) {
        this.attemptsChart.destroy();
      }

      this.attemptsChart = new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.chartData.labels || [],
          datasets: [{
            label: 'Quiz Attempts',
            data: this.chartData.attempts || [],
            borderColor: '#007bff',
            backgroundColor: 'rgba(0, 123, 255, 0.1)',
            fill: true,
            tension: 0.3
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false
            }
          },
          scales: {
            y: {
              beginAtZero: true,
              grid: {
                color: 'rgba(0,0,0,0.05)'
              }
            },
            x: {
              grid: {
                display: false
              }
            }
          }
        }
      });
    },
    async generateReport() {
      // This function can trigger the CSV export as required by the project doc
      this.$store.dispatch('showAlert', {
        type: 'info',
        message: 'Generating user report...'
      });
      try {
        // Assuming you have an API endpoint for this
        const response = await adminAPI.exportUsers();
        // Create a downloadable link for the CSV file
        const blob = new Blob([response.data], { type: 'text/csv' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `user-report-${new Date().toISOString().split('T')[0]}.csv`;
        link.click();
        URL.revokeObjectURL(link.href);
        this.$store.dispatch('showAlert', {
          type: 'success',
          message: 'Report downloaded successfully!'
        });
      } catch (error) {
        console.error('Error generating report:', error);
        this.$store.dispatch('showAlert', {
          type: 'error',
          message: 'Failed to generate report.'
        });
      }
    },
    logout() {
      this.$store.dispatch('auth/logout').then(() => {
        this.$router.push('/auth');
      });
    }
  }
};
</script>

<style scoped>
.stats-card {
  border: none;
  border-radius: 0.5rem;
  transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
}

.stats-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.1);
}

.card {
  border: none;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.card-header {
  background-color: transparent;
  border-bottom: 1px solid #dee2e6;
}
</style>
