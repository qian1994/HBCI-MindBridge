import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
 {
    path: '/pannels',
    name: 'pannels',
    component:() => import('../views/pannels.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
