<script setup lang="ts">
import { merge } from '3h-utils';
import { tableNameModalCallback, tableNameModalState, tableNameModalVisible, tableNameModalPending, tableNameModalForm, tableNameModalTitle } from '@/shared/table/tableNameModal';

const onSubmit = () => {
  tableNameModalCallback.value?.(merge(tableNameModalState));
  tableNameModalPending.value = true;
};

const onCancel = () => {
  tableNameModalCallback.value?.(null);
  tableNameModalVisible.value = false;
};
</script>

<template>
  <a-modal v-model:visible="tableNameModalVisible" @ok="onSubmit()" @cancel="onCancel()" v-bind="{
    title: tableNameModalTitle,
    width: 400,
    footer: null,
  }">

    <a-alert type="info" show-icon>
      <template #message>表名格式</template>
      <template #description>
        表名应为“某某学院XX级”，其中XX为表示年级（入学年份）的两位阿拉伯数字。
      </template>
    </a-alert>

    <a-form ref="tableNameModalForm" @finish="onSubmit()" v-bind="{
      id: 'table-name-form',
      model: tableNameModalState,
      labelCol: { span: 5, offset: 3 },
      wrapperCol: { span: 10 },
    }">

      <a-form-item name="name" label="表名" :rules="[{
        required: true,
        pattern: /^[^/?:;~!@$%]+\d{2}级$/,
        message: '表名与格式要求不匹配',
      }]">
        <a-input v-model:value="tableNameModalState.name" />
      </a-form-item>

      <div class="flex-centered">
        <a-space>
          <a-button v-bind="{
            type: 'primary',
            htmlType: 'submit',
            loading: tableNameModalPending,
          }">
            确认
          </a-button>
          <a-button @click="onCancel()">取消</a-button>
        </a-space>
      </div>

    </a-form>

  </a-modal>
</template>

<style scoped>
#table-name-form {
  margin-top: 2em;
}
</style>
