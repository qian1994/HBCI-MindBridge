<template>
    <div class="attention_stable-widget">
        <h2>注意力稳定性训练</h2>
        <div v-if="start" class="choose-info"> <span>用时: {{ timmerShow }}</span> <span>总共： {{ formData.count }}</span>
            <span>剩余： {{ formData.count - trainResultTotal.length }}</span> <span>错误次数: {{ currentTrainResult.errorNumber
            }}</span>
        </div>
        <div class="attention_stable-config" v-if="!start">
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
            </el-form>
        </div>
        <div class="attention_stable-content" v-if="start">
            <div class="left-cards">
                <div v-for="item, index in findPairs[0]"
                    :class="['attention_stable-content-cards', currentChooseId === index ? 'active' : '']"
                    :style="`${cardStyle[0][index]['style']}`" @click="choose(index)">
                    {{ item }}
                </div>
            </div>
            <div class="right-cards">
                <div v-for="item, index in findPairs[1]"
                    :class="['attention_stable-content-cards', currentChooseItem === index >= 0 ? 'active' : '']"
                    :style="`${cardStyle[1][index]['style']}`" @click="chooseItem(index)">
                    {{ item }}
                </div>
            </div>
            <div v-if="lines" v-for="item, index in lines">
                <div v-if="rightArray.indexOf(index) == -1" v-for="line in lines[index]"
                    class="attention_stable-content-lines"
                    :style="`width:${line['width']}px; top:${line['top']}px; left: ${line['left']}px; height: ${line['height']}px`">
                </div>
            </div>
        </div>
        <div class="attention_stable-content-lines-count" v-if="timeCountShow">
            {{ count }}
        </div>
    </div>
</template>

<script>
import { savePationData } from '../api/index'
export default {
    data() {
        return {
            count: 3,
            timeCountShow: false,
            time: "00: 00: 00",
            currentCount: 5,
            start: false,
            currentIndex: 1,
            rightArray: [],
            cards: [],
            shuffleIndex: [],
            totalHeight: 700,
            lines: [],
            trainResultTotal: [],
            formData: {
                level: 1,
                count: 2
            },
            currentTrainResult: {
                errorNumber: 0,
                time: 0,
            },
            currentChooseId: '',
            currentChooseItem: ''
        }
    },
    computed: {
        numberCards() {
            if (this.formData.level == 1) {
                return 5
            }

            if (this.formData.level == 2) {
                return 10
            }

            if (this.formData.level == 3) {
                return 15
            }

            if (this.formData.level == 4) {
                return 20
            }
        },
        findPairs() {
            let arr1 = new Array(this.numberCards).fill(0).map((item, index) => index + 1)
            let arr2 = new Array(this.numberCards).fill(0).map((item, index) => String.fromCharCode(index + 'A'.charCodeAt()))
            return [arr1, arr2]
        },
        cardStyle() {
            return this.findPairs.map(cards => {
                return cards.map((item, index) => {
                    return {
                        style: `width:${700 / cards.length}px; height: ${700 / cards.length}px; text-align: center;  line-height:  ${700 / cards.length}px;color: white; border-bottom: 1px solid white; box-sizing: border-box;`
                    }
                })
            })
        },
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
            this.showLines()
            this.timeCount()
            this.trainResultTotal = []

        },
        showLines() {
            const sigleCardHeight = this.totalHeight / this.numberCards
            this.shuffleIndex = new Array(this.numberCards).fill(0).map((item, index) => index).sort(() => Math.random() - 0.5);
            const lines = this.shuffleIndex.map((item, index) => {
                let widths = this.generateRandomNumbers(index).map(item => item * (this.totalHeight - 2 * sigleCardHeight))
                let topStartPoint = index * sigleCardHeight + sigleCardHeight / 2
                let topEndPoint = item * sigleCardHeight + sigleCardHeight / 2
                let topPoint1 = 0
                let topPoit2 = 0
                if (index < this.shuffleIndex.length / 2) {
                    topPoint1 = this.totalHeight / 2 + (this.totalHeight - sigleCardHeight) / 2 * Math.random()
                    topPoit2 = (this.totalHeight - sigleCardHeight) / 2 * Math.random()
                } else {
                    topPoint1 = (this.totalHeight - sigleCardHeight) / 2 * Math.random() + sigleCardHeight / 2
                    topPoit2 = this.totalHeight / 2 + (this.totalHeight - sigleCardHeight) / 2 * Math.random()
                }
                const positions = [
                    {
                        top: topStartPoint,
                        left: sigleCardHeight,
                    }, {
                        top: topStartPoint,
                        left: sigleCardHeight + widths[0],
                    }, {
                        top: topPoint1,
                        left: sigleCardHeight + widths[0],
                    }, {
                        top: topPoint1,
                        left: sigleCardHeight + widths[0] + widths[1]
                    }, {
                        top: topPoit2,
                        left: sigleCardHeight + widths[0] + widths[1]
                    }, {
                        top: topPoit2,
                        left: sigleCardHeight + widths[0] + widths[1] + widths[2]
                    }, {
                        top: topEndPoint,
                        left: sigleCardHeight + widths[0] + widths[1] + widths[2]
                    }, {
                        top: topEndPoint,
                        left: sigleCardHeight + widths[0] + widths[1] + widths[2] + widths[3]
                    }
                ]
                let element = []
                for (let i = 0; i < positions.length; i++) {
                    if (i == 0) {
                        continue
                    }
                    element.push({
                        left: positions[i - 1]['left'],
                        width: (positions[i]['left'] - positions[i - 1]['left']) || 3,
                        top: positions[i]['top'] > positions[i - 1]['top'] ? positions[i - 1]['top'] : positions[i]['top'],
                        height: Math.abs(positions[i]['top'] - positions[i - 1]['top']) +3 || 3
                    })
                }
                return element
            })
            this.lines = lines
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
        async endTotalTask() {
            console.log('end total task')
            this.start = false
            clearInterval(this.timmer)
            console.log(this.trainResultTotal)
            const res = await savePationData(this.trainResultTotal)
        },
        reStart() {
            console.log('this is re start')
            if (this.timmer) {
                clearInterval(this.timmer)
            }
            this.trainResultTotal.push({
                pationId: this.$router.currentRoute.params.pationId,
                mode: 'stable',
                currentTime: +new Date(),
                level: this.formData.level,
                time: this.currentTrainResult.time / 1000,
                errorNumber: this.currentTrainResult.errorNumber,
            })
            this.currentTrainResult = {
                time: 0,
                errorNumber: 0
            }
            this.rightArray = []
            this.showLines()
            this.timeCount()

        },
        choose(index) {
            if (this.currentChooseItem === '') {
                this.currentChooseId = index
                return
            }

            if (this.shuffleIndex[this.currentChooseItem] == index) {
                this.rightArray.push(this.currentChooseId)
            } else {
                this.currentTrainResult.errorNumber += 1
                return
            }
            this.currentChooseItem = ''
            this.currentChooseId = ''
            if (this.rightArray.length < this.shuffleIndex) {
                return
            }
            this.currentIndex += 1
            if (this.currentIndex > this.formData.count) {
                this.trainResultTotal.push({
                pationId: this.$router.currentRoute.params.pationId,
                mode: 'stable',
                currentTime: +new Date(),
                level: this.formData.level,
                time: this.currentTrainResult.time / 1000,
                errorNumber: this.currentTrainResult.errorNumber,
            })
                this.endTotalTask()
                return
            }

            this.reStart()
        },
        chooseItem(index) {
            if (this.currentChooseId === '') {
                this.currentChooseItem = index
                return
            }
            if (this.currentChooseId == this.shuffleIndex.indexOf(index)) {
                this.rightArray.push(this.currentChooseId)
            } else {
                this.currentTrainResult.errorNumber += 1
                return
            }

            this.currentChooseItem = ''
            this.currentChooseId = ''
            if (this.rightArray.length < this.shuffleIndex.length) {
                return
            }

            this.currentIndex += 1
            
            if (this.currentIndex > this.formData.count) {
                this.trainResultTotal.push({
                pationId: this.$router.currentRoute.params.pationId,
                mode: 'stable',
                currentTime: +new Date(),
                level: this.formData.level,
                time: this.currentTrainResult.time / 1000,
                errorNumber: this.currentTrainResult.errorNumber,
            })
                this.endTotalTask()
                return
            }
            this.reStart()
        },
        generateRandomNumbers(index) {
            const start = 0.05 + index / this.numberCards * 0.37
            const second = 0.235
            const third = 0.235
            const last = 1 - start - second - third
            const arr = [start, second, third, last]
            return arr;
        },
        getRandomHeight(start, totalHeight) {
            console.log(start, totalHeight)
        }
    }
}
</script>

<style>
.attention_stable-widget {
    max-width: 800px;
    margin: 5px auto;
    background: white;
    padding: 30px;
    box-sizing: border-box;
}

.attention_stable-content .left-cards {
    position: absolute;
    left: 0;
    top: 0;
}


.attention_stable-content .right-cards {
    position: absolute;
    right: 0;
    top: 0;

}

.attention_stable-widget .choose-info span {
    display: inline-block;
    width: 150px;
    overflow: hidden;
}

.attention_stable-content {
    position: relative;
    height: 700px;
    width: 700px;
    margin: 30px auto;
    box-sizing: border-box;
    background-color: #ccc;
}


.attention_stable-content-cards {
    background: #ddd;
}


.attention_stable-content-cards.active {
    background: #787878;
}

.attention_stable-content-lines {
    position: absolute;
    display: inline-block;
    background-color: white;
    box-sizing: border-box;
    border: 1px solid hotpink;
}

.attention_stable-content-lines-count {
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