<template>
  <div id="app">
    <router-view />
  </div>
</template>
<script>
export default {
};
</script>
<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  overflow: hidden;
  padding: 50px auto;
}
*{
  margin: 0;
  padding: 0;
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
