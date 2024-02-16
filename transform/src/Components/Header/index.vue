<template>
    <div class="header">
        <div class="logo-MindBridge" @click="homePage" >
        </div>
        <div class="header-btn-container"> <el-button type="">Home Page</el-button> <el-button type=""> Document</el-button>  <el-button type="">Introduction</el-button></div>
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
    }
}
</script>

<style>
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