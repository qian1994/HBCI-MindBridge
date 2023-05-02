<template>
  <div class="attention-jigsaw-puzzle">
    <div v-if="start"> <span>用时: {{ timmerShow }}</span> <span>次数： {{ currentCount }}</span></div>
    <div v-if="start"> <span>错误次数: {{ currentTrainResult.errorNumber }}</span> </div>
    <div class="attention_span_train-config" v-if="!start">
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
      <!-- <button class="btn btn-warning btn-block btn-reset" @click="render">重置游戏</button> -->
    </div>
  </div>
</template>

<script>
import vue from "vue"
export default {
  data() {
    return {
      start: false,
      puzzles: [],
      formData: {
        level: 1,
        count: 5
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
        if (isPass) {
          alert('恭喜，闯关成功！')
        }
      }
    }
  },
  ready() {
    this.render()
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