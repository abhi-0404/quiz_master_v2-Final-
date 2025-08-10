<template>
  <div class="loading-overlay">
    <div class="loading-spinner">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="loading-text mt-3">Loading...</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LoadingOverlay'
}
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9998;
  backdrop-filter: blur(2px);
}

.loading-spinner {
  text-align: center;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}

.loading-text {
  color: var(--primary-color);
  font-weight: 500;
  margin: 0;
}
</style>
