import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
import TableView from '@/views/TableView.vue';
import ExportView from '@/views/ExportView.vue';
import ImportView from '@/views/ImportView.vue';
import BackupView from '@/views/BackupView.vue';
import { Modal } from 'ant-design-vue';

const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [{
    path: '/',
    name: 'home',
    component: HomeView,
  }, {
    path: '/table',
    name: 'table',
    component: TableView,
  }, {
    path: '/export',
    name: 'export',
    component: ExportView,
  }, {
    path: '/import',
    name: 'import',
    component: ImportView,
  }, {
    path: '/backup',
    name: 'backup',
    component: BackupView,
  }],
});

router.beforeEach(() => {
  Modal.destroyAll();
});

export default router;
