import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Paradigm from '../views/paradigm.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/paradigm',
    name: 'paradigm',
    component: Paradigm
  }
]

const router = new VueRouter({
  routes
})

export default router
