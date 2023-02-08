<script setup lang="ts">
import { merge } from '3h-utils';
import { backupNameModalCallback, backupNameModalState, backupNameModalVisible, backupNameModalPending, backupNameModalForm, backupNameModalTitle } from '@/shared/backup/backupNameModal';

const onSubmit = () => {
  backupNameModalCallback.value?.(merge(backupNameModalState));
  backupNameModalPending.value = true;
};

const onCancel = () => {
  backupNameModalCallback.value?.(null);
  backupNameModalVisible.value = false;
};
</script>

<template>
  <a-modal v-model:visible="backupNameModalVisible" @ok="onSubmit()" @cancel="onCancel()" v-bind="{
    title: backupNameModalTitle,
    footer: null,
    confirmLoading: backupNameModalPending,
  }">

    <a-alert type="info" show-icon>
      <template #message>备份名称格式</template>
      <template #description>
        建议使用“时间+名称”的格式，方便日后管理。
      </template>
    </a-alert>

    <a-form ref="backupNameModalForm" @finish="onSubmit()" v-bind="{
      id: 'backup-name-form',
      model: backupNameModalState,
      labelCol: { span: 5, offset: 3 },
      wrapperCol: { span: 12 },
    }">

      <a-form-item name="name" label="备份名称" :rules="[{
        required: true,
        pattern: /^[^/?:;~!@$%]+$/,
        message: '备份名称为必填项，且不能含有以下字符：/?:;~!@$%',
      }]">
        <a-input v-model:value="backupNameModalState.name" />
      </a-form-item>

      <div id="backup-name-form-actions">
        <a-space>
          <a-button type="primary" html-type="submit">确认</a-button>
          <a-button @click="onCancel()">取消</a-button>
        </a-space>
      </div>

    </a-form>

  </a-modal>
</template>

<style scoped>
#backup-name-form {
  margin-top: 2em;
}

#backup-name-form-actions {
  display: flex;
  margin-top: 1em;
  justify-content: center;
}
</style>
