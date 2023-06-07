import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
// import HomeView from '../views/HomeView.vue'
import TestView from "@/views/TestView.vue";
import MainView from "@/views/MainView.vue";

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'main',
    component: MainView
  },

  {
    path:'/test',
    name:'test',
    component: TestView
  },

  {
    path: '/main',
    name: 'main',
    component: MainView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
