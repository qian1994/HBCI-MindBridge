import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  }
  ,{
    path: '/result',
    name: 'result',
    component:() => import('../views/result.vue')
   }, {
    path: '/operate',
    name: 'operate',
    component:() => import('../views/operate.vue')
   }
]

const router = new VueRouter({
  routes
})

export default router
