import { createRouter, createWebHashHistory } from 'vue-router';
import HomeView from '@/views/HomeView.vue';
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
    component: () => import('@/views/TableView.vue'),
  }, {
    path: '/export',
    name: 'export',
    component: () => import('@/views/ExportView.vue'),
  }, {
    path: '/import',
    name: 'import',
    component: () => import('@/views/ImportView.vue'),
  }, {
    path: '/alias',
    name: 'alias',
    component: () => import('@/views/AliasView.vue')
  }, {
    path: '/backup',
    name: 'backup',
    component: () => import('@/views/BackupView.vue'),
  }],
});

router.beforeEach(() => {
  Modal.destroyAll();
});

export default router;
