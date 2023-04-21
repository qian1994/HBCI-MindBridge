<template>
    <div class="header">
        <div class="logo-MindBridge" @click="homePage" >
        </div>
        <!-- <div class="header-btn-container"> <el-button type="paramy">主页</el-button> <el-button type=""> 产品文档</el-button>  <el-button type="">团队介绍</el-button></div> -->
        <div class="battery-container">
            <img class="battery battery-0" src="../../assets/battery-0.png" alt=""> <img class="battery battery-1" src="../../assets/battery-1.png" alt=""> <img class="battery battery-2" src="../../assets/battery-2.png" alt="">  <img class="battery battery-3" src="../../assets/battery-3.png" alt=""> <img class="battery battery-4" src="../../assets/battery-4.png" alt="">
        </div>
    </div>
</template>
<script>
import { homePage} from "../../api/index";

export default {
    name: 'Header',
    data(){
        return {
           
        }
    },
    methods: {
        homePage() {
            homePage()
        }
    },
    
}
</script>

<style>

.battery {
    display: none;
    width: 40px;
    position: absolute;
    top: 10px;
    right: 42px;
}

.logo-MindBridge {
    width: 54px;
    height: 54px;
    background: url('../../assets/logo_MindBridge.png');
    background-size: 100% 100%;
}

.header .logo-MindBridge img {
    height: 100%;
}

.header {
    box-sizing: border-box;
    height: 60px;
    line-height: 60px;
    background-color: white;
    position: relative;
}

.header-btn-container {
    position: absolute;
    right: 20px;
    top: 0;
}

.logo-img {
    width: 54px;
}
</style>