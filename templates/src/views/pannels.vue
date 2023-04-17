<template>
    <div class="pannels-widgets">
        <TopNav :connectSession="false"></TopNav>
         <div class="pannels-header">
            <el-button type="primary" v-if="!isStartStream" @click="_startStream" plain> 开始</el-button>
            <el-button type="danger" v-else @click="_stopStream" plain> 结束</el-button>
        </div>
        <div>
            <TimeSerise></TimeSerise>
        </div>
    </div>
</template>
<script>
import TopNav from "../Components/topNav/index.vue"
import { startStream, stopStream, stopSession } from "../api";
import TimeSerise from '../Components/timeserise/index.vue'
export default {
    data() {
        return{
            isStartStream: false
        }
    },
    components:{
       TopNav,
       TimeSerise
    },
    methods:{
        _startStream() {
            startStream().then((Response) => {
                this.isStartStream = true;
            }).catch((error) => {
                console.error(error)
            })
        },
        _stopStream() {
            stopStream().then((Response) => {
                this.isStartStream = false;
            }).catch((error) => {
                console.error(error)
            })
        },
        _stopSession() {
            stopSession()
        }
    }
}
</script>
