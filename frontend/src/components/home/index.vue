<script setup>
import { ref } from 'vue'
import Header from './Header.vue'
import FoodList from './FoodList.vue'

const selectedLocation = ref(null)
const searchQuery = ref('')
</script>

<template>
  <div class="app">
    <Header 
      v-model:selectedLocation="selectedLocation"
      v-model:searchQuery="searchQuery"
    />
    <main>
      <FoodList 
        :selectedLocation="selectedLocation"
        :searchQuery="searchQuery"
      />
    </main>
  </div>
</template>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  background-color: #f8f9fa;
}

.app {
  min-height: 100vh;
}

main {
  width: 100%;
  margin: 0 auto;
  /* padding: 2rem; */
}
</style>
