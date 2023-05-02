<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script>
export default {
  methods: {
  },
  created() {
  },
  beforeDestroy() {
  },
  components: {
  },
  computed:{
  }
};
</script>
<style>
* {
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

html,
body {
  width: 100%;
  height: 100%;
  background: #F5F7FA;
  -moz-user-select:none;  /* 火狐 */
  -webkit-user-select:none; /* Safari 和 Chrome */
  -ms-user-select:none; /* IE10+ */
  user-select:none; /* 标准语法 */
}
</style>
