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
  }, {
    path: '/pannels',
    name: 'pannels',
    component: () => import('../views/pannels.vue')
  },
  {
    path: '/span-train',
    name: 'SpanTrain',
    component: () => import('../views/attention_span_training.vue')
  },
  {
    path: '/concentration-train',
    name: 'concentrationTrain',
    component: () => import('../views/attention_concentration_training.vue')
  }, {
    path: '/JigsawPuzzle-train',
    name: 'JigsawPuzzle',
    component: () => import('../views/attention_JigsawPuzzle_training.vue')
  }, {
    path: '/stable-train',
    name: 'stable',
    component: () => import('../views/attention_stable_training.vue')
  }, {
    path: '/inhibition-train',
    name: 'inhibition',
    component: () => import('../views/attention_inhibition_training/index.vue')
  }, {
    path: '/reaction-train',
    name: 'reaction',
    component: () => import('../views/attention_reaction_training/index.vue')
  }, {
    path: '/memory-train',
    name: 'memory',
    component: () => import('../views/attention_memory_training/index.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
