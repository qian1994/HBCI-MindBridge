<template>
  <div class="container">
    <TopNav :connectSession="connectSession"></TopNav>
    
  </div>
</template>
<script>
import TopNav from '../Components/topNav/index.vue'
export default {
   components: {
    TopNav
   },
   data() {
    return {
      connectSession: true
    }
   }
};
</script>
