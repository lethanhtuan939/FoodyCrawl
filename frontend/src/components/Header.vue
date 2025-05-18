<script setup>
import { ref, computed, defineModel } from 'vue'
import { useDebounceFn } from '@vueuse/core'

const locations = ref([])
const searchInput = ref('')
const selectedLocation = defineModel('selectedLocation', {
  type: Object,
  default: null
})
const searchQuery = defineModel('searchQuery', {
  type: String,
  default: ''
})

const debouncedSearch = useDebounceFn((value) => {
  searchQuery.value = value
}, 500)

function handleSearch(e) {
  searchInput.value = e.target.value
  debouncedSearch(e.target.value)
}

async function fetchLocations() {
  try {
    const response = await fetch('http://localhost:8000/locations')
    locations.value = await response.json()
  } catch (error) {
    console.error('Error fetching locations:', error)
  }
}

const locationGroups = computed(() => {
  const groups = []
  locations.value.forEach(location => {
    const index = groups.findIndex(group => group.country_name === location.country_name)
    if (index === -1) {
      groups.push({
        country_name: location.country_name,
        locations: [location]
      })
    } else {
      groups[index].locations.push(location)
    }
  })
  return groups
})

fetchLocations()
</script>

<template>
  <header class="header">
    <div class="logo">
      <h1>Foody Crawl</h1>
    </div>
    <div class="filter">
      <div class="search-box">
        <input 
          type="text" 
          :value="searchInput"
          @input="handleSearch"
          placeholder="Tìm kiếm món ăn..."
        >
      </div>
      <div class="location-selector">
        <select v-model="selectedLocation">
          <option :value="null" disabled selected hidden>Chọn địa điểm</option>
          <option value="all">Mọi nơi</option>
          <optgroup v-for="group in locationGroups" :key="group.country_name" :label="group.country_name">
            <option v-for="location in group.locations" :key="location.id" :value="location">
            {{ location.name }}
          </option>
          </optgroup>
        </select>
      </div>
    </div>
  </header>
</template>

<style scoped>
.header {
  overflow-y: auto;
  position: sticky;
  top: 0;
  left: 0;
  z-index: 1000;
  display: flex;
  gap: 2rem;
  align-items: center;
  padding: 1rem 4rem;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

.logo h1 {
  color: #ff5a5f;
  margin: 0;
  font-size: 2rem;
}

.filter {
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-grow: 1;
  justify-content: flex-end;
}

.search-box {
  position: relative;
}

.search-box input {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  outline: none;
  min-width: 300px;
}

.search-box input::placeholder {
  color: #bbb;
}

.search-box input:focus {
  border-color: #ff5a5f;
  box-shadow: 0 0 0 2px rgba(255, 90, 95, 0.1);
}

.location-selector select {
  padding: 0.5rem 1rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  outline: none;
  cursor: pointer;
}

.location-selector select:hover {
  border-color: #ff5a5f;
}
</style>
