//import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import lodash from 'lodash'
import axios from 'axios'


axios.defaults.withCredentials = true;
//axios.defaults.baseURL = 'http://192.168.86.137:8001/'
//已经启用vite代理
const app = createApp(App)

app.use(ElementPlus)
app.use(createPinia())
app.use(router)

app.mount('#app')
