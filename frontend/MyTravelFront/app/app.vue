<script setup lang="js">
  import { ref, onMounted } from 'vue'

  const coords = ref(null)

  onMounted(() => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          coords.value = {
            lat: position.coords.latitude,
            lng: position.coords.longitude
          }
          // Send to backend
          sendLocation(coords.value)
        },
        (error) => {
          console.error("Error getting location:", error)
        }
      )
    } else {
      console.error("Geolocation not supported")
    }
  })

  // function to send location to backend
  async function sendLocation({ lat, lng }) {
    try {
      const res = await $fetch('/api/location', {
        method: 'POST',
        body: { lat, lng }
      })
      console.log('Location saved:', res)
    } catch (e) {
      console.error('Failed to send location:', e)
    }
  }

  const { data, pending, error } = await useFetch("http://localhost:3000/businesses")
</script>

<template>
  <div class="wrapper">
    <div class="navbar">
      <div class="nav">
        <p>Map</p>
      </div>
      <div class="nav">
        <p></p>
      </div>
      <div class="nav">
        <p>Map</p>
      </div>
    </div>

    <div class="">

    </div>
    <div>
      <h2>User Location</h2>
      <p v-if="coords">📍 Lat: {{ coords.lat }}, Lng: {{ coords.lng }}</p>
      <p v-else>Fetching location...</p>
    </div>  
  </div>
  <div>
    <h2>📍 User Locations</h2>
    <div v-if="error">❌ Failed to load: {{ error.message }}</div>
    <div v-else-if="pending">⏳ Loading...</div>
    <ul v-else>
      <li v-for="loc in data.data" :key="loc.id">
        ID: {{ loc.id }} — Lat: {{ loc.lat }}, Lng: {{ loc.lng }}
      </li>
    </ul>
  </div>
</template>

<style scoped>

</style>