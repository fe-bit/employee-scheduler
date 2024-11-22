import './assets/main.css'
import { createApp } from 'vue'
import App from './App.vue'

import { createWebHistory, createRouter } from 'vue-router'
import TheWelcome from './components/TheWelcome.vue'
import EmployeesView from './views/EmployeesView.vue'
import SchedulesView from './views/SchedulesView.vue'



import VueDatePicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'


const routes = [
  { path: '/', component: TheWelcome },
  { path: '/employees', component: EmployeesView },
  { path: '/schedules', component: SchedulesView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

const app = createApp(App);
app.use(router)
app.component('VueDatePicker', VueDatePicker);
app.mount('#app');
