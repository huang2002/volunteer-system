<script setup lang="ts">
import { merge } from '3h-utils';
import { importConfirmModalCallback, importConfirmModalState, importConfirmModalVisible, importConfirmModalPending, importConfirmModalForm, constructedImport } from '@/shared/import/importConfirmModal';
import { tableNames } from '@/shared/table/tableNames';
import { QuestionCircleOutlined } from '@ant-design/icons-vue';
import { computed } from 'vue';

defineProps<{
  fileCount: number;
  recordCount: number;
}>();

const onSubmit = () => {
  importConfirmModalCallback.value?.(merge(constructedImport.value));
  importConfirmModalPending.value = true;
};

const onCancel = () => {
  importConfirmModalCallback.value?.(null);
  importConfirmModalVisible.value = false;
};

const targetTableNames = computed(() => (
  Object.keys(constructedImport.value as {})
));

const newTableNames = computed(() => {
  const existingTableNames = tableNames.value;
  return targetTableNames.value.filter((name) => (
    !existingTableNames.includes(name)
  ));
});

const rejectedByNewTableCreation = computed(() => (
  !importConfirmModalState.allowTableCreation
  && (newTableNames.value.length > 0)
));

const rejected = computed(() => (
  rejectedByNewTableCreation.value
));
</script>

<template>
  <a-modal v-model:visible="importConfirmModalVisible" @ok="onSubmit()" @cancel="onCancel()" v-bind="{
    title: '导入记录',
    footer: null,
    closable: false,
    maskClosable: false,
  }">

    <a-alert type="info" show-icon>
      <template #message>
        导入信息
      </template>
      <template #description>
        <ul style="margin-bottom: 0;">
          <li>来自 {{ fileCount }} 个文件的 {{ recordCount }} 条数据。</li>
          <li>对应的表格：{{ targetTableNames.join('、') }}。</li>
          <li>年级由程序根据班级和学号猜测得出。</li>
          <li>重复数据只会保留第一条。</li>
          <li>首尾空格会被自动删除。</li>
        </ul>
      </template>
    </a-alert>

    <a-alert v-if="rejectedByNewTableCreation" v-bind="{
      class: 'rejection-alert',
      type: 'error',
      showIcon: true,
      message: `此次导入需要新建这些表格：${newTableNames.join('、')}。`,
    }" />

    <a-form ref="importConfirmModalForm" @finish="onSubmit()" v-bind="{
      id: 'import-confirm-form',
      model: importConfirmModalState,
      labelCol: { span: 0 },
      wrapperCol: { span: 24 },
    }">

      <a-form-item name="allowTableCreation">
        <div class="flex-centered">
          <a-checkbox v-model:checked="importConfirmModalState.allowTableCreation">
            允许创建新的表格
            <a-tooltip color="blue">
              <template #title>
                当记录对应的年级表格不存在时，允许自动创建。
              </template>
              <QuestionCircleOutlined style="color: #19F;" />
            </a-tooltip>
          </a-checkbox>
        </div>
      </a-form-item>

      <div class="flex-centered">
        <a-space>
          <a-button v-bind="{
            type: 'primary',
            htmlType: 'submit',
            loading: importConfirmModalPending,
            disabled: rejected,
          }">
            确认
          </a-button>
          <a-button @click="onCancel()" :disabled="importConfirmModalPending">取消</a-button>
        </a-space>
      </div>

    </a-form>

  </a-modal>
</template>

<style scoped>
#import-confirm-form {
  margin-top: 2em;
}

.rejection-alert {
  margin-top: 1em;
}
</style>
