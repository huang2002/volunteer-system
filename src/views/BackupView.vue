<script setup lang="ts">
import { backupList, updateBackupList, loadingBackupNames } from '@/shared/backup/backupList';
import CreateBackupModal from '@/components/BackupNameModal.vue';
import { FolderAddOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { createBackup } from '@/shared/backup/backupActions';
import { onBeforeMount } from 'vue';
import BackupListItem from '@/components/BackupListItem.vue';

onBeforeMount(() => {
  updateBackupList(false);
});
</script>

<template>
  <div id="backup-view" class="view">

    <a-list v-bind="{
      dataSource: backupList,
      bordered: true,
      loading: loadingBackupNames,
    }">

      <template #header>
        <div id="backup-list-header">

          <h2 id="backup-list-title">
            备份列表
          </h2>

          <a-button @click="updateBackupList(true)" v-bind="{
            id: 'backup-list-refresh',
            type: 'link',
            size: 'small',
          }">
            <template #icon>
              <SyncOutlined />
            </template>
            刷新
          </a-button>

          <a-button @click="createBackup(true)" v-bind="{
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
        <BackupListItem :item="item" />
      </template>

    </a-list>

    <CreateBackupModal />

  </div>
</template>

<style scoped>
#backup-view {
  padding: 32px;
}

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
