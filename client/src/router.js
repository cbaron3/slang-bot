import Vue from 'vue'
import Router from 'vue-router'
import Ping from './components/Ping.vue'
import HomePage from './components/HomePage.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'HomePage',
      component: HomePage,
    },
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    }
  ],
});
