<script setup lang="ts">
import { CopyOutlined, DeleteOutlined, EditOutlined, InfoCircleOutlined, WarningOutlined } from '@ant-design/icons-vue';
import RecordAction from '@/components/RecordAction.vue';
import { merge } from '3h-utils';
import { KEY_GET_CONTENT_CONTAINER } from '@/shared/common';
import { inject } from 'vue';
import type { TableColumnType } from 'ant-design-vue';
import { recordModalStudentDefaults, type ActivityRecord } from '@/shared/record/recordModal';
import { updateRecord, appendRecord, deleteRecord } from '@/shared/record/recordActions';
import RecordIndex from './RecordIndex.vue';

const props = defineProps<{
  records: ActivityRecord[];
  tableName?: string;
  loading: boolean;
  showActions?: boolean;
  importPreviewMode?: boolean;
  updater?: (alertSuccess: boolean) => void;
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
  { title: '开始日期', dataIndex: 'activity_begin', ellipsis: true },
  { title: '结束日期', dataIndex: 'activity_end', ellipsis: true },
  { title: '项目名称', dataIndex: 'activity_name', ellipsis: true },
  { title: '项目类型', dataIndex: 'activity_type', ellipsis: true },
  { title: '举办单位', dataIndex: 'activity_host', ellipsis: true },
  { title: '负责人姓名', dataIndex: 'manager_name', ellipsis: true },
  { title: '负责人联系方式', dataIndex: 'manager_contact', ellipsis: true },
  { title: '负责人QQ', dataIndex: 'manager_qq', ellipsis: true },
  { title: '备注', dataIndex: 'notes', ellipsis: true },
];
if (props.showActions) {
  columns.push({ title: '操作', key: 'actions', fixed: 'right' });
}

</script>

<template>
  <a-table v-bind="{
    columns,
    dataSource: records,
    loading,
    rowKey: 'record_id',
    size: 'small',
    scroll: { x: 'max-content' },
    sticky: { getContainer: getContentContainer },
    bordered: true,
    pagination: {
      defaultPageSize: 10,
      pageSizeOptions: ['10', '15', '20', '25', '30'],
      showLessItems: true,
      showQuickJumper: true,
      showSizeChanger: true,
      showTotal: (total: number, range: [number, number]) => (
        `第 ${range[0]} 条到第 ${range[1]} 条 （共 ${total} 条记录）`
      )
    },
  }">

    <template #headerCell="{ column, title }">
      <template v-if="(column as TableColumnType).dataIndex === 'record_id'">
        {{ title }}
        <span title="">
          <a-tooltip v-bind="{
            color: (importPreviewMode ? 'orange' : 'blue'),
            placement: 'right',
          }">
            <template #title>
              <template v-if="importPreviewMode">
                此处编号仅为预览，真实编号将在正式导入时生成。
              </template>
              <template v-else>
                编号由后台程序根据记录的创建时间自动生成。
              </template>
            </template>
            <WarningOutlined v-if="importPreviewMode" style="color: #F90;" />
            <InfoCircleOutlined v-else style="color: #19F;" />
          </a-tooltip>
        </span>
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
              () => {
                updater!(false);
              },
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
              () => {
                updater!(false);
              },
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
              () => {
                updater!(false);
              },
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
:deep(th.ant-table-cell) {
  font-weight: bold;
}

:deep(.ant-table-cell) {
  min-width: 100px;
}
</style>
