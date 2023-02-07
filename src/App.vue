<script setup lang="ts">
import { RouterView, useRoute } from 'vue-router';
import {
  AppstoreOutlined, DatabaseOutlined, ExportOutlined,
  GithubOutlined, HomeOutlined, TableOutlined,
} from '@ant-design/icons-vue';
import { onMounted, provide, ref, watch, type Component } from 'vue';
import { updateTableNames } from './common/tableNames';
import locale from 'ant-design-vue/es/locale/zh_CN';
import { KEY_GET_CONTENT_CONTAINER } from './common/common';

const CONTENT_ID = 'content';
const getContentContainer = () => (
  document.getElementById(CONTENT_ID)
);
provide(KEY_GET_CONTENT_CONTAINER, getContentContainer);

onMounted(updateTableNames);

// eslint-disable-next-line no-undef
const VERSION = 'v' + __VERSION__;
const selectedMenuKeys = ref(['home']);

const route = useRoute();
watch(route, (rt) => {
  if (selectedMenuKeys.value[0] !== rt.name) {
    selectedMenuKeys.value = [rt.name as string];
  }
});

interface LinkInfo {
  name: string;
  icon: Component;
  text: string;
}

const links: LinkInfo[] = [
  { name: 'home', icon: HomeOutlined, text: '欢迎页面' },
  { name: 'table', icon: TableOutlined, text: '增删改查' },
  { name: 'export', icon: ExportOutlined, text: '生成报表' },
  { name: 'backup', icon: DatabaseOutlined, text: '数据备份' },
];
</script>

<template>
  <a-config-provider :locale="locale">
    <a-layout id="container">

      <a-layout-header id="header">
        <h1 id="header-title">
          志愿服务信息管理系统
          <code id="header-version">
          {{ VERSION }}
        </code>
        </h1>
        <a-button v-bind="{
          id: 'header-link',
          type: 'link',
          size: 'small',
          href: 'https://github.com/huang2002/volunteer-system',
        }">
          <GithubOutlined />
          huang2002
        </a-button>
      </a-layout-header>

      <a-layout>

        <a-layout-sider id="sider">

          <h2 id="sider-title">
            <a-space>
              <AppstoreOutlined />
              导航菜单
            </a-space>
          </h2>

          <a-menu id="sider-menu" theme="dark" v-model:selectedKeys="selectedMenuKeys">
            <a-menu-item v-for="link in links" :key="link.name" @click="$router.push({ name: link.name })">
              <a-space>
                <component :is="link.icon" />
                {{ link.text }}
              </a-space>
            </a-menu-item>
          </a-menu>

        </a-layout-sider>

        <a-layout-content :id="CONTENT_ID">
          <RouterView />
          <a-back-top v-bind="{
            target: getContentContainer,
            visibilityHeight: 200,
            title: '返回顶部',
            style: {
              right: '2em',
            },
          }" />
        </a-layout-content>

      </a-layout>

    </a-layout>
  </a-config-provider>
</template>

<style scoped>
#container {
  width: 100%;
  height: 100%;
}

#header {
  display: flex;
  padding: 0 2em;
  align-items: center;
  justify-content: space-between;
}

#header-title {
  display: inline-block;
  margin: 0;
  color: #FFF;
}

#header-version {
  color: #DDD;
  font-size: 0.8em;
}

#header-link {
  color: #FFF;
}

#sider {
  padding-top: 1em;
  background-color: #123;
  overflow: auto;
}

#sider-title {
  padding-left: 1em;
  color: #EEE;
}

#sider-menu {
  padding: 0.2em 0;
}

:deep(#sider-menu>.ant-menu-item) {
  padding-left: 2em;
}

#content {
  background-color: #EEE;
  overflow: auto;
}

.view {
  min-height: 100%;
  margin: 2em;
  padding: 2em;
  background-color: #FFF;
}
</style>
