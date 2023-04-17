<template>
    <div class="warning-widgets">
        <div class="warning-content">
            <div> <span class="red-point-watch"></span></div>
            <p>
                实验过程，请根据关注红点
            </p>
        </div>
        <div class="warning-header" v-if="show">
            <el-button class="enter-button" @click="start" v-if="currentTrial == 0">开始实验</el-button>
            <el-button class="enter-button" @click="nextTrial" v-if="currentTrial != 0">下一轮</el-button>
            <el-button class="enter-button" v-if="currentTrial > 0" @click="endTotal" type="primary">实验结束</el-button>
        </div>
        <div class="">
            <div class="total-trial">
                <span></span><el-button v-for="item in totalTrialButton"
                    :type="goodTrial.indexOf(item - 1) >= 0 ? 'primary' : 'info'" @click="troggle(item)">trial : {{ item
                    }}</el-button>
            </div>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import { startFlashTask, msgListener, endTrialTask, endTotalTask, startSession, initDevTools , openParamsWindow} from '../api/index'
export default {
    data() {
        return {
            images: [],
            show: true,
            selectral: 0,
            showImageArray: [],
            stopFlag: false,
            currentTrial: 0,
            badTrial: [],
            goodTrial: [],
            motionParams: {},
            params: {}
        }
    },
    mounted() {
        this.preload()
        msgListener.add(this.getMessageFromServe)
        this.openWindow()
    },
    computed: {
        totalTrialButton() {
            return new Array(this.currentTrial).fill(0).map((item, index) => {
                return index + 1
            })
        }
    },
    
    methods: {
        async openWindow() {
            const res = await openParamsWindow()
        },
        troggle(data) {
            let index = parseInt(data) - 1
            let array = this.goodTrial
            if (array.indexOf(index) >= 0) {
                this.goodTrial = array.filter(el => el != index)
            } else {
                Vue.set(this.goodTrial, this.goodTrial.length, index)
            }
            this.goodTrial = this.goodTrial.sort((a, b) => { return a - b })
        },
        getMessageFromServe(res) {
            const data = JSON.parse(res)
            if (data.data == "stop-flash") {
                this.flashTaskEnd()
            }
            if (data.data == 'sucess-save-data') {
                this.$router.push({ name: 'Home', params: { 'activeName': "3" } })
            }
        },
        flashTaskEnd() {
            setTimeout(() => {
                endTrialTask()
            }, 1000);
        },
        preload() {
            let params = {}
            if (localStorage.getItem('config')) {
                params = JSON.parse(localStorage.getItem('config'))
            }
            this.params = params
            const images = params.images || []
            this.targetIndex = params.targetIndex
            this.trialNumber = params.trialNumber
            this.totalTrial = params.totalTrial
            this.lantency = params.lantency
            this.instance = params.instance
            this.trialLantency = params.trialLantency
            this.selectModel = params.selectModel
            this.motionParams = {
                motionNumber: params.motionNumber,
                motionDistance: params.motionDistance,
                motionWidth: params.motionWidth,
                motionHeight: params.motionHeight,
                motionSpeed: params.motionSpeed,
                motionInstance: params.instance,
                targetIndex: params.targetIndex,
                trialNumber: params.trialNumber,
                totalTrial: params.totalTrial
            }
            // if (this.$router.currentRoute.params && this.$router.currentRoute.params.currentTrialIndex) {
            //     this.currentTrial = this.$router.currentRoute.params.currentTrialIndex
            // }

            // if (this.$router.currentRoute.params && this.$router.currentRoute.params.goodTrial) {
            //     this.goodTrial = this.$router.currentRoute.params.goodTrial
            // }
        },
        async start() {
            this.currentTrial += 1
            this.troggle(this.currentTrial)
            startFlashTask({ ...this.params, images: [] })
        },
        async back() {
            this.stopFlag = true
            this.$router.back()
        },
        async endTotal() {
            const trial = this.totalTrialButton.map(item => {
                return this.goodTrial.indexOf(item - 1) >= 0 ? 1 : 0
            })
            const res = await endTotalTask({...this.$router.currentRoute.params, trial: trial})
            if (res == 'ok') {
                const config = JSON.parse(localStorage.getItem('config'))
                config.passedImpedence = true
                localStorage.setItem('config', JSON.stringify(config))
                this.$router.push({ name: 'pationInfo', params: { "status": "end-task", "additional": trial.join(',') } })
            }
        },
        nextTrial() {
            this.currentTrial += 1
            this.troggle(this.currentTrial)
            startFlashTask({ ...this.params, images: [] })
        }
    }
}
</script>
<style>
.warning-widgets {
    position: relative;
    text-align: left;
    padding: 30px;
    box-sizing: border-box;
    max-width: 900px;
    margin-left: auto;
    margin-right: auto;
    box-sizing: border-box;
    background-color: white;
}

.warning-header {
    text-align: center
}

.warning-content {
    font-size: 20px;
    text-align: center;
    font-weight: 400;
    color: #3D3D3D;
    line-height: 24px;
    font-size: 18px;
    margin-bottom: 34px;
}

.total-trial {
    margin: 30px 0;
}

.total-trial .el-button {
    margin-bottom: 20px;
}

.red-point-watch {
    display: inline-block;
    height: 20px;
    width: 20px;
    background-color: red;
    border-radius: 100%;
    margin: 34px 0;
}

.enter-button {
    width: 150px;
}
</style>