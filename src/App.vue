<script setup lang="ts">
import { RouterView } from 'vue-router';
import { GithubOutlined, HomeOutlined, TableOutlined } from '@ant-design/icons-vue';
import { ref } from 'vue';

const selectedMenuKeys = ref(['home']);
</script>

<template>
  <a-layout id="container">
    <a-layout-header id="header">
      <h1 id="header-title">志愿服务信息管理系统</h1>
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
        <a-menu theme="dark" v-model:selectedKeys="selectedMenuKeys">
          <a-menu-item key="home" @click="$router.push('/')">
            <HomeOutlined />
            欢迎页面
          </a-menu-item>
          <a-menu-item key="table" @click="$router.push('/table')">
            <TableOutlined />
            查看/编辑
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

#header-link {
  color: #FFF;
}

#sider {
  padding-top: 1em;
  background-color: #123;
  overflow: auto;
}

#content {
  background-color: #EEE;
  padding: 2em;
  overflow: auto;
}

:deep(.view) {
  min-height: 100%;
  padding: 2em;
  background-color: #FFF;
}
</style>
