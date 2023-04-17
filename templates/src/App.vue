<template>
  <div id="app">
    <div id="nav">
      <router-link to="/home">home</router-link>|
      <router-link to="/pannels">pannels</router-link>
    </div>
    <router-view />
  </div>
</template>
<script>
import { msgListener  } from "./api";
import { mapState } from "vuex" ;
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

    timerSeriseButton() {
      this.$store.dispatch("changeTimeSerise", 
        [1,2,3]
      )
    },

    fftButton() {
      this.$store.dispatch("changeFFT", 
        [1,2,3]
      )
    }
    
  },
  created() {
    msgListener.add(this.streamReceive);
  },
  beforeDestroy() {
    msgListener.remove(this.streamReceive);
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
</style>
