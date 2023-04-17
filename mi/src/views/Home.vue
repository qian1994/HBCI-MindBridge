<template>
  <div class="container">
    <div class="">
      <div class="mi-hand">
        <img src="../assets/left-hand.png" alt="" @click="choose(1)">
        <img src="../assets/right-hand.png" alt=""  @click="choose(2)">
      </div>
      <div class="mi-foot">
        <img src="../assets/left-foot.png" alt=""  @click="choose(3)">
        <img src="../assets/right-foot.png" alt=""  @click="choose(4)">
      </div>
    </div>
    <div>
      <div class="mi-choose-word">
        选中：
        <span v-for="index in mi_array">{{index}}</span>
      </div>
    </div>
    <div class="mi-footer">
      <button class="mi-button" @click="enter">enter</button>
      <button class="mi-button" @click="deleteW">delete</button> 
    </div>
  </div>
</template>
<script>
export default {
  components: {
  },
  data() {
    return {
      mi_array: []
    }
  },
  created() {
  },
  destroyed() {
  },
  methods: {
    enter() {
      if (this.mi_array.length == 0) {
        return;
      }
      setTimeout(() => {
        this.$router.push({ name:"paradigm", params:{mi: this.mi_array} })
      }, 1000);
    },  
    choose(item) {
      this.mi_array.push(item)
    },
    deleteW() {
      this.mi_array.pop()
    }
  },
  
};
</script>
<style>
.container {
  width: 100%;
  height: 100%;
  padding-top: 30px;
  box-sizing: border-box;
  position: relative;
}


.mi-hand, .mi-foot {
  display: flex;
  justify-content: center;
}

.mi-hand img, .mi-foot img {
  width: 100px;
  margin: 50px 300px; 

}

.mi-footer {
  text-align: center;
}

button.mi-button {
  width: 300px;
  margin: 20px 50px;
  height: 40px;
}

.mi-choose-word {
  margin: 20px 0;
  padding: 50px 100px;
  text-align: center;
  color: orange;
  background-color: white;
  font-size: 20px;

}

.mi-choose-word span {
  font-size: 20px;
  color: orange;
  display: inline-block;
  margin: 20px;
}
</style>