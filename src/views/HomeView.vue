<script setup lang="ts">
import { FilePdfOutlined } from '@ant-design/icons-vue';

const REPO_URL = 'https://github.com/huang2002/volunteer-system';
</script>

<template>
  <a-typography id="home-view" class="view">
    <a-typography-title :level="2">
      欢迎使用“志愿服务管理系统”！
    </a-typography-title>
    <a-typography-paragraph>
      关于如何使用此系统，请参考文件夹中的
      <a-typography-text code>
        <FilePdfOutlined />
        说明书.pdf
      </a-typography-text>
      。
    </a-typography-paragraph>
    <a-typography-paragraph>
      如果发现系统本身有问题，
      或是有需要改进的地方，
      欢迎在Github上
      <a-typography-link v-bind="{
        href: `${REPO_URL}/issues`,
        target: '_blank',
      }">
        提交Issue
      </a-typography-link>
      进行反馈。
    </a-typography-paragraph><a-typography-paragraph>
      本项目的
      <a-typography-text strong>GitHub仓库</a-typography-text>
      ：
      <a-typography-link v-bind="{
        href: REPO_URL,
        target: '_blank',
      }">
        {{ REPO_URL }}
      </a-typography-link>
      。
    </a-typography-paragraph>
  </a-typography>
</template>

<style scoped>

</style>
