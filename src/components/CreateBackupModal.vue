<script setup lang="ts">
import { merge } from '3h-utils';
import { createBackupModalCallback, createBackupModalState, createBackupModalVisible, createBackupModalPending, createBackupModalForm } from '@/common/backup/createBackupModal';

const onSubmit = () => {
  createBackupModalCallback.value?.(merge(createBackupModalState));
  createBackupModalPending.value = true;
};

const onCancel = () => {
  createBackupModalCallback.value?.(null);
  createBackupModalVisible.value = false;
};
</script>

<template>
  <a-modal v-model:visible="createBackupModalVisible" @ok="onSubmit" @cancel="onCancel" v-bind="{
    title: '创建备份',
    footer: null,
    confirmLoading: createBackupModalPending,
  }">

    <a-alert type="info" show-icon>
      <template #message>备份名称格式</template>
      <template #description>
        建议使用“时间+名称”的格式，方便日后管理。
      </template>
    </a-alert>

    <a-form ref="createBackupModalForm" @finish="onSubmit" v-bind="{
      id: 'create-backup-form',
      model: createBackupModalState,
      labelCol: { span: 5, offset: 3 },
      wrapperCol: { span: 10 },
    }">

      <a-form-item name="name" label="备份名称" :rules="[{
        required: true,
        pattern: /^\d{2}$/,
      }]">
        <a-input v-model:value="createBackupModalState.name" />
      </a-form-item>

      <a-form-item id="create-backup-form-actions">
        <a-space>
          <a-button type="primary" html-type="submit">创建</a-button>
          <a-button @click="onCancel">取消</a-button>
        </a-space>
      </a-form-item>

    </a-form>

  </a-modal>
</template>

<style scoped>
#create-backup-form {
  margin-top: 2em;
}

#create-backup-form-actions {
  margin-top: 1em;
  justify-content: center;
}
</style>
