<template>
    <div class="paradigm-widgets">
        <div class="paradigm-header" v-if="show">
            <el-button @click="start">start</el-button>
            <el-button @click="stop">stop</el-button>
            <el-button @click="back">back</el-button>
        </div>
        <img v-for="imgpath in showImageArray" :src="imgpath" class="show-img">
        <div class="paradigm-red-circle"></div>
    </div>
</template>
<script>
import { startStream, stopStream, trigger , startFlashTask, msgListener} from '../api/index'
export default {
    data() {
        return {
            images: [],
            show: true,
            currentIndex: 0,
            showImageArray: [],
            targetIndex: 0,
            trialNumber: 5,
            totalTrial: 20,
            lantency: 83,
            instance: 83,
            trialLantency: 83,
            stopFlag: false,
            elem: []
        }
    },
    mounted() {
        this.preload()
        msgListener.add(this.trialEnd)
    },
    destroyed() {
    },
    methods: {
        trialEnd(res) {
            console.log(res)
        },  
        preload() {
            const params = this.$router.currentRoute.params
            const images = params.images
            this.targetIndex = params.targetIndex
            this.trialNumber = params.trialNumber
            this.totalTrial = params.totalTrial + 2
            this.lantency = params.lantency
            this.instance = params.instance
            this.trialLantency = params.trialLantency
            for (let key in images) {
                for (let imagePath in images[key]) {
                    const img = new Image()
                    images[key][imagePath] = 'file:///C:/Users/admin/Desktop/心理陈老师/web'+ images[key][imagePath] 
                    img.src = images[key][imagePath]
                    img.load = () => { }
                }
            }

            this.images = images
            setTimeout(() => {
                this.initParadigm()
            }, 1000);
        },
        initParadigm() {
            let bimgArray = new Array(this.images['b'].length).fill(0).map((item, index) => index)
            let oimgArray = new Array(this.images['o'].length).fill(0).map((item, index) => index)
            bimgArray = this.shuffle(bimgArray)
            oimgArray = this.shuffle(oimgArray)
            const imagePath = []
            for (let i = 0; i < this.totalTrial; i++) {
                for (let j = 0; j < this.trialNumber; j++) {
                    if (j == this.targetIndex - 1) {
                        const index = parseInt(Math.random() * oimgArray.length)
                        imagePath.push(this.images['o'][index])
                        continue
                    }
                    const index = parseInt(Math.random() * bimgArray.length)
                    imagePath.push(this.images['b'][index])
                }
            }
            this.showImageArray = imagePath
            
        },
        shuffle(arr) {
            let length = arr.length,
                randomIndex,
                temp;
            while (length) {
                randomIndex = Math.floor(Math.random() * (length--));
                temp = arr[randomIndex];
                arr[randomIndex] = arr[length];
                arr[length] = temp
            }
            return arr;
        },
        start() {
            setTimeout(() => {
                this.postPythonStartTask(this.$router.currentRoute.params)
            }, 1000);

        },
        stop() {
            this.show = true
            if (this.stopFlag) {
                return
            }
            stopStream('stop')
            this.stopFlag = true
        },
        back() {
            console.log('回到首页')
            this.stopFlag = true
            this.exitFullscreen()
            this.$router.back()
        },
        postPythonStartTask(data) {
            startFlashTask({...data, images: []})
        },
        startTask() {
            let index = 0
            let time = window.performance.now()
            while(1){
                let now = window.performance.now()
                console.log(now-time)
                if ( now -time < 83) {
                    time = now
                    continue
                }
                
                if (this.currentIndex >= this.showImageArray.length) {
                    this.stop()
                    break
                }
                if (index % 2 == 1) {
                    this.elem[this.currentIndex - 1].style.display = 'none'
                    index += 1
                    return
                }
                if ((this.currentIndex + 1) % this.trialNumber == this.targetIndex) {
                    trigger((parseInt(this.currentIndex / this.trialNumber) + 1))
                }
                if (this.currentIndex % this.trialNumber == 0) {
                    trigger(99)
                }
                if (this.currentIndex > 0) {
                    this.elem[this.currentIndex - 1].style.display = "none"
                }
                this.elem[this.currentIndex].style.display = 'block'
                index += 1
                this.currentIndex += 1
            }
        },
    }
}
</script>
<style>
.paradigm-widgets {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: gray;
}

.paradigm-header {
    position: absolute;
    left: 0;
    top: 30px;
    z-index: 100;
}

.show-img {
    position: absolute;
    left: 0;
    right: 0;
    width: 100%;
    height: 100%;
    display: none;
}

.paradigm-red-circle {
    position: absolute;
    width: 5px;
    height: 5px;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
    background-color: red;
    border-radius: 100%;
}
</style>