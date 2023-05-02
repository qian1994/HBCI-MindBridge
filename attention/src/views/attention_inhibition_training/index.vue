<template>
    <div :class="['attention_inhibition-widget', start ? 'active' : '']">
        <div v-if="start" class="choose-info"> <span>用时: {{ timmerShow }}</span> <span>总共： {{ formData.count }}</span>
            <span>剩余： {{ formData.count - trainResultTotal.length }}</span> </div>
        <div class="attention_stable-config" v-if="!start">
            <el-form :model="formData" ref="ruleForm" label-width="100px" class="demo-ruleForm">
                <el-form-item label="次数" prop="count">
                    <el-input v-model="formData.count"></el-input>
                </el-form-item>
                <el-form-item label="难度等级" prop="count">
                    <el-select v-model="difficulty" placeholder="请选择">
                        <el-option key="easy" value="easy" label="easy"></el-option>
                        <el-option key="normal" value="normal" label="normal"></el-option>
                        <el-option key="hard" value="hard" label="hard"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item>
                    <el-button size="large" @click="submit"> 开始 </el-button>
                </el-form-item>
            </el-form>
        </div>
        <div class="maze-container" v-if="start">
            <Maze :strategy="strategy" :difficulty="difficulty" @start="onStart" @finish="onFinish" @init="onInit"
                :style="mazeStyle"></Maze>
        </div>
        <div class="attention_inhibition-widget-count" v-if="timeCountShow">
            {{ count }}
        </div>
    </div>
</template>

<script>
import Maze from './Maze.vue'
// type Difficulty = "easy" | "normal" | "hard";
// type Strategy = "cluster" | "dig";
export default {
    data() {
        return {
            count: 3,
            timeCountShow: false,
            strategy: 'dig',
            difficulty: 'easy',
            mazeStyle: {
                width: "100%",
                height: "100%"
            },
            formData: {
                level: 1,
                count: 2
            },
            currentTrainResult: {
                errorNumber: 0,
                time: 0,
            },
            trainResultTotal: [],

            start: false
        }
    },
    components: {
        Maze
    },
    mounted() {

    },
    computed: {
        timmerShow() {
            const time = parseInt(this.currentTrainResult.time / 1000) || 0
            const mSecond = this.currentTrainResult.time % 1000 || 0
            const minute = parseInt(time / 60)
            const second = time % 60 || 0
            return `${minute}:${second}:${mSecond}`
        },
    },
    methods: {
        submit() {
            this.start = true
            this.timeCount()
        },
        onStart() {
            console.log('this is on onStart')

        },
        endTotalTask() {
            console.log('this is place end totalTask')
            console.log(this.trainResultTotal)
            this.start = false
        },
        onFinish() {
            console.log('this is on finish')
            this.trainResultTotal.push({
                pationId: this.$router.currentRoute.params.pationId,
                mode: 'inhibition',
                currentTime: +new Date(),
                level: this.difficulty,
                time: this.currentTrainResult.time / 1000,
                errorNumber: this.currentTrainResult.errorNumber,
            })
            this.currentTrainResult ={
                errorNumber: 0,
                time: 0,
            },
            clearInterval(this.timmer)
            if(this.trainResultTotal.length < this.formData.count) {
                this.timeCount()
            }else{
                this.endTotalTask()
            }
        },
        onInit() {
            console.log('this is on onInit')

        },
        timerRuning() {
            this.timmer = setInterval(() => {
                this.currentTrainResult.time += 100
            }, 100);
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
<style scoped>
.attention_inhibition-widget {
    max-width: 800px;
    margin: 5px auto;
    background: white;
    padding: 30px;
    box-sizing: border-box;
}

.attention_inhibition-widget.active {
    width: 1300px;
    max-width: 1300px;
    overflow: hidden;
}

.maze-container {
    width: 1200px;
    height: 800px;
}


.attention_inhibition-widget-count {
    position: fixed;
    z-index: 100;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.2);
    text-align: center;
    top: 0;
    left: 0;
    color: red;
    line-height: 500px;
    font-size: 100px;
}
</style>