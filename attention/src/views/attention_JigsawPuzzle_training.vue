<template>
  <div class="attention-jigsaw-puzzle">
    <h2>注意力与观察训练</h2>
    <div v-if="start"> <span>用时: {{ timmerShow }}</span> <span>次数： {{ currentCount }}</span></div>
    <div v-if="start"> <span>错误次数: {{ currentTrainResult.errorNumber }}</span> </div>
    <div class="attention_span_train-config" v-if="!start">
      <el-form :model="formData" ref="ruleForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="等级" prop="count">
          <el-select v-model="formData.level" placeholder="请选择">
            <el-option label="初级" value="1" key="1"> </el-option>
            <el-option label="中级" value="2" key="2"> </el-option>
            <el-option label="高级" value="3" key="3"> </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="次数" prop="count">
          <el-select v-model="formData.count" placeholder="请选择">
            <el-option v-for="item, index in new Array(10).fill(0)" :label="index + 1" :value="index + 1"
              :key="'key' + index"> </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button size="large" @click="submit"> 开始 </el-button>
          <el-button size="large" @click="$router.go(-1)"> 返回 </el-button>

        </el-form-item>
        <el-form-item>
          <div>
            训练时，练习者用鼠标按1,2,3,4,5,6 的顺序依次点击其位置, 每次训练至少5次以上, 用时越短则说明注意力水平越高，
            当训练成绩连续5天都无法得到提升，请调高训练级别。
          </div>
        </el-form-item>
      </el-form>
    </div>
    <div class="attention-jigsaw-puzzle-content">
      <ul class="puzzle-wrap">
        <li :class="{ 'puzzle': true, 'puzzle-empty': !puzzle }" v-for="puzzle, index in puzzles" v-text="puzzle"
          @click="moveFn(index)"></li>
      </ul>
    </div>
  </div>
</template>

<script>
import vue from "vue"
import { savePationData } from '../api/index'

export default {
  data() {
    return {
      start: false,
      puzzles: [],
      timeCountShow: false,
      count: 3,
      formData: {
        level: 1,
        count: 3
      },
      currentTrainResult: {
        errorNumber: 0,
        time: 0,
      },
      trainResultTotal: []
    }
  },
  methods: {
    submit() {
      this.start = true
      this.render()
    },
    // 重置渲染
    render() {
      let puzzleArr = [],
        i = 1
      // 生成包含1 ~ 15数字的数组
      for (i; i < 16; i++) {
        puzzleArr.push(i)
      }

      // 随机打乱数组
      puzzleArr = puzzleArr.sort(() => {
        return Math.random() - 0.5
      });

      // 页面显示
      this.puzzles = puzzleArr
      this.puzzles.push('')
    },

    // 点击方块
    moveFn(index) {
      // 获取点击位置及其上下左右的值
      let curNum = this.puzzles[index],
        leftNum = this.puzzles[index - 1],
        rightNum = this.puzzles[index + 1],
        topNum = this.puzzles[index - 4],
        bottomNum = this.puzzles[index + 4]

      // 和为空的位置交换数值
      if (leftNum === '' && index % 4) {
        vue.set(this.puzzles, index - 1, curNum)
        vue.set(this.puzzles, index, '')

        // this.puzzles.$set(index - 1, curNum)
        // this.puzzles.$set(index, '')
      } else if (rightNum === '' && 3 !== index % 4) {
        // this.puzzles.$set(index + 1, curNum)
        // this.puzzles.$set(index, '')
        vue.set(this.puzzles, index + 1, curNum)
        vue.set(this.puzzles, index, '')
      } else if (topNum === '') {
        // this.puzzles.$set(index - 4, curNum)
        // this.puzzles.$set(index, '')
        vue.set(this.puzzles, index - 4, curNum)
        vue.set(this.puzzles, index, '')
      } else if (bottomNum === '') {
        // this.puzzles.$set(index + 4, curNum)
        // this.puzzles.$set(index, '')
        vue.set(this.puzzles, index + 4, curNum)
        vue.set(this.puzzles, index, '')
      }
      this.passFn()
    },

    // 校验是否过关
    passFn() {
      if (this.puzzles[15] === '') {
        const newPuzzles = this.puzzles.slice(0, 15)
        const isPass = newPuzzles.every((e, i) => e === i + 1)
        if (!isPass)
          return

        this.trainResultTotal.push({
          pationId: this.$router.currentRoute.params.id,
          mode: 'maze',
          currentTime: +new Date(),
          level: this.formData.level,
          time: this.currentTrainResult.time / 1000,
          errorNumber: this.currentTrainResult.errorNumber,
          totalNumber: this.findPairs.length
        })
        this.currentTrainResult = {
          time: 0,
          errorNumber: 0
        }

        clearInterval(this.timmer)
        if(this.formData.count <= this.trainResultTotal.length) {
          this.endTotalTask()
          return
        }
        this.reStart()
      }
    },

    async endTotalTask() {
      this.start = false
      console.log(this.trainResultTotal)
      // this is place to upload the total result 
      const res = await savePationData(this.trainResultTotal)
      this.$router.go(-1)

    },
    timerRuning() {
      this.timmer = setInterval(() => {
        this.currentTrainResult.time += 100
      }, 100);
    },
    reStart() {
      if (this.timmer) {
        clearInterval(this.timmer)
      }
      this.currentTrainResult = {
        time: 0,
        errorNumber: 0
      }
      this.rightArray = []
      this.cards = new Array(this.numberCards * this.numberCards).fill(15).map((item, index) => index + 1).sort(() => Math.random() - 0.5);
      this.timeCount()
    },
    timeCount() {
      this.count = 3
      this.timeCountShow = true
      clearInterval(this.timmer)
      setTimeout(() => {
        clearInterval(this.timmer)
        this.timeCountShow = false
        this.timerRuning()
      }, 3000);
      this.timmer = setInterval(() => {
        this.count -= 1
      }, 1000);
    },
  }
}
</script>

<style>
.attention-jigsaw-puzzle {
  max-width: 800px;
  margin: 5px auto;
  background: white;
  padding: 30px;
  box-sizing: border-box;
}

.puzzle-wrap {
  width: 400px;
  height: 400px;
  margin: 20px auto;
  margin-bottom: 40px;
  padding: 0;
  background: #ccc;
  list-style: none;
}

.puzzle {
  float: left;
  width: 100px;
  height: 100px;
  font-size: 20px;
  background: #f90;
  text-align: center;
  line-height: 100px;
  border: 1px solid #ccc;
  box-shadow: 1px 1px 4px;
  text-shadow: 1px 1px 1px #B9B4B4;
  cursor: pointer;
  box-sizing: border-box;
}

.puzzle-empty {
  background: #ccc;
  box-shadow: inset 2px 2px 18px;
}

.btn-reset {
  box-shadow: inset 2px 2px 18px;
}
</style>