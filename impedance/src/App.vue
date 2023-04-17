<template>
  <div id="app">
    <Header></Header>
    <router-view ></router-view>
  </div>
</template>
<script>
import Header from './Components/Header/index.vue'

export default {
  data() {
    return {
    }
  },
  components:{
    Header
  },
};
</script>
<style>
* {
  margin: 0;
  padding: 0;
}

html,
body {
  width: 100%;
  height: 100%;
  background: #F5F7FA;
}

#app {
  height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
