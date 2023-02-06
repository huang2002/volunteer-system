<script setup lang="ts">
import {
  recordModalCallback, recordModalState, recordModalVisible,
  recordModalPending, recordModalTitle, recordModalForm,
  recordModalBatchMode, recordModalBatchModeAvailable,
} from '@/common/recordModal';
import { InfoCircleOutlined } from '@ant-design/icons-vue';
import type { Rule } from 'ant-design-vue/lib/form';

const formCommonLayout = {
  labelCol: { span: 6, offset: 2 },
  wrapperCol: { span: 11 },
};

const formTailLayout = {
  wrapperCol: {
    offset: (
      formCommonLayout.labelCol.span
      + formCommonLayout.labelCol.offset
    ),
  },
};

const rules: Record<string, Rule[]> = {
  student_name: [{ type: 'string', required: true }],
  student_school: [{ type: 'string', required: true }],
  student_class: [{ type: 'string', required: true }],
  student_id: [{ type: 'string', required: true }],
  activity_length: [{ type: 'number', required: true }],
  activity_date: [{ type: 'string', required: true, pattern: /^\d{4}\/\d{2}\/\d{2}$/ }],
  activity_name: [{ type: 'string', required: true }],
  activity_type: [{ type: 'string', required: true }],
  activity_host: [{ type: 'string', required: true }],
  manager_name: [{ type: 'string', required: true }],
  manager_qq: [{ type: 'string', required: true }],
  notes: [{ type: 'string' }],
};

const onSubmit = () => {
  recordModalCallback.value?.(recordModalState);
  recordModalPending.value = true;
};

const onCancel = () => {
  recordModalCallback.value?.(null);
  recordModalVisible.value = false;
};
</script>

<template>
  <a-modal v-model:visible="recordModalVisible" @ok="onSubmit" @cancel="onCancel" v-bind="{
    style: { top: '2em' },
    title: recordModalTitle,
    footer: null,
    width: 650,
    confirmLoading: recordModalPending,
  }">

    <a-form ref="recordModalForm" @finish="onSubmit" v-bind="{
      id: 'record-form',
      model: recordModalState,
      rules,
      ...formCommonLayout,
    }">

      <a-form-item name="student_name" label="姓名">
        <a-input v-model:value="recordModalState.student_name" v-bind="{
          name: 'student_name',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item name="student_school" label="学院名称（全称）">
        <a-input v-model:value="recordModalState.student_school" v-bind="{
          name: 'student_school',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item name="student_class" label="班级">
        <a-input v-model:value="recordModalState.student_class" v-bind="{
          name: 'student_class',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item name="student_id" label="学号">
        <a-input v-model:value="recordModalState.student_id" v-bind="{
          name: 'student_id',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item name="activity_length" label="志愿时长">
        <a-input-number v-model:value="recordModalState.activity_length" v-bind="{
          name: 'activity_length',
          addonAfter: '小时',
          min: 0,
          precision: 2,
          step: 1,
          style: { width: '100%' },
        }" />
      </a-form-item>

      <a-form-item name="activity_date" label="服务日期">
        <a-date-picker v-model:value="recordModalState.activity_date" v-bind="{
          name: 'activity_date',
          allowClear: false,
          mode: 'date',
          valueFormat: 'YYYY/MM/DD',
          format: [ // for parsing
            'YYYY/MM/DD',
            'YYYY-MM-DD',
            'YYYY.MM.DD',
            'YYYYMMDD',
          ],
          style: { width: '100%' },
        }" />
      </a-form-item>

      <a-form-item name="activity_name" label="项目名称（全称）">
        <a-input v-model:value="recordModalState.activity_name" v-bind="{
          name: 'activity_name',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item name="activity_type" label="项目类型">
        <a-input v-model:value="recordModalState.activity_type" v-bind="{
          name: 'activity_type',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item name="activity_host" label="举办单位">
        <a-input v-model:value="recordModalState.activity_host" v-bind="{
          name: 'activity_host',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item name="manager_name" label="项目负责人姓名">
        <a-input v-model:value="recordModalState.manager_name" v-bind="{
          name: 'manager_name',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item name="manager_qq" label="项目负责人QQ">
        <a-input v-model:value="recordModalState.manager_qq" v-bind="{
          name: 'manager_qq',
          allowClear: true,
        }" />
      </a-form-item>

      <a-form-item id="record-form-item-notes" name="notes" label="备注">
        <a-textarea v-model:value="recordModalState.notes" v-bind="{
          name: 'notes',
          allowClear: true,
          showCount: true,
          maxlength: 200,
          autoSize: {
            maxRows: 6,
          },
        }" />
      </a-form-item>

      <a-form-item v-if="recordModalBatchModeAvailable" v-bind="formTailLayout">
        <a-tooltip color="blue">
          <template #title>
            提交成功后不自动关闭弹窗，而是仅清除部分信息，方便导入同一项目的更多记录。
          </template>
          <a-checkbox v-model:checked="recordModalBatchMode">
            批量导入模式
            <InfoCircleOutlined />
          </a-checkbox>
        </a-tooltip>
      </a-form-item>

      <a-form-item v-bind="formTailLayout">
        <a-space>
          <a-button type="primary" html-type="submit">确认</a-button>
          <a-button @click="onCancel">取消</a-button>
          <a-button danger @click="recordModalForm?.resetFields()">重置</a-button>
        </a-space>
      </a-form-item>

    </a-form>

  </a-modal>
</template>

<style scoped>
.ant-form-item {
  margin-bottom: 0.8em;
}

#record-form-item-notes {
  margin-bottom: 2em;
}
</style>
