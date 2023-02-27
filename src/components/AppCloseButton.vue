<script setup lang="ts">
import { PoweroffOutlined } from '@ant-design/icons-vue';
import { ref } from 'vue';

const closing = ref(false);
const closed = ref(false);
const closeApp = async () => {
  closing.value = true;
  try {
    await fetch('/api/close', { method: 'POST' });
  } finally {
    closed.value = true;
    closing.value = false;
  }
};
</script>

<template>
  <a-button @click="closeApp()" v-bind="{
    id: 'header-link',
    ghost: true,
    danger: true,
    shape: 'round',
    loading: closing,
  }">
    <template #icon>
      <PoweroffOutlined />
    </template>
    退出系统
  </a-button>

  <teleport to="#app">
    <a-result id="close-result" v-if="closed" status="warning">
      <template #title>
        后台程序已关闭
      </template>
      <template #subTitle>
        请关闭此页面以完全退出系统
      </template>
    </a-result>
  </teleport>
</template>

<style scoped>
#close-result {
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(6px);
  text-shadow: 0 0 10px #FFF;
  z-index: 9999;
}
</style>
