<script setup lang="ts">
import { DATE_PATTERN, type RecordModalState } from '@/shared/common';
import { recordModalCallback, recordModalState, recordModalVisible, recordModalPending, recordModalMode, recordModalForm, recordModalBatchMode, type RecordModalMode } from '@/shared/record/recordModal';
import { CopyOutlined, FilterOutlined, InfoCircleOutlined, ScissorOutlined } from '@ant-design/icons-vue';
import type { Rule } from 'ant-design-vue/lib/form';
import { computed, watch } from 'vue';
import { merge, unique } from '3h-utils';

const props = defineProps<{
  suggestionSource: RecordModalState[];
}>();

const formCommonLayout = {
  labelCol: { span: 6, offset: 3 },
  wrapperCol: { span: 9 },
};

const formTailLayout = {
  labelCol: { span: 0 },
  wrapperCol: { span: 24 },
};

const rules: Record<keyof RecordModalState, Rule[]> = {
  student_name: [{ type: 'string', required: true }],
  student_school: [{ type: 'string', required: true }],
  student_class: [{ type: 'string', required: true }],
  student_id: [{ type: 'string', required: true }],
  student_contact: [{ type: 'string' }],
  activity_length: [{ type: 'number', required: true }],
  activity_begin: [{ type: 'string', required: true, pattern: DATE_PATTERN }],
  activity_end: [{ type: 'string', required: true, pattern: DATE_PATTERN }],
  activity_name: [{ type: 'string', required: true }],
  activity_type: [{ type: 'string' }],
  activity_host: [{ type: 'string' }],
  manager_name: [{ type: 'string' }],
  manager_contact: [{ type: 'string' }],
  manager_qq: [{ type: 'string' }],
  notes: [{ type: 'string' }],
};

const titles: Record<RecordModalMode, string> = {
  append: '添加记录',
  update: '修改记录',
};

watch(recordModalState, () => {
  if (
    recordModalState.activity_begin
    && !recordModalState.activity_end
  ) {
    recordModalState.activity_end = recordModalState.activity_begin;
  }
  if (
    recordModalState.activity_end
    && !recordModalState.activity_begin
  ) {
    recordModalState.activity_begin = recordModalState.activity_end;
  }
});

const generateSuggestions = (
  filterKey: (keyof RecordModalState)[],
  valueKey: keyof RecordModalState,
) => (
  computed(() => {

    let source = props.suggestionSource;

    filterKey.forEach((key) => {
      const expected = recordModalState[key];
      if (!expected) {
        return;
      }
      source = source.filter((record) => (
        record[key] === expected
      ));
    });

    return unique(
      source.map(
        (record) => record[valueKey]
      )
    ).map((value) => ({
      text: String(value),
      value,
    }));

  })
);

const studentSchoolSuggestions = generateSuggestions(
  [],
  'student_school'
);
const studentClassSuggestions = generateSuggestions(
  ['student_school'],
  'student_class',
);
const studentNameSuggestions = generateSuggestions(
  ['student_school', 'student_class', 'student_id'],
  'student_name',
);
const studentIdSuggestions = generateSuggestions(
  ['student_school', 'student_class', 'student_name'],
  'student_id',
);
const studentContactSuggestions = generateSuggestions(
  ['student_school', 'student_class', 'student_name'],
  'student_contact',
);
const activityNameSuggestions = generateSuggestions(
  ['activity_host', 'activity_type'],
  'activity_name',
);
const activityTypeSuggestions = generateSuggestions(
  ['activity_name', 'activity_host'],
  'activity_type',
);
const activityHostSuggestions = generateSuggestions(
  ['activity_name', 'activity_type'],
  'activity_host',
);
const managerNameSuggestions = generateSuggestions(
  ['manager_qq', 'manager_contact'],
  'manager_name',
);
const managerContactSuggestions = generateSuggestions(
  ['manager_name', 'manager_qq'],
  'manager_contact',
);
const managerQQSuggestions = generateSuggestions(
  ['manager_name', 'manager_contact'],
  'manager_qq',
);
const notesSuggestions = generateSuggestions(
  [],
  'notes',
);

const onSubmit = () => {
  recordModalPending.value = true;
  recordModalCallback.value?.(merge(recordModalState));
};

const onCancel = () => {
  recordModalCallback.value?.(null);
  recordModalVisible.value = false;
};
</script>

<template>
  <a-modal v-model:visible="recordModalVisible" @ok="onSubmit()" @cancel="onCancel()" v-bind="{
    style: { top: '2em' },
    title: titles[recordModalMode],
    width: 700,
    footer: null,
  }">
    <a-space v-bind="{
      direction: 'vertical',
      size: 'large',
      style: {
        width: '100%',
      },
    }">

      <a-alert type="info" show-icon v-if="recordModalMode === 'append'">
        <template #message>
          系统提醒
        </template>
        <template #description>
          <a-space>
            <FilterOutlined />
            后台程序添加记录时会自动检查，遇到除编号外完全相同的记录将只保留第一条。
          </a-space>
          <br />
          <a-space>
            <CopyOutlined />
            如需添加雷同记录，请填写不同的备注加以区分，例如：1、2、……。
          </a-space>
          <br />
          <a-space>
            <ScissorOutlined />
            首尾空格会被自动删除。
          </a-space>
        </template>
      </a-alert>

      <a-form ref="recordModalForm" @finish="onSubmit()" v-bind="{
        id: 'record-form',
        model: recordModalState,
        rules,
        ...formCommonLayout,
      }">

        <a-form-item name="student_school" label="学院名称（全称）">
          <a-auto-complete v-model:value="recordModalState.student_school" v-bind="{
            dataSource: studentSchoolSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="student_school" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="student_class" label="班级">
          <a-auto-complete v-model:value="recordModalState.student_class" v-bind="{
            dataSource: studentClassSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="student_class" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="student_name" label="姓名">
          <a-auto-complete v-model:value="recordModalState.student_name" v-bind="{
            dataSource: studentNameSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="student_name" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="student_id" label="学号">
          <a-auto-complete v-model:value="recordModalState.student_id" v-bind="{
            dataSource: studentIdSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="student_id" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="student_contact" label="联系方式">
          <a-auto-complete v-model:value="recordModalState.student_contact" v-bind="{
            dataSource: studentContactSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="student_contact" allow-clear />
          </a-auto-complete>
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

        <a-form-item name="activity_begin" label="开始日期">
          <a-date-picker v-model:value="recordModalState.activity_begin" v-bind="{
            name: 'activity_begin',
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

        <a-form-item name="activity_end" label="结束日期">
          <a-date-picker v-model:value="recordModalState.activity_end" v-bind="{
            name: 'activity_end',
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
          <a-auto-complete v-model:value="recordModalState.activity_name" v-bind="{
            dataSource: activityNameSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="activity_name" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="activity_type" label="项目类型">
          <a-auto-complete v-model:value="recordModalState.activity_type" v-bind="{
            dataSource: activityTypeSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="activity_type" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="activity_host" label="举办单位">
          <a-auto-complete v-model:value="recordModalState.activity_host" v-bind="{
            dataSource: activityHostSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="activity_host" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="manager_name" label="项目负责人姓名">
          <a-auto-complete v-model:value="recordModalState.manager_name" v-bind="{
            dataSource: managerNameSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="manager_name" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="manager_contact" label="项目负责人联系方式">
          <a-auto-complete v-model:value="recordModalState.manager_contact" v-bind="{
            dataSource: managerContactSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="manager_name" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item name="manager_qq" label="项目负责人QQ">
          <a-auto-complete v-model:value="recordModalState.manager_qq" v-bind="{
            dataSource: managerQQSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-input name="manager_qq" allow-clear />
          </a-auto-complete>
        </a-form-item>

        <a-form-item id="record-form-item-notes" name="notes" label="备注">
          <a-auto-complete v-model:value="recordModalState.notes" v-bind="{
            dataSource: notesSuggestions,
            backfill: true,
            filterOption: true,
          }">
            <a-textarea v-bind="{
              name: 'notes',
              allowClear: true,
              showCount: true,
              maxlength: 200,
              autoSize: {
                maxRows: 6,
              },
            }" />
          </a-auto-complete>
        </a-form-item>

        <a-form-item v-if="recordModalMode === 'append'" v-bind="formTailLayout">
          <div class="flex-centered">
            <a-tooltip color="blue">
              <template #title>
                提交成功后不自动关闭弹窗，而是仅清除部分信息，方便继续导入同一项目的更多记录。
              </template>
              <a-checkbox v-model:checked="recordModalBatchMode">
                批量导入模式
                <InfoCircleOutlined style="color: #19F;" />
              </a-checkbox>
            </a-tooltip>
          </div>
        </a-form-item>

        <div class="flex-centered">
          <a-space>
            <a-button v-bind="{
              type: 'primary',
              htmlType: 'submit',
              loading: recordModalPending,
            }">
              确认
            </a-button>
            <a-button @click="onCancel()">取消</a-button>
            <a-button danger @click="recordModalForm?.resetFields()">重置</a-button>
          </a-space>
        </div>

      </a-form>

    </a-space>
  </a-modal>
</template>

<style scoped>
.ant-form-item {
  margin-bottom: 0.8em;
}

#record-form-item-notes {
  margin-bottom: 1.8em;
}
</style>
