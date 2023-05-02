<template>
    <div :class="['attention_inhibition-widget', start ? 'active': '']">
        <div v-if="start" class="choose-info"> <span>用时: {{ timmerShow }}</span> <span>总共： {{ formData.count }}</span>
            <span>剩余： {{ formData.count - trainResultTotal.length }}</span> <span>错误次数: {{ currentTrainResult.errorNumber
            }}</span>
        </div>
        <div class="attention_stable-config" v-if="!start">
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
            </el-form>
        </div>
        <div class="maze-container" v-if="start">
            <Maze :strategy="strategy" :difficulty="difficulty" @start="onStart" @finish="onFinish" @init="onInit"
                :style="mazeStyle"></Maze>
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
    computed:{
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
        },
        onStart() {
            console.log('this is on onStart')

        },
        onFinish() {
            console.log('this is on finish')
        },
        onInit() {
            console.log('this is on onInit')

        }
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

</style>