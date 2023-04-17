import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Custom from '../views/custom.vue'
import TimeSerise from '../views/TimeSerise.vue'
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
  }, {
    path: '/custom',
    name: 'Custom',
    component: Custom
  },
  {
    path: '/timeSerise',
    name: "TimeSerise",
    component: TimeSerise
  }
]

const router = new VueRouter({
  routes
})

export default router
