import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import '@/assets/main.css';
import 'ant-design-vue/es/message/style/css';
import 'ant-design-vue/es/modal/style/css';

const app = createApp(App);

app.use(router);

app.mount('#app');
