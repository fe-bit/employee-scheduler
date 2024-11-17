import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'

import { createWebHistory, createRouter } from 'vue-router'
import TheWelcome from './components/TheWelcome.vue'
import HelloWorld from './components/HelloWorld.vue'
import EmployeesView from './views/EmployeesView.vue'
import SchedulesView from './views/SchedulesView.vue'


const routes = [
  { path: '/', component: TheWelcome },
  { path: '/employees', component: EmployeesView },
  { path: '/schedules', component: SchedulesView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

createApp(App)
  .use(router)
  .mount('#app')
