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
  },
 {
    path: '/paradigm',
    name: 'paradigm',
    component:() => import('../views/paradigm.vue')
  },
  {
     path: '/enter',
     name: 'enter',
     component:() => import('../views/enter.vue')
   },{
    path: '/impedence',
    name: 'impedence',
    component:() => import('../views/impedence.vue')
   }, {
    path: '/pationInfo',
    name: 'pationInfo',
    component:() => import('../views/pationInfo.vue')
   }, {
    path: '/operate',
    name: 'operate',
    component:() => import('../views/operate.vue')
   },{
    path: '/create-image',
    name: 'create-image',
    component:() => import('../views/createimage.vue')
   }, {
    path: '/motion',
    name: 'motion',
    component:() => import('../views/motion.vue')
   },{
    path: '/result',
    name: 'result',
    component:() => import('../views/result.vue')
   }
]

const router = new VueRouter({
  routes
})

export default router
