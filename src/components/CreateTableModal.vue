<script setup lang="ts">
import { merge } from '3h-utils';
import {
  createTableModalCallback, createTableModalState, createTableModalVisible,
  createTableModalPending, createTableModalForm,
} from '@/common/table/createTableModal';

const onSubmit = () => {
  createTableModalCallback.value?.(merge(createTableModalState));
  createTableModalPending.value = true;
};

const onCancel = () => {
  createTableModalCallback.value?.(null);
  createTableModalVisible.value = false;
};
</script>

<template>
  <a-modal v-model:visible="createTableModalVisible" @ok="onSubmit" @cancel="onCancel" v-bind="{
    title: '创建表格',
    footer: null,
    width: 400,
    confirmLoading: createTableModalPending,
  }">

    <a-alert type="info" show-icon>
      <template #message>表名格式</template>
      <template #description>
        表名应为两位阿拉伯数字，用来表示年级（入学年份）。
      </template>
    </a-alert>

    <a-form ref="createTableModalForm" @finish="onSubmit" v-bind="{
      id: 'create-table-form',
      model: createTableModalState,
      labelCol: { span: 5, offset: 3 },
      wrapperCol: { span: 10 },
    }">

      <a-form-item name="name" label="表名" :rules="[{
        required: true,
        pattern: /^\d{2}$/,
      }]">
        <a-input v-model:value="createTableModalState.name" />
      </a-form-item>

      <a-form-item id="create-table-form-actions">
        <a-space>
          <a-button type="primary" html-type="submit">创建</a-button>
          <a-button @click="onCancel">取消</a-button>
        </a-space>
      </a-form-item>

    </a-form>

  </a-modal>
</template>

<style scoped>
#create-table-form {
  margin-top: 2em;
}

#create-table-form-actions {
  margin-top: 1em;
  justify-content: center;
}
</style>
