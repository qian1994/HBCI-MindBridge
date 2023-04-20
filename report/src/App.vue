<template>
  <div id="app">
    <Header></Header>
    <router-view />
  </div>
</template>
<script>
import Header from './Components/header/index.vue'
export default {
  components:{
    Header
  },
};
</script>
<style>
* {
  padding: 0;
  margin: 0;
}

html,
body {
  width: 100%;
  min-height: 100%;
}

#app {
  min-height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: #F5F7FA;
}
</style>
