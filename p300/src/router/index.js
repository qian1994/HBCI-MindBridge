import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Paradigm from '../views/paradigm.vue'
import PationInfo from '../views/pationInfo.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/paradigm',
    name: 'paradigm',
    component: Paradigm
  }, {
    path: '/PationInfo',
    name: 'PationInfo',
    component: PationInfo
  }
]

const router = new VueRouter({
  routes
})

export default router
