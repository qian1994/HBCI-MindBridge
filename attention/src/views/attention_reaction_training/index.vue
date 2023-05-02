<template>
  <div class="attention_reaction_train">
    <div class="attention_reaction_train-config" v-if="!start">
      <el-form :model="formData" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="难度级别" prop="name">
          <el-input v-model="formData.level"></el-input>
        </el-form-item>
        <el-form-item label="次数" prop="count">
          <el-input v-model="formData.count"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button size="large" @click="submit"> 开始 </el-button>
        </el-form-item>
        <el-form-item>
          <div>
            请根据提示，选择对应的颜色图案
          </div>
        </el-form-item>
      </el-form>
    </div>
    <div v-if="start"> <span>用时: {{ timmerShow }}</span> <span>次数： {{ currentCount }}</span></div>
    <div v-if="start"> <span>错误次数: {{ currentTrainResult.errorNumber }}</span> </div>
    <div v-if="start">
      <Shape @close="stopShape" :shape="currentShape" :color="currentColor" />
    </div>
  </div>
</template>

<script>
// import Endgame from "./components/Endgame";
import Shape from "./Shape.vue";

export default {
  name: "App",
  data() {
    return {
      formData: {
        level: 1,
        count: 5
      },
      currentTrainResult: {
        errorNumber: 0,
        time: 0,
      },
      currentCount: 0,
      start: false,
      showShape: false,
      colorArray: ["yellow", "green", "red", "blue"],
      shapeArray: ["circle", "rectangle", "triangular"],
      currentShape: null, //will hold one shape at a time from ShapeArray
      currentColor: null, //will hold one color at a time from colorArray
      clickOnGreenFlag: false,
      showResults: false, // show the end game screen
      intervalShape: null,
      greenCounter: 0, //how many time to player succed
      timer: null,
      timeplayed: 0,
      showIndicator: false,
      showIndicatorInterval: null,
      successIndicator: null, //will chane to sentence according to 'greenCounter'
      highestScore: 0,
    };
  },
  components: { Shape },
  computed: {
    timmerShow() {
      const time = parseInt(this.currentTrainResult.time / 1000) || 0
      const mSecond = this.currentTrainResult.time % 1000 || 0
      const minute = parseInt(time / 60)
      const second = time % 60 || 0
      return `${minute}:${second}:${mSecond}`
    }
  },
  methods: {
    submit() {
      console.log('this is submit click')
      this.start = true
      this.randomShapeAndColor()

    },
    startTimer() {
      this.timer = setInterval(() => {
        this.timeplayed += 10;
      }, 10);
    },
    stopTimer() {
      clearInterval(this.timer);
    },
    //
    randomShapeAndColor() {
      // this.timerDelay = 300 + Math.random() * 400;
      this.startTimer();
      this.intervalShape = setInterval(this.addShape, 500);
    },
    addShape() {
      this.currentColor = this.colorArray[Math.floor(Math.random() * 4)];
      this.currentShape = this.shapeArray[Math.floor(Math.random() * 3)];

      this.showResults = false;
      this.showShape = true;
      // this.toggleShowShape();
    },
    toggleShowShape() {
      this.showShape = !this.showShape;
    },
    stopShape(clickOnGreen) {
      this.clickOnGreenFlag = clickOnGreen;
      if (this.clickOnGreenFlag) {
        this.showIndicator = true;
        this.showIndicatorInterval = setInterval(this.closeIndicator, 500);
        this.greenCounter++;
        console.log('this is good choose')
      } else {
        // clearInterval(this.intervalShape);
        // this.stopTimer();
        // this.successIndicator = this.giveSuccessIndicator(); //getting value for seccess
        // this.timeplayed = this.timeplayed / 1000; //from ms to seconds
        // this.timeplayed = parseFloat(this.timeplayed.toFixed(4)); //only 4 digit decimal
        // this.showShape = false; //stop showing the shapes on the DOM
        // if (this.greenCounter > this.highestScore) {
        //   //need to upload name and score
        //   this.highestScore = this.greenCounter;
        // }
        // this.showResults = true; //showing the end game DOM
        console.log('this is wrong choose')
      }
    },
    closeIndicator() {
      clearInterval(this.showIndicatorInterval);
      this.showIndicator = false;
    },
    closeEndGame() {
      this.showResults = false;
      this.greenCounter = 0;
      this.endTimer = 0;
    },
    giveSuccessIndicator() {
      //returing sentnce according to the value
      if (this.greenCounter <= 3) return "You snooze you lose";
      else if (this.greenCounter <= 6) return "Congrats on a mediocre job";
      else return "Eternal bragging rights";
    },
  },
};
</script>

<style>
.welcome h1 {
  color: blueviolet;
}

.attention_reaction_train {
  max-width: 800px;
  margin: 5px auto;
  background: white;
  padding: 30px;
  box-sizing: border-box;
  min-height: 600px;
}
</style>
