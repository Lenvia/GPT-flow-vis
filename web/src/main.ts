import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

// import ElementPlus from 'element-plus';
import 'element-plus/dist/index.css'
// import {zhCn} from "element-plus/es/locale";

// Import Bootstrap and BootstrapVue CSS files (order is important)
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";


createApp(App)
    .use(store)
    .use(router)
    // .use(ElementPlus, {locale: zhCn}
    .mount('#app')
