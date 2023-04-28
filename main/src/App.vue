<template>
  <div id="app">
    <Header></Header>
    <router-view :config="config"> </router-view>
  </div>
</template>
<script>
import { getApplications, initDevTools } from "./api";
import Header from './Components/header/index.vue'
export default {
  data() {
    return {
      config: []
    }
  },
  components:{
    Header
  },
  mounted() {
    setTimeout(async () => {
      const config = await getApplications()
      console.log('adfasdfasdf', config)
      this.config = config
    }, 100);
  },

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
