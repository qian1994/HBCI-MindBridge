<template>
  <div id="app">
    <Header></Header>
    <router-view />
  </div>
</template>
<script>
import { initDevTools } from './api/index'
import Header from './Components/Header/index.vue'
export default {
  methods: {
  },
  created() {
    
  },
  beforeDestroy() {
  },
  components: {
    Header
  },
  computed:{
  }
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

* {
  margin: 0;
  padding: 0;
}

body, html {
  min-height: 100%;
  background: #F5F7FA;
}
</style>
