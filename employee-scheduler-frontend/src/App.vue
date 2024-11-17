<script setup>
</script>

<template>
      
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid w-100">
      <a class="navbar-brand" href="#">Employee Scheduler</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <RouterLink class="nav-link" to="/">Home</RouterLink>
          <RouterLink class="nav-link" to="/employees">Employees</RouterLink>
          <RouterLink class="nav-link" to="/schedules">Schedules</RouterLink>
        </div>
      </div>
    </div>
  </nav>
  <main class="container">
    <RouterView />
  </main>
</template>

<style scoped>
</style>
