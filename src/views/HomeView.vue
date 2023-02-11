<script setup lang="ts">
import { BranchesOutlined, ExclamationCircleOutlined, FilePdfOutlined, GithubOutlined, ReadOutlined } from '@ant-design/icons-vue';

// eslint-disable-next-line no-undef
const VERSION = 'v' + __VERSION__;
const REPO_PATH = 'huang2002/volunteer-system';
const REPO_URL = 'https://github.com/' + REPO_PATH;
</script>

<template>
  <a-typography id="home-view" class="view">

    <a-typography-title :level="2">
      欢迎使用“志愿服务管理系统”！
    </a-typography-title>

    <a-typography-paragraph>
      <a-space size="middle" align="start">
        <BranchesOutlined />
        <span>
          当前系统版本：
          <a-typography-text code>
            {{ VERSION }}
          </a-typography-text>
          。
        </span>
      </a-space>
    </a-typography-paragraph>

    <a-typography-paragraph>
      <a-space size="middle" align="start">
        <ReadOutlined />
        <span>
          关于如何使用此系统，请参考文件夹中的
          <a-typography-text code>
            <FilePdfOutlined />
            使用手册.pdf
          </a-typography-text>
          。
        </span>
      </a-space>
    </a-typography-paragraph>

    <a-typography-paragraph>
      <a-space size="middle" align="start">
        <ExclamationCircleOutlined />
        <span>
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
        </span>
      </a-space>
    </a-typography-paragraph>

    <a-typography-paragraph>
      <a-space size="middle" align="start">
        <GithubOutlined />
        <span>
          本项目的
          <a-typography-text strong>GitHub仓库</a-typography-text>
          ：
          <a-typography-link v-bind="{
            href: REPO_URL,
            target: '_blank',
          }">
            {{ REPO_PATH }}
          </a-typography-link>
          。
        </span>
      </a-space>
    </a-typography-paragraph>

  </a-typography>
</template>

<style scoped>
#home-view {
  padding: 24px 32px;
}
</style>
