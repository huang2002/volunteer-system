<script setup lang="ts">
import { tableNames } from '@/common/tableNames';
import { DeleteOutlined, EditOutlined, PlusSquareOutlined } from '@ant-design/icons-vue';
import { message, type TableColumnType, type RadioGroupProps } from 'ant-design-vue';
import { computed, ref, watch } from 'vue';
import { tableActionDisabled, updateRecord, deleteRecord } from '../common/tableActions';
import RecordModel from '../components/RecordModel.vue';
import type { ActivityRecord } from '../common/recordModel';

const activeTableName = ref('');

const tableNameOptions = computed((): RadioGroupProps['options'] => (
  tableNames.value.map((name) => ({
    label: `表 ${name}`,
    value: name,
  }))
));

const columns: TableColumnType[] = [
  { title: '记录编号', dataIndex: 'record_id', fixed: 'left' },
  { title: '姓名', dataIndex: 'student_name', fixed: 'left' },
  { title: '学院', dataIndex: 'student_school' },
  { title: '班级', dataIndex: 'student_class' },
  { title: '学号', dataIndex: 'student_id' },
  { title: '志愿时长', dataIndex: 'activity_length' },
  { title: '服务日期', dataIndex: 'activity_date' },
  { title: '项目名称', dataIndex: 'activity_name' },
  { title: '项目类型', dataIndex: 'activity_type' },
  { title: '举办单位', dataIndex: 'activity_host' },
  { title: '项目负责人姓名', dataIndex: 'manager_name' },
  { title: '项目负责人QQ', dataIndex: 'manager_qq' },
  { title: '备注', dataIndex: 'notes' },
  { title: '操作', key: 'actions', fixed: 'right' },
];

const dataSource = ref<ActivityRecord[]>([]);
const updateDataSource = async () => {
  const tableName = activeTableName.value;
  const response = await fetch(`/api/view/table/${tableName}`);
  if (response.status === 200) {
    try {
      const result = await response.json();
      dataSource.value = result;
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
};

watch(activeTableName, updateDataSource);

const createTable = () => {

};
</script>

<template>
  <div id="table-view" class="view">

    <section id="toolbar">
      <a-radio-group v-model:value="activeTableName" v-bind="{
        id: 'toolbar-radio-group',
        optionType: 'button',
        buttonStyle: 'solid',
        options: tableNameOptions,
      }" />
      <a-button class="toolbar-button" @click="createTable">
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
      rowKey: 'record_id',
      scroll: { x: 'max-content' },
      bordered: true,
      pagination: false,
    }">

      <template #bodyCell="{ column, text, record }">

        <template v-if="(column as TableColumnType).dataIndex === 'activity_length'">
          {{ text }}
          小时
        </template>

        <template v-else-if="(column as TableColumnType).key === 'actions'">

          <a-button type="link" size="small" :disabled="tableActionDisabled" @click="updateRecord(
            activeTableName,
            (record as ActivityRecord),
            updateDataSource,
          )">
            <template #icon>
              <EditOutlined />
            </template>
            修改
          </a-button>

          <a-button type="link" size="small" danger :disabled="tableActionDisabled" @click="deleteRecord(
            activeTableName,
            (record as ActivityRecord).record_id,
            updateDataSource,
          )">
            <template #icon>
              <DeleteOutlined />
            </template>
            删除
          </a-button>

        </template>

      </template>

    </a-table>

    <RecordModel />

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
  margin-left: 0.5em;
}
</style>
