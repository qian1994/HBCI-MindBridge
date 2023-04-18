<template>
    <div class="paradigms-motion">
        <div class="content"></div>
        <div class="red-point"></div>
        <div></div>
    </div>
</template>
<script>
import { trigger, fullScreen, exitFullScreen, endSignalTrialTask, msgListener } from '../api/index'
export default {
    data() {
        return {
            timeDownCount: 3,
            elements: [],
            container:  null,
            with: screen.width,
            height: screen.height,
            params: {}
        }
    },
    created() {
      msgListener.add(this.getPageParams)  
    },
    async mounted() {
        document.querySelector('body').style.overflow = 'hidden'
        document.querySelector('.el-menu.el-menu--horizontal').style.display = 'none'
        document.querySelector('.header').style.display ='none'
        this.container = document.querySelector('.paradigms-motion .content')
        this.container.style.display = 'none'
    },
    destroyed(){
        document.querySelector('body').style.overflow = 'auto'
        document.querySelector('.el-menu-demo').style.display = 'block'
        document.querySelector('.header').style.display ='block'
    },
    methods:{
        getPageParams(res) {
            const params = JSON.parse(res)
            console.log(params)
            if (params && params['data'] == 'stop-flash') {
                return
            }
            this.timeDownCount = 3
            this.timmer = null
            this.timmer2 = null
            this.params = params
            for(let i = 0; i  < this.params.motionNumber; i++) {
                let x = this.with * Math.random()
                let y = this.height * Math.random()
                if(Math.sqrt(Math.pow(x-this.with/2, 2) + Math.pow(y-this.height/2, 2)) < this.params.motionDistance) {
                    continue
                }
                const div = document.createElement('div')
                div.className = 'circle'
                div.style.position = 'absolute'
                div.style.left = x + 'px'
                div.style.top = y + 'px'
                div.style.backgroundColor = 'white'
                this.elements.push(div)
                document.querySelector('.paradigms-motion .content').appendChild(div)
            }  
            setTimeout(() => {
                this.timeCount()
            }, 500);
        },
        timeCount() {
            this.container = document.querySelector('.paradigms-motion .content')
            this.timmer = setInterval(() => {
                if (this.timeDownCount <= 0) {
                    document.querySelector('.red-point').innerHTML=''
                    document.querySelector('.red-point').style.background = 'red'
                    document.querySelector('.red-point').style.with = "10px"
                    document.querySelector('.red-point').style.height = "10px"
                    clearInterval(this.timmer)
                    this.taskStart()
                    return
                }
                document.querySelector('.red-point').innerHTML=this.timeDownCount
                document.querySelector('.red-point').style.background = ''
                document.querySelector('.red-point').style.with = "50px"
                document.querySelector('.red-point').style.height = "50px"
                this.timeDownCount -=1
            }, 1000);
        },
        async endSignalTrialTask() {
            clearInterval(this.timmer)
            await endSignalTrialTask()
        },
        taskStart() {
            let count = 0
            trigger(-1)
            let targetIndex = this.params.targetIndex
            let totalTrial = this.params.totalTrial
            let trialNumber = this.params.trialNumber
            this.timmer = setInterval(async () => {
                if (count > totalTrial * trialNumber * 2) {
                    this.endSignalTrialTask()
                    clearInterval(this.timmer)
                    return
                }
                if (count % 2 == 0) {
                    clearInterval(this.timmer2)
                    this.container.style.transform = "rotate(0deg)";
                    this.container.style.display = 'none'
                }else {
                    this.container.style.display = 'block'
                    if(count % trialNumber == 0) {
                        trigger(1)
                    } 
                    if (count % 5 == targetIndex) {
                        let edg = 0
                        trigger(2)
                        this.timmer2 = setInterval(() => {
                            this.container.style.transform = "rotate("+edg * 7+"deg)";
                            edg +=1
                        }, 16)
                    }
                }
                count += 1
            }, 83);
        }
    }
}

</script>
<style>

.paradigms-motion {
    background-color: gray;
    width: 100%;
    height: 100%;
    position: fixed;
    z-index: 1000;
    overflow: hidden;
}

.content{
    width: 100%;
    height: 100%;
}


.circle {
    width: 3px;
    height: 3px;
    border-radius: 100%;
}

.red-point {
    position: fixed;
    left: 50%;
    top: 50%;
    width: 10px;
    height: 10px;
    transform: translate(-50%, -50%);
    font-size: 50px;
    color: red;
}
</style>
  