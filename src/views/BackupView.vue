<script setup lang="ts">
import { backupNames, updateBackupNames, loadingBackupNames } from '@/common/backup/backupNames';
import CreateBackupModal from '@/components/CreateBackupModal.vue';
import { FolderAddOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { createBackup } from '@/common/backup/backupActions';
import { onBeforeMount } from 'vue';

onBeforeMount(updateBackupNames);
</script>

<template>
  <div id="backup-view" class="view">

    <a-list v-bind="{
      dataSource: backupNames,
      bordered: true,
      loading: loadingBackupNames,
    }">

      <template #header>
        <div id="backup-list-header">

          <div id="backup-list-title">
            备份列表
            <a-tooltip color="blue" title="刷新备份列表">
              <a-button @click="updateBackupNames" v-bind="{
                type: 'link',
                size: 'small',
              }">
                <template #icon>
                  <SyncOutlined />
                </template>
              </a-button>
            </a-tooltip>
          </div>

          <a-button @click="createBackup" v-bind="{
            type: 'primary',
          }">
            <template #icon>
              <FolderAddOutlined />
            </template>
            创建备份
          </a-button>

        </div>
      </template>

      <template #renderItem="{ item }">
        <a-list-item>

          <template #actions>

            <a-button v-bind="{
              type: 'text',
              size: 'small',
              danger: true,
            }">
              删除
            </a-button>

          </template>

          {{ item }}

        </a-list-item>
      </template>

    </a-list>

    <CreateBackupModal />

  </div>
</template>

<style scoped>
#backup-list-header {
  display: flex;
  align-items: center;
  overflow-x: auto;
}

#backup-list-title {
  flex: 1 0;
  font-weight: bold;
}
</style>
