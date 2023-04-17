<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script>
export default {
  methods: {
    refresh() {
      window.location.reload();
    },
    streamReceive(stream) {
      this.streamJson = stream;
      const data = JSON.parse(JSON.parse(stream).data);
      console.log(data);
    },
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
  height: 100%;
}

#app {
  height: 100%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  background-color: black;
}
</style>
