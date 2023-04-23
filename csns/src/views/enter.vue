<template>
    <div class="warning-widgets">
        <div class="warning-content">
            <div> <span class="red-point-watch"></span></div>
            <p>
                实验过程，请根据关注红点
            </p>
        </div>
        <div class="warning-header" v-if="show">
            <el-button class="enter-button" :disabled="!stopFlashed" @click="start"
                v-if="currentTrial == 0">开始实验</el-button>
            <el-button class="enter-button" :disabled="!stopFlashed" @click="nextTrial"
                v-if="currentTrial != 0">下一轮</el-button>
            <el-button class="enter-button" :disabled="!stopFlashed" v-if="currentTrial > 0" @click="endTotal"
                type="primary">实验结束</el-button>
        </div>
        <div class="">
            <div class="total-trial">
                <span></span><el-button :disabled="!stopFlashed" v-for="item in totalTrialButton"
                    :type="goodTrial.indexOf(item - 1) >= 0 ? 'primary' : 'info'" @click="troggle(item)">trial : {{ item
                    }}</el-button>
            </div>
        </div>
        <div>
            <h3>通道选择：</h3>
            <ElectrodePositions :show-info="showChannels" :radius="radius" @point-click="toggle"></ElectrodePositions>
        </div>
    </div>
</template>
<script>
import Vue from 'vue'
import ElectrodePositions from '../Components/HeadPlot/electrodePositions.vue'

import {
    startFlashTask,
    msgListener,
    endTotalTask,
    startSession,
    initDevTools,
    openParamsWindow,
    getConfigFromServe,
    postSelectChannel,
    getTimeSeriseChannelShow

} from '../api/index'
export default {
    data() {
        return {
            radius: 400,
            images: [],
            show: true,
            selectral: 0,
            showImageArray: [],
            stopFlag: false,
            currentTrial: 0,
            badTrial: [],
            goodTrial: [],
            params: {},
            stopFlashed: true,
            channels: [],
            products: [],
            selectChannels: []
        }
    },
    mounted() {
        this.preload()
        msgListener.add(this.getMessageFromServe)
        this.openWindow()
        setTimeout(async () => {
            const data = await getConfigFromServe("msg")
            this.channels = JSON.parse(data)['channels']
            this.products = JSON.parse(data)['products']
            const channels = await getTimeSeriseChannelShow()
            this.selectChannels = channels
        }, 300);
    },
    components: {
        ElectrodePositions
    },
    computed: {
        totalTrialButton() {
            return new Array(this.currentTrial).fill(0).map((item, index) => {
                return index + 1
            })
        },
        showChannels() {
            let channels = []
            if (this.$router.currentRoute.params.productId == '5') {
                channels = this.channels['8']
            }
            if (this.$router.currentRoute.params.productId == '516') {
                channels = this.channels["16"]
            }
            if (this.$router.currentRoute.params.productId == '520') {
                channels = this.channels["20"]
            }
            if (this.$router.currentRoute.params.productId == '532') {
                channels = this.channels['32']
            }
            if (this.$router.currentRoute.params.productId == '564') {
                channels = this.channels['64']
            }
            if (!channels || !channels.length) {
                return []
            }
            let info = {}
            this.currentChannels = channels
            channels.forEach((item, index) => {
                info[item] = {
                    switch: this.selectChannels.indexOf(item) >= 0 ? true : false,
                    label: item,
                    show: 'switch',
                    name: item,
                }
            })
            return info
        }
    },

    methods: {
        async openWindow() {
            const res = await openParamsWindow()
        },
        toggle(point) {
            const channel = point['label']
            if (this.selectChannels.indexOf(channel) >= 0) {
                this.selectChannels = this.selectChannels.filter(item => item != channel)
            } else {
                this.selectChannels.push(channel)
            }
            postSelectChannel(this.selectChannels)
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
                this.stopFlashed = true
            }, 100);
        },
        preload() {
            let params = {}
            if (localStorage.getItem('config')) {
                params = JSON.parse(localStorage.getItem('config'))
            }
            this.params = params

        },
        async start() {
            this.stopFlashed = false
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
            const res = await endTotalTask({ ...this.$router.currentRoute.params, trial: trial })
            if (res == 'ok') {
                this.$message('数据保存成功')
                localStorage.setItem('config', JSON.stringify(this.params))
                setTimeout(() => {
                    this.$router.push({ name: 'home' })
                }, 1000);
            }
        },
        nextTrial() {
            this.stopFlashed = false
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