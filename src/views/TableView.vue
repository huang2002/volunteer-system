<script setup lang="ts">
import { tableNames, updateTableNames, loadingTableNames } from '@/common/tableNames';
import {
  CopyOutlined,
  DeleteOutlined, EditOutlined, FormOutlined,
  PlusSquareOutlined, ReloadOutlined, SyncOutlined,
} from '@ant-design/icons-vue';
import { message, type TableColumnType, type RadioGroupProps } from 'ant-design-vue';
import { computed, ref, watch, inject } from 'vue';
import { updateRecord, deleteRecord, appendRecord, appendingRecord } from '@/common/recordActions';
import { createTable } from '@/common/tableActions';
import RecordModal from '@/components/RecordModal.vue';
import { recordModalDefaults, recordModalStudentDefaults, type ActivityRecord } from '@/common/recordModal';
import CreateTableModal from '@/components/CreateTableModal.vue';
import { createTableModalVisible } from '@/common/createTableModal';
import RecordAction from '@/components/RecordAction.vue';
import { merge } from '3h-utils';
import TableToolbarButton from '@/components/TableToolbarButton.vue';
import { KEY_GET_CONTENT_CONTAINER } from '@/common/common';

const getContentContainer = inject(KEY_GET_CONTENT_CONTAINER);

const activeTableName = ref('');

const tableNameOptions = computed((): RadioGroupProps['options'] => (
  tableNames.value.map((name) => ({
    label: `表 ${name}`,
    value: name,
  }))
));

const columns: TableColumnType[] = [
  { title: '记录编号', dataIndex: 'record_id', ellipsis: true, fixed: 'left' },
  { title: '姓名', dataIndex: 'student_name', ellipsis: true, fixed: 'left' },
  { title: '学院', dataIndex: 'student_school', ellipsis: true },
  { title: '班级', dataIndex: 'student_class', ellipsis: true },
  { title: '学号', dataIndex: 'student_id', ellipsis: true },
  { title: '志愿时长', dataIndex: 'activity_length', ellipsis: true },
  { title: '服务日期', dataIndex: 'activity_date', ellipsis: true },
  { title: '项目名称', dataIndex: 'activity_name', ellipsis: true },
  { title: '项目类型', dataIndex: 'activity_type', ellipsis: true },
  { title: '举办单位', dataIndex: 'activity_host', ellipsis: true },
  { title: '项目负责人姓名', dataIndex: 'manager_name', ellipsis: true },
  { title: '项目负责人QQ', dataIndex: 'manager_qq', ellipsis: true },
  { title: '备注', dataIndex: 'notes', ellipsis: true },
  { title: '操作', key: 'actions', fixed: 'right' },
];

const dataSource = ref<ActivityRecord[]>([]);
const loadingDataSource = ref(false);
const updateDataSource = async (
  onSuccess?: () => void,
) => {
  const tableName = activeTableName.value;
  if (!tableName) {
    return;
  }
  loadingDataSource.value = true;
  const response = await fetch(`/api/view/table/${tableName}`);
  if (response.status === 200) {
    try {
      const result = await response.json();
      if (activeTableName.value !== tableName) {
        // loading other table
        return;
      }
      dataSource.value = result;
      onSuccess?.();
    } catch {
      message.error('更新数据时出错');
    }
  } else {
    try {
      const errorText = await response.text();
      message.error(errorText);
    } catch {
      message.error('获取数据时出错');
    }
  }
  loadingDataSource.value = false;
};

watch(activeTableName, () => {
  updateDataSource();
});

const createAndViewTable = () => {
  createTable((newTable) => {
    activeTableName.value = newTable.name;
  });
};

const onRefreshSuccess = () => {
  message.success('刷新成功');
};
</script>

<template>
  <div id="table-view" class="view">

    <div id="toolbar">

      <a-input-group id="toolbar-table-select" compact>
        <a-tooltip v-bind="{
          color: 'blue',
          title: '刷新表格列表',
        }">
          <a-button @click="updateTableNames(onRefreshSuccess)" v-bind="{
            loading: loadingTableNames,
          }">
            <template #icon>
              <SyncOutlined />
            </template>
          </a-button>
        </a-tooltip>
        <a-radio-group v-model:value="activeTableName" v-bind="{
          optionType: 'button',
          buttonStyle: 'solid',
          options: tableNameOptions,
        }" />
      </a-input-group>

      <TableToolbarButton v-bind="{
        loading: appendingRecord,
        disabled: !activeTableName,
        onClick: () => {
          appendRecord(
            activeTableName,
            recordModalDefaults,
            updateDataSource,
          );
        },
      }">
        <template #icon>
          <FormOutlined style="color: #F90;" />
        </template>
        添加记录
      </TableToolbarButton>

      <TableToolbarButton v-bind="{
        loading: loadingDataSource,
        disabled: !activeTableName,
        onClick: () => {
          updateDataSource(onRefreshSuccess);
        },
      }">
        <template #icon>
          <ReloadOutlined style="color: #19F;" />
        </template>
        刷新表格
      </TableToolbarButton>

      <TableToolbarButton v-bind="{
        loading: createTableModalVisible,
        onClick: createAndViewTable,
      }">
        <template #icon>
          <PlusSquareOutlined style="color: #1C3;" />
        </template>
        新建表格
      </TableToolbarButton>

    </div>

    <a-alert v-if="!activeTableName" v-bind="{
      type: 'info',
      showIcon: true,
      message: '请在上方选择想要查看/编辑的表格名称。',
    }" />

    <a-alert v-else-if="!tableNames.includes(activeTableName)" v-bind="{
      type: 'warning',
      showIcon: true,
      message: '指定的表不存在，请重新选择，或刷新重试。',
    }" />

    <a-table v-else v-bind="{
      columns,
      dataSource,
      loading: loadingDataSource,
      rowKey: 'record_id',
      scroll: { x: 'max-content' },
      sticky: { getContainer: getContentContainer },
      bordered: true,
      pagination: false,
    }">

      <template #bodyCell="{ column, text, record }">

        <template v-if="(column as TableColumnType).dataIndex === 'activity_length'">
          {{ text }}
          小时
        </template>

        <template v-else-if="(column as TableColumnType).dataIndex === 'notes'">
          <template v-if="!(record as ActivityRecord).notes">
            <a-typography-text disabled>无</a-typography-text>
          </template>
        </template>

        <a-space v-else-if="(column as TableColumnType).key === 'actions'">

          <RecordAction v-bind="{
            title: '修改',
            color: 'blue',
            onClick: () => {
              updateRecord(
                activeTableName,
                (record as ActivityRecord),
                updateDataSource,
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
                activeTableName,
                merge(record as ActivityRecord, recordModalStudentDefaults),
                updateDataSource,
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
                activeTableName,
                (record as ActivityRecord).record_id,
                updateDataSource,
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

    <CreateTableModal />
    <RecordModal :suggestion-source="dataSource" />

  </div>
</template>

<style scoped>
#toolbar {
  display: flex;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow-x: auto;
}

#toolbar-table-select {
  flex: 1 0;
}

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
