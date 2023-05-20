<template>
  <div id="app">
   
    <router-view />
  </div>
</template>
<script>
import { msgListener  } from "./api";
import { mapState } from "vuex" ;
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
    ...mapState(['timeSerise'])
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
