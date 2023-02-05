import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import TableView from '../views/TableView.vue';
import BackupView from '../views/BackupView.vue';
import ExportView from '../views/ExportView.vue';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [{
    path: '/',
    name: 'home',
    component: HomeView,
  }, {
    path: '/table/:tableName(\\d+)?',
    name: 'table',
    component: TableView,
  }, {
    path: '/backup',
    name: 'backup',
    component: BackupView,
  }, {
    path: '/export',
    name: 'export',
    component: ExportView,
  }],
});

export default router;
