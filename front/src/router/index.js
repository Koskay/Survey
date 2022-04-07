import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Survey from '../views/Survey.vue'
import Questions from "@/views/Questions";
import Statistic from "@/views/Statistic";


Vue.use(VueRouter)

const routes = [
  {
    path: '',
    name: 'Login',
    component: Login
  },

  {
    path: '/survey/',
    name: 'Survey',
    component: Survey,
    props: true
  },
  {
    path: '/questions/:id/',
    name: 'Questions',
    component: Questions,
    props: true
  },
  {
    path: '/statistic/:id/',
    name: 'Statistic',
    component: Statistic,
    props: true
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
