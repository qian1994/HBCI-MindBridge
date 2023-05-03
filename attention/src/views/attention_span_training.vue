<template>
    <div class="attention_span_train-widget">
        <h2>注意力广度训练</h2>
        <div v-if="start"> <span>用时: {{ timmerShow }}</span> <span>次数： {{ trainResultTotal.length }} / {{formData.count}}</span> </div>
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
                        <el-option v-for="item, index in new Array(10).fill(0)" :label="index+1" :value="index+1" :key="'key' + index"> </el-option>
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
        <div class="attention_span_train-content" v-if="start">
            <div v-for="item in cards" :class="['card', rightArray.indexOf(item) >= 0 ? 'active' : '']" :style="cardStyle"
                @click="choose(item)"> {{ item }}</div>
        </div>
        <div class="attention_span_train-time-count" v-if="timeCountShow">
            {{ count }}
        </div>
    </div>
</template>

<script>
import { savePationData } from '../api/index'

export default {
    data() {
        return {
            time: "00: 00: 00",
            start: false,
            currentIndex: 1,
            rightArray: [],
            cards: [],
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
    computed: {
        numberCards() {
            if (this.formData.level == 1) {
                return 5
            }

            if (this.formData.level == 2) {
                return 7
            }

            if (this.formData.level == 3) {
                return 10
            }

            if (this.formData.level == 4) {
                return 15
            }
        },

        cardStyle() {
            let number = parseInt(600 / Math.sqrt(this.cards.length))
            return `width:${number}px;height:${number}px; line-height: ${number}px;`
        },

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
            this.start = true
            this.cards = new Array(this.numberCards * this.numberCards).fill(15).map((item, index) => index + 1).sort(() => Math.random() - 0.5);
            this.timeCount()
        },
        goBack() {
            this.$router.go(-1)
        },
        async endTotalTask() {
            this.start = false
            console.log(this.trainResultTotal)
            // this is place to upload the total result 
            const res = await savePationData(this.trainResultTotal)
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
            this.currentIndex = 1
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
                this.count -=1
            }, 1000);
        },
        choose(item) {
            if (this.currentIndex == item) {
                this.rightArray.push(item)
                this.currentIndex += 1
                if (this.numberCards * this.numberCards == this.rightArray.length) {
                    clearInterval(this.timmer)
                    this.trainResultTotal.push({
                        pationId: this.$router.currentRoute.params.pationId,
                        mode: 'span',
                        currentTime: +new Date(),
                        level: this.formData.level,
                        time: this.currentTrainResult.time / 1000,
                        errorNumber: this.currentTrainResult.errorNumber
                    })
                    if (this.trainResultTotal.length >= this.formData.count) {
                        this.endTotalTask()
                        return
                    }
                    this.reStart()
                }
                return
            }
            this.currentTrainResult.errorNumber += 1
        }
    }
}
</script>

<style>
.attention_span_train-widget h2 {
    margin-bottom: 15px;
}

.attention_span_train-widget {
    max-width: 800px;
    margin: 5px auto;
    background: white;
    padding: 30px;
    box-sizing: border-box;
}

.attention_span_train-content {
    width: 600px;
    height: 600px;
    margin: 30px auto;
    border-right: 1px solid #ddd;
    border-bottom: 1px solid #ddd;
}

.card {
    display: inline-block;
    text-align: center;
    border-left: 1px solid #ddd;
    border-top: 1px solid #ddd;
    box-sizing: border-box;
    cursor: pointer;
}

.card.active {
    background: gray;
}

.card:hover {
    background: #ddd;
}
.attention_span_train-time-count {
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