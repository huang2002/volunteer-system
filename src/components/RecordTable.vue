<script setup lang="ts">
import { CopyOutlined, DeleteOutlined, EditOutlined, QuestionCircleOutlined } from '@ant-design/icons-vue';
import RecordAction from '@/components/RecordAction.vue';
import { merge } from '3h-utils';
import { KEY_GET_CONTENT_CONTAINER } from '@/shared/common';
import { inject } from 'vue';
import type { TableColumnType } from 'ant-design-vue';
import { recordModalStudentDefaults, type ActivityRecord } from '@/shared/record/recordModal';
import { updateRecord, appendRecord, deleteRecord } from '@/shared/record/recordActions';
import RecordIndex from './RecordIndex.vue';

const props = defineProps<{
  dataSource: ActivityRecord[];
  tableName?: string;
  loading: boolean;
  showActions?: boolean;
  dataSourceUpdater: () => void;
}>();

const getContentContainer = inject(KEY_GET_CONTENT_CONTAINER);

const columns: TableColumnType[] = [
  { title: '记录编号', dataIndex: 'record_id', ellipsis: true, fixed: 'left' },
  { title: '姓名', dataIndex: 'student_name', ellipsis: true, fixed: 'left' },
  { title: '学院', dataIndex: 'student_school', ellipsis: true },
  { title: '班级', dataIndex: 'student_class', ellipsis: true },
  { title: '学号', dataIndex: 'student_id', ellipsis: true },
  { title: '联系方式', dataIndex: 'student_contact', ellipsis: true },
  { title: '志愿时长', dataIndex: 'activity_length', ellipsis: true },
  { title: '服务日期', dataIndex: 'activity_date', ellipsis: true },
  { title: '项目名称', dataIndex: 'activity_name', ellipsis: true },
  { title: '项目类型', dataIndex: 'activity_type', ellipsis: true },
  { title: '举办单位', dataIndex: 'activity_host', ellipsis: true },
  { title: '项目负责人姓名', dataIndex: 'manager_name', ellipsis: true },
  { title: '项目负责人联系方式', dataIndex: 'manager_contact', ellipsis: true },
  { title: '项目负责人QQ', dataIndex: 'manager_qq', ellipsis: true },
  { title: '备注', dataIndex: 'notes', ellipsis: true },
];
if (props.showActions) {
  columns.push({ title: '操作', key: 'actions', fixed: 'right' });
}

</script>

<template>
  <a-table v-bind="{
    columns,
    dataSource,
    loading,
    rowKey: 'record_id',
    scroll: { x: 'max-content' },
    sticky: { getContainer: getContentContainer },
    bordered: true,
    pagination: false,
  }">

    <template #headerCell="{ column, title }">
      <template v-if="(column as TableColumnType).dataIndex === 'record_id'">
        {{ title }}
        <sup title="">
          <a-tooltip color="blue">
            <template #title>
              编号由后台程序根据记录的创建时间自动生成。
            </template>
            <QuestionCircleOutlined style="color: #19F;" />
          </a-tooltip>
        </sup>
      </template>
    </template>

    <template #bodyCell="{ column, text, record }">

      <template v-if="column.dataIndex && !record[column.dataIndex]">
        <a-typography-text disabled>无</a-typography-text>
      </template>

      <template v-else-if="(column as TableColumnType).dataIndex === 'record_id'">
        <RecordIndex :value="(record as ActivityRecord).record_id" />
      </template>

      <template v-else-if="(column as TableColumnType).dataIndex === 'activity_length'">
        {{ text }}
        小时
      </template>

      <a-space v-else-if="(column as TableColumnType).key === 'actions'">

        <RecordAction v-bind="{
          title: '修改',
          color: 'blue',
          onClick: () => {
            updateRecord(
              tableName!,
              (record as ActivityRecord),
              dataSourceUpdater,
            );
          },
        }">
          <template #icon>
            <EditOutlined />
          </template>
        </RecordAction>

        <RecordAction v-bind="{
          title: '添加此项目的其他记录',
          color: 'green',
          onClick: () => {
            appendRecord(
              tableName!,
              merge(record as ActivityRecord, recordModalStudentDefaults),
              dataSourceUpdater,
            );
          },
        }">
          <template #icon>
            <CopyOutlined />
          </template>
        </RecordAction>

        <RecordAction v-bind="{
          title: '删除',
          color: 'red',
          onClick: () => {
            deleteRecord(
              tableName!,
              (record as ActivityRecord).record_id,
              dataSourceUpdater,
            );
          },
        }">
          <template #icon>
            <DeleteOutlined />
          </template>
        </RecordAction>

      </a-space>

    </template>

  </a-table>
</template>

<style scoped>
.table-header-cell {
  font-weight: bold;
  white-space: nowrap;
}

:deep(th.ant-table-cell) {
  font-weight: bold;
}

:deep(.ant-table-cell) {
  min-width: 100px;
}
</style>
