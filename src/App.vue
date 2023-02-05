<script setup lang="ts">
import { RouterView } from 'vue-router';
import { AppstoreOutlined, DatabaseOutlined, ExportOutlined, GithubOutlined, HomeOutlined, TableOutlined } from '@ant-design/icons-vue';
import { onBeforeMount, ref } from 'vue';
import { updateTableNames } from './common/tableNames';

// eslint-disable-next-line no-undef
const VERSION = 'v' + __VERSION__;
const selectedMenuKeys = ref(['home']);

onBeforeMount(updateTableNames);
</script>

<template>
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
          <a-menu-item key="home" @click="$router.push('/')">
            <a-space>
              <HomeOutlined />
              欢迎页面
            </a-space>
          </a-menu-item>
          <a-menu-item key="table" @click="$router.push('/table')">
            <a-space>
              <TableOutlined />
              增删改查
            </a-space>
          </a-menu-item>
          <a-menu-item key="export" @click="$router.push('/export')">
            <a-space>
              <ExportOutlined />
              生成报表
            </a-space>
          </a-menu-item>
          <a-menu-item key="backup" @click="$router.push('/backup')">
            <a-space>
              <DatabaseOutlined />
              数据备份
            </a-space>
          </a-menu-item>
        </a-menu>

      </a-layout-sider>

      <a-layout-content id="content">
        <RouterView />
      </a-layout-content>

    </a-layout>

  </a-layout>
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
  padding: 2em;
  overflow: auto;
}

.view {
  min-height: 100%;
  padding: 2em;
  background-color: #FFF;
}
</style>
