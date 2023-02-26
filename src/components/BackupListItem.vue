<script setup lang="ts">
import { loadBackup, renameBackup, deleteBackup } from '@/shared/backup/backupActions';
import type { BackupItem } from '@/shared/backup/backupList';
import { DeleteOutlined, EditOutlined, FolderTwoTone, SyncOutlined } from '@ant-design/icons-vue';
import { computed } from 'vue';

const props = defineProps<{
  item: BackupItem;
}>();

const description = computed(() => {
  const tableCount = props.item.tables.length;
  if (tableCount) {
    return `包含${tableCount}张表格：${props.item.tables.join('、')}。`;
  } else {
    return '不包含任何表格。';
  }
});
</script>

<template>
  <a-list-item>

    <template #actions>

      <a-button @click="loadBackup(item.name, true)" v-bind="{
        type: 'link',
        size: 'small',
      }">
        <template #icon>
          <SyncOutlined />
        </template>
        加载
      </a-button>

      <a-button @click="renameBackup(item.name, true)" v-bind="{
        type: 'link',
        size: 'small',
        style: {
          color: '#F90',
        },
      }">
        <template #icon>
          <EditOutlined />
        </template>
        重命名
      </a-button>

      <a-button @click="deleteBackup(item.name, true)" v-bind="{
        type: 'link',
        size: 'small',
        danger: true,
      }">
        <template #icon>
          <DeleteOutlined />
        </template>
        删除
      </a-button>

    </template>

    <a-list-item-meta v-bind="{
      title: item.name,
    }">
      <template #avatar>
        <FolderTwoTone two-tone-color="#F90" style="font-size: 1.6em;" />
      </template>
      <template #description>
        <a-typography-text v-bind="{
          type: 'secondary',
          ellipsis: true,
          title: description,
          content: description,
        }" />
      </template>
    </a-list-item-meta>

  </a-list-item>
</template>
