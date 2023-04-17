<template>
    <div class="fft-config">
        <div>
            <el-button type="primary" @click="openFFT">打开功率谱图</el-button>
            <el-button type="success" @click="home">返回首页</el-button>
        </div>
    </div>
</template>
<script>
import { openRealTimeFFT, homePage, getConfigFromServe, postSelectChannel, initDevTools, getCurrentBoardData } from '../../api/index'

export default {
    name: 'fft-config',
    data() {
        return {
           
        }
    },
    methods: {
        openFFT() {
            
            openRealTimeFFT('')
        },
        home() {
            homePage()
        }
    }
}
</script>

<style>

</style>