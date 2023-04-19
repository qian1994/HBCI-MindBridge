<template>
  <div id="app">
    <Header></Header>
    <el-menu 
        :default-active="activeIndex" 
        class="el-menu-demo menu"
        mode="horizontal" 
        router>
        <el-menu-item index="/impedence">阻抗测试</el-menu-item>
        <el-menu-item index="/home" >开始评估</el-menu-item>
        <el-menu-item index="/operate">评估配置</el-menu-item>
        <el-menu-item index="/result">评估结果</el-menu-item>

        <el-button class="backHome" type="warning" @click="homePage"> 回到首页</el-button>
    </el-menu>
    <router-view @PationInfo="getPationInfo"/>
  </div>
</template>
<script>
import { initDevTools, homePage, createNewExpriment } from './api/index'
import Header from './Components/header'
export default {
  components:{
    Header
  },
  data() {
    return {
      models: [],
      activeIndex: "/home"
    }
  },
  created() {
    initDevTools()
  },
  mounted() {
    const path = window.location.href.split('#')[1]
    this.activeIndex = path
    if (path == '/') {
      this.activeIndex = '/home'
    }
  },
  methods:{
    homePage() {
      homePage()
    },
    getPationInfo(info) {
      console.log('pationifo', info)
    }
  }
};
</script>
<style>
* {
  margin: 0;
  padding: 0;
}

html,
body {
  width: 100%;
  background: #F5F7FA;
}

.header{
  margin-bottom: 5px;
}

#app {
  height: 100%;
  box-sizing: border-box;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  position: relative;
}

.el-form-item__content {
  line-height: 30px;
  font-size: 12px;
}
.el-input__inner {
  height: 30px;
  line-height: 30px;
  font-size: 12px;
}
.el-input__icon {
  line-height: 30px;
}
.backHome {
  position: absolute;
  top: 10px;
  right: 20px;
}

#app .el-menu.el-menu--horizontal {
  border-bottom: none;
}

.el-menu-demo.menu {
  max-width: 900px;
  margin: 0 auto;
  position: relative;
}
</style>
