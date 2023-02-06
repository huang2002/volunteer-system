<script setup lang="ts">
import { tableNames, updateTableNames, loadingTableNames } from '@/common/tableNames';
import { DeleteOutlined, EditOutlined, FormOutlined, PlusSquareOutlined, ReloadOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { message, type TableColumnType, type RadioGroupProps } from 'ant-design-vue';
import { computed, ref, watch } from 'vue';
import { recordActionDisabled, updateRecord, deleteRecord, appendRecord } from '@/common/recordActions';
import { createTable } from '@/common/tableActions';
import RecordModal from '@/components/RecordModal.vue';
import { type ActivityRecord, recordModalVisibility } from '@/common/recordModal';
import CreateTableModal from '@/components/CreateTableModal.vue';
import { createTableModalVisibility } from '@/common/createTableModal';

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

    <section id="toolbar">

      <a-button @click="updateTableNames(onRefreshSuccess)" v-bind="{
        type: 'link',
        class: 'toolbar-button',
        loading: loadingTableNames,
      }">
        <template #icon>
          <SyncOutlined />
        </template>
        刷新表名
      </a-button>

      <a-radio-group v-model:value="activeTableName" v-bind="{
        id: 'toolbar-radio-group',
        optionType: 'button',
        buttonStyle: 'solid',
        options: tableNameOptions,
      }" />

      <a-button @click="appendRecord(activeTableName, updateDataSource)" v-bind="{
        class: 'toolbar-button',
        loading: recordModalVisibility,
        disabled: !activeTableName,
      }">
        <template #icon>
          <FormOutlined />
        </template>
        添加记录
      </a-button>

      <a-button @click="updateDataSource(onRefreshSuccess)" v-bind="{
        class: 'toolbar-button',
        loading: loadingDataSource,
        disabled: !activeTableName,
      }">
        <template #icon>
          <ReloadOutlined />
        </template>
        刷新表格
      </a-button>

      <a-button @click="createAndViewTable" v-bind="{
        class: 'toolbar-button',
        loading: createTableModalVisibility,
      }">
        <template #icon>
          <PlusSquareOutlined />
        </template>
        新建表格
      </a-button>

    </section>

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
      sticky: true,
      bordered: true,
      pagination: false,
    }">

      <template #bodyCell="{ column, text, record }">

        <template v-if="(column as TableColumnType).dataIndex === 'activity_length'">
          {{ text }}
          小时
        </template>

        <template v-if="(column as TableColumnType).dataIndex === 'notes'">
          <template v-if="!(record as ActivityRecord).notes">
            <a-typography-text disabled>无</a-typography-text>
          </template>
        </template>

        <a-space v-else-if="(column as TableColumnType).key === 'actions'">

          <a-button type="primary" ghost size="small" :disabled="recordActionDisabled" @click="updateRecord(
            activeTableName,
            (record as ActivityRecord),
            updateDataSource,
          )">
            <EditOutlined />
            修改
          </a-button>

          <a-button danger ghost size="small" :disabled="recordActionDisabled" @click="deleteRecord(
            activeTableName,
            (record as ActivityRecord).record_id,
            updateDataSource,
          )">
            <DeleteOutlined />
            删除
          </a-button>

        </a-space>

      </template>

    </a-table>

    <CreateTableModal />
    <RecordModal />

    <a-back-top />

  </div>
</template>

<style scoped>
#toolbar {
  display: flex;
  margin-bottom: 1em;
}

#toolbar-radio-group {
  flex: 1 0;
  overflow-x: auto;
}

.toolbar-button {
  margin: 0 0.3em;
}

.table-header-cell {
  font-weight: bold;
  white-space: nowrap;
}

:deep(th.ant-table-cell) {
  font-weight: bold;
}

:deep(.ant-table-cell) {
  min-width: 7em;
}
</style>
