<template>
    <div class="attention_concentration-widget">
        <div v-if="start" class="choose-info"> <span>用时: {{ timmerShow }}</span>
            <span>轮数： {{ formData.count }} </span>
            <span>此刻： {{ currentIndex }} </span> <span>总共： {{ findPairs.length }}</span>
            <span>剩余： {{ findPairs.length - rightArray.length / 2 }}</span> <span>错误次数: {{ currentTrainResult.errorNumber
            }}</span>
        </div>
        <div class="attention_concentration-config" v-if="!start">
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
        <div class="attention_concentration-content" v-if="start">
            <div v-for="item, index in cards"
                :class="['card', rightArray.indexOf(index) >= 0 ? 'active' : '', currentChooseArray.indexOf(index) >= 0 ? 'active' : '']"
                :style="cardStyle" @click="choose(index)"> {{ item }}</div>
        </div>
        <div class="attention_concentration_train-time-count" v-if="timeCountShow">
            {{ count }}
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            time: "00: 00: 00",
            start: false,
            currentIndex: 1,
            rightArray: [],
            cards: [],
            count: 3,
            timeCountShow: false,
            formData: {
                level: 1,
                count: 5
            },
            currentTrainResult: {
                errorNumber: 0,
                time: 0,
            },
            currentChooseArray: [],
            trainResultTotal: []
        }
    },
    computed: {
        numberCards() {
            if (this.formData.level == 1) {
                return 10
            }

            if (this.formData.level == 2) {
                return 20
            }

            if (this.formData.level == 3) {
                return 30
            }

            if (this.formData.level == 4) {
                return 40
            }
        },
        findPairs() {
            let used = []; // 用于记录已经使用过的元素
            let pairs = []; // 用于记录满足条件的元素对
            const arr = this.cards
            for (let i = 0; i < arr.length - 1; i++) {
                if (used.includes(i)) continue; // 如果 i 已经使用过，跳过该元素
                for (let j = i + 1; j < arr.length; j++) {
                    if (used.includes(j)) continue; // 如果 j 已经使用过，跳过该元素
                    if (arr[i] + arr[j] === 10) {
                        pairs.push([arr[i], arr[j]]);
                        used.push(i, j);
                        break; // 找到一组符合条件的元素，跳出内循环
                    }
                }
            }
            return pairs;
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
            this.cards = new Array(this.numberCards * this.numberCards).fill(15).map((item, index) => parseInt(9 * Math.random() + 1)).sort(() => Math.random() - 0.5);
            this.timeCount()
        },
        endTotalTask() {
            console.log('end total task')
            console.log(this.trainResultTotal)
            this.start = false
            clearInterval(this.timmer)
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
            this.cards = new Array(this.numberCards * this.numberCards).fill(15).map((item, index) => parseInt(9 * Math.random() + 1)).sort(() => Math.random() - 0.5);
            this.timeCount()
        },
        choose(index) {
            if (this.currentChooseArray.length == 0) {
                this.currentChooseArray.push(index)
                return
            }
            if (this.cards[this.currentChooseArray[0]] + this.cards[index] == 10) {
                this.rightArray.push(this.currentChooseArray[0], index)
                this.currentChooseArray = []
            } else {
                this.currentTrainResult.errorNumber += 1
                this.currentChooseArray = []
            }
            console.log(this.findPairs, this.rightArray)
            if (this.findPairs.length == this.rightArray.length / 2) {
                this.trainResultTotal.push({
                    pationId: this.$router.currentRoute.params.pationId,
                    mode: 'concentration',
                    currentTime: +new Date(),
                    level: this.formData.level,
                    time: this.currentTrainResult.time / 1000,
                    errorNumber: this.currentTrainResult.errorNumber,
                    totalNumber: this.findPairs.length
                })
                if (this.currentIndex >= this.formData.count) {
                    this.endTotalTask()
                } else {
                    this.currentIndex += 1
                    this.reStart()
                }
            }

        },
        generateRandomNumbers() {
            const arr = [];
            let sum = 0;
            for (let i = 0; i < 5; i++) {
                const num = Math.random() * 0.1 + 0.15;
                arr.push(num);
                sum += num;
            }
            const multiplier = 1 / sum;
            for (let i = 0; i < arr.length; i++) {
                arr[i] *= multiplier;
            }
            return arr;
        },
        getRandomHeight(start, totalHeight) {
            console.log(start, totalHeight)
        }
    }
}
</script>

<style>
.attention_concentration-widget {
    max-width: 800px;
    margin: 5px auto;
    background: white;
    padding: 30px;
    box-sizing: border-box;
}

.attention_concentration-widget .choose-info span {
    display: inline-block;
    width: 150px;
    overflow: hidden;
}

.attention_concentration-content {
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

.attention_concentration_train-time-count {
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