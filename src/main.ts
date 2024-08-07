// import './assets/main.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
// import cors from 'cors'


import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
// import SequenceQuery from rcsbsearchapi.search

const app = createApp(App)
// app.use(cors());
app.use(ElementPlus)
app.use(createPinia())
app.use(router)

app.mount('#app')
