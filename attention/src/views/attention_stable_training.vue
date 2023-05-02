<template>
    <div class="attention_stable-widget">
        <div v-if="start" class="choose-info"> <span>用时: {{ timmerShow }}</span> <span>总共： {{ formData.count}}</span>
            <span>剩余： {{ formData.count - trainResultTotal.length }}</span> <span>错误次数: {{ currentTrainResult.errorNumber
            }}</span></div>
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
        <div class="attention_stable-content" v-if="start">
            <div class="left-cards">
                <div v-for="item, index in findPairs[0]" 
                :class="['attention_stable-content-cards', currentChooseId===index ? 'active' : '']"  
                    :style="`${cardStyle[0][index]['style']}`"
                    @click="choose(index)">
                    {{item}}
                </div>
            </div>
            <div class="right-cards">
                <div 
                v-for="item, index in findPairs[1]" 
                :class="['attention_stable-content-cards', currentChooseItem===index >= 0 ? 'active' : '']"  
                :style="`${cardStyle[1][index]['style']}`" @click="chooseItem(index)">
                    {{item}}
                </div>
            </div>
            <div v-if="lines" v-for="item, index in lines" >
                <div v-if="rightArray.indexOf(index) == -1" v-for="line in lines[index]" class="attention_stable-content-lines" :style="`width:${line['width']}px; top:${line['top']}px; left: ${line['left']}px; height: ${line['height']}px`"></div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
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
            currentChooseItem:''
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
            let arr1 = new Array(this.numberCards).fill(0).map((item, index) => index+1)
            let arr2 = new Array(this.numberCards).fill(0).map((item, index) => String.fromCharCode(index + 'A'.charCodeAt()))
            return [arr1, arr2]
        },
        cardStyle() {
            return this.findPairs.map(cards => {
                return cards.map((item, index) => {
                    return {
                        style: `width:${700/cards.length}px; height: ${700/cards.length}px; text-align: center;  line-height:  ${700/cards.length}px;color: white; border-bottom: 1px solid white; box-sizing: border-box;`
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
    mounted() {
    },
    methods: {
        submit() {
            this.timmer = setInterval(() => {
                this.currentTrainResult.time += 100
            }, 100);
            this.start = true
            this.showLines()
        },
        showLines() {
            const sigleCardHeight = this.totalHeight / this.numberCards
            this.shuffleIndex = new Array(this.numberCards ).fill(0).map((item, index) => index).sort(() => Math.random() - 0.5);
            const lines = this.shuffleIndex.map((item, index) => {
                let widths = this.generateRandomNumbers(index).map(item => item *  (this.totalHeight - 2 * sigleCardHeight) )
                let topStartPoint = index * sigleCardHeight + sigleCardHeight / 2
                let topEndPoint = item * sigleCardHeight + sigleCardHeight / 2
                let topPoint1 = 0
                let topPoit2 = 0
                if (index < this.shuffleIndex.length / 2) {
                    topPoint1 = this.totalHeight / 2 +  (this.totalHeight - sigleCardHeight) / 2  * Math.random()
                    topPoit2 = (this.totalHeight - sigleCardHeight) / 2  * Math.random()
                }else {
                    topPoint1 = (this.totalHeight - sigleCardHeight) /2  * Math.random() + sigleCardHeight / 2
                    topPoit2 = this.totalHeight / 2 +  (this.totalHeight - sigleCardHeight) /2  * Math.random()
                }
                const positions = [
                    {
                        top: topStartPoint,
                        left: sigleCardHeight ,
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
                        left:sigleCardHeight + widths[0] + widths[1] + widths[2]
                    }, {
                        top: topEndPoint,
                        left: sigleCardHeight + widths[0] + widths[1] + widths[2]
                    }, {
                        top: topEndPoint,
                        left:sigleCardHeight + widths[0] + widths[1] + widths[2] + widths[3]
                    }
                ]
                let element = []
                for (let i = 0; i < positions.length; i ++) {
                    if (i == 0) {
                        continue
                    }
                    element.push({
                        left: positions[i-1]['left'],
                        width:( positions[i]['left'] - positions[i-1]['left']) || 2,
                        top: positions[i]['top'] > positions[i-1]['top'] ? positions[i-1]['top']: positions[i]['top'],
                        height: Math.abs(positions[i]['top'] - positions[i-1]['top']) || 2
                    })
                }
                return element
            })
            this.lines = lines
        },
        endTotalTask() {
            console.log('end total task')
        },
        reStart() {
            console.log('this is re start')
            if (this.timmer) {
                clearInterval(this.timmer)
            }
            this.trainResultTotal.push({
                time: this.currentTrainResult.time,
                errorNumber: this.currentTrainResult.errorNumber,
                level: this.formData.level
            })
            this.currentTrainResult.time = {
                time: 0,
                errorNumber: 0
            }
            this.rightArray = []
            this.showLines()
            this.timmer = setInterval(() => {
                console.log(this.currentTrainResult.time)
                this.currentTrainResult.time += 100
            }, 100);
        },
        choose(index) {
            if (this.currentChooseItem === '') {
                this.currentChooseId = index
                return
            }

            if( this.shuffleIndex[this.currentChooseItem] == index) {
                this.rightArray.push(this.currentChooseId)
            }else {
                this.currentTrainResult.errorNumber += 1
                return 
            }
            this.currentChooseItem = ''
            this.currentChooseId = '' 
            console.log(this.rightArray)
            if (this.rightArray.length < this.shuffleIndex) {
                return
            }

            this.currentIndex +=1
            if (this.currentIndex > this.formData.count) {
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
            if(this.currentChooseId == this.shuffleIndex.indexOf(index)) {
                this.rightArray.push(this.currentChooseId)
            }else {
                this.currentTrainResult.errorNumber += 1
                return
            }

            this.currentChooseItem = ''
            this.currentChooseId = '' 
            console.log(this.rightArray)
            if (this.rightArray.length < this.shuffleIndex.length) {
                return
            }

            this.currentIndex+=1
            if (this.currentIndex > this.formData.count) {
                this.endTotalTask()
                return
            }

            this.reStart()
        },
        generateRandomNumbers(index) {
            const start = 0.05 + index / this.numberCards * 0.37
            const second = 0.235
            const third = 0.235
            const last = 1  - start - second - third
            const arr = [start, second, third, last] 
            return arr;
        },
        getRandomHeight(start,totalHeight) {
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


.attention_stable-content-cards{
    background:  #ddd;
}


.attention_stable-content-cards.active{
    background:  #787878;
}

.attention_stable-content-lines {
    position: absolute;
    display: inline-block;
    background: red;
}
</style>