import { createApp } from 'vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import App from './App.vue'
import router from './router'
import store from './store'

import timeFormater from "time-formater";

import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)

app.config.globalProperties.$moment = timeFormater;

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

// 注册全局组件
import ReaderBanner from '@/components/ReaderBanner';
import AdminBanner from '@/components/AdminBanner';

app.component(ReaderBanner.name, ReaderBanner);
app.component(AdminBanner.name, AdminBanner);

app.use(store).use(router).use(ElementPlus).mount('#app')
