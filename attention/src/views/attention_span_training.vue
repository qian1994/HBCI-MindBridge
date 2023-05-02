<template>
    <div class="attention_span_train-widget">
        <h2>注意力广度训练</h2>
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
                    <el-button class="back" @click="goBack"> 返回 </el-button>
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
    </div>
</template>

<script>
export default {
    data() {
        return {
            time: "00: 00: 00",
            currentCount: 1,
            start: false,
            currentIndex: 1,
            rightArray: [],
            cards: [],
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

            this.timmer = setInterval(() => {
                this.currentTrainResult.time += 100
            }, 100);
        },
        goBack() {
            this.$router.go(-1)
        },
        endTotalTask() {
            console.log('end total task')
        },
        reStart() {
            console.log('this is re start')
            if (this.timmer) {
                clearInterval(this.timmer)
            }
            this.currentTrainResult.time = {
                time: 0,
                errorNumber: 0
            }
            this.rightArray = []
            this.cards = new Array(this.numberCards * this.numberCards).fill(15).map((item, index) => index + 1).sort(() => Math.random() - 0.5);
            this.timmer = setInterval(() => {
                this.currentTrainResult.time += 100
            }, 100);
        },
        choose(item) {
            if (this.currentIndex == item) {
                this.rightArray.push(item)
                this.currentIndex += 1
                if (this.numberCards * this.numberCards == this.rightArray.length) {
                    clearInterval(this.timmer)
                    this.currentCount += 1
                    this.trainResultTotal.push({
                        time: this.currentTrainResult.time/1000,
                        errorNumber: this.currentTrainResult.errorNumber
                    })
                    if (this.currentCount > this.formData.count) {
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
</style>