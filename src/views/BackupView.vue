<script setup lang="ts">
import { backupNames, updateBackupNames, loadingBackupNames } from '@/shared/backup/backupNames';
import CreateBackupModal from '@/components/BackupNameModal.vue';
import { FolderAddOutlined, SyncOutlined, FolderOutlined } from '@ant-design/icons-vue';
import { createBackup, renameBackup, deleteBackup } from '@/shared/backup/backupActions';
import { onBeforeMount } from 'vue';
import { onRefreshSuccess } from '@/shared/common';

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

          <h2 id="backup-list-title">
            备份列表
          </h2>

          <a-button @click="updateBackupNames(onRefreshSuccess)" v-bind="{
            id: 'backup-list-refresh',
            type: 'link',
            size: 'small',
          }">
            <template #icon>
              <SyncOutlined />
            </template>
            刷新
          </a-button>

          <a-button @click="createBackup()" v-bind="{
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

            <a-button @click="renameBackup(item as string)" v-bind="{
              type: 'link',
              size: 'small',
            }">
              重命名
            </a-button>

            <a-button @click="deleteBackup(item as string)" v-bind="{
              type: 'link',
              size: 'small',
              danger: true,
            }">
              删除
            </a-button>

          </template>

          <a-space :title="item">
            <FolderOutlined style="color: #F90;" />
            {{ item }}
          </a-space>

        </a-list-item>
      </template>

    </a-list>

    <CreateBackupModal />

  </div>
</template>

<style scoped>
#backup-list-header {
  display: flex;
  align-items: baseline;
  overflow-x: auto;
}

#backup-list-title {
  margin: 0;
  margin-right: 10px;
  font-weight: bold;
}

#backup-list-refresh {
  margin-right: auto;
}
</style>
