<template>
  <div class="not-found">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 text-center">
          <div class="error-content">
            <h1 class="display-1 text-primary">404</h1>
            <h2 class="mb-3">Page Not Found</h2>
            <p class="text-muted mb-4">
              The page you're looking for doesn't exist or has been moved.
            </p>
            <div class="actions">
              <router-link to="/" class="btn btn-primary me-3">
                <i class="fas fa-home me-2"></i>
                Go Home
              </router-link>
              <button @click="goBack" class="btn btn-outline-secondary">
                <i class="fas fa-arrow-left me-2"></i>
                Go Back
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
  methods: {
    goBack() {
      this.$router.go(-1)
    }
  }
}
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #f8f9fa;
}

.error-content {
  padding: 2rem;
}

.display-1 {
  font-size: 8rem;
  font-weight: bold;
}
</style>
