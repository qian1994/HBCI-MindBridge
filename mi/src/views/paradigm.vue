<template>
    <div class="mi-paradigm">
      <div class="mi-title"> 请根据提示进行相关运动想象 </div>
      <div class="mi-footer">
        <el-button @click="start">start</el-button>
        <el-button @click="stop">stop</el-button>
      </div>
      <div :class="{ 'breack-active': isActive }">
        <div class="mi-hand">
          <div class="img">
            <img src="../assets/left-hand.png" v-if="currentIndex == 1">
          </div>
          <div class="img">
            <img src="../assets/right-hand.png" v-if="currentIndex == 2">
          </div>
        </div>
        <div class="mi-rest">
            <div class="mi-rest-icon" :class="{ 'rest-active': restActive }">
              <span>+</span>
            </div>
        </div>
        <div class="mi-foot">
          <div class="img">
            <img src="../assets/left-foot.png" v-if="currentIndex == 3">
          </div>
          <div class="img">
            <img src="../assets/right-foot.png" v-if="currentIndex == 4">
          </div>
        </div>
      </div>
      
    </div>
  </template>
  <script>
  export default {
    components: {
    },
    data() {
      return {
        show_mi: [],
        trial_index: 0,
        breakTime: true,
        rest: 0
      }
    },
    created() {
      this.show_mi = this.$router.history.current.params.mi
    },
    computed:{
      currentIndex() {
        if (this.rest) {
          return 0
        }
        return this.show_mi[this.trial_index]
      },
      isActive() {
        if(this.breakTime) {
          return true
        }
        return false
      }, 
      restActive() {
        if (this.currentIndex == 0) {
          return false
        }
        return true
      }
    },
    methods: {
     start() {
      window.eel.start()
      this.miStart()
     },
     stop() {
      window.eel.stop()
      alert('实验结束，请关闭窗口，或回到首页')
     },
     showRest() {
      this.breakTime = false
      this.rest = 1
      setTimeout(() => {
        this.showmipng()
      }, 1000)
     },
     showmipng() {
      this.rest = 0
      this.breakTime = false
      window.eel.trigger(this.currentIndex, this.trial_index)
      if(this.trial_index >= this.show_mi.length) {
        window.eel.stop()
        return
      }
      setTimeout(() => {
        window.eel.trigger(this.currentIndex, this.trial_index)
        this.trial_index += 1
        this.miStart()
      }, 6000)
     },
     miStart() {
      this.rest = 0
      this.breakTime = true
      const timer1 = setTimeout(() => {
        this.showRest()
      }, 2000);
     }
    }
  };
  </script>
  <style>
    .mi-title {
      text-align: center;
      color: orange;
      font-size: 20px;
    }
    .mi-paradigm .mi-rest {
      font-size: 100px;
      color: white;
      text-align: center;
      margin: 50px 0; 
    }

    .breack-active {
      opacity: 0;
    }

    .mi-footer {
      text-align: center;
      
    }
    .rest-active {
      opacity: 0;
    }
    .mi-footer button {
      width: 300px;
      height: 40px;
      margin: 20px 100px;
    }

    .mi-paradigm .img {
      width: 100px;
      margin: 50px 300px; 
      height: 200px;
    }

    .mi-paradigm .img img {
      margin: 0;
    }
  </style>