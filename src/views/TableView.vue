<script setup lang="ts">
import { tableNames } from '@/common/tableNames';
import { DeleteOutlined, EditOutlined, InfoCircleOutlined, PlusSquareOutlined, WarningOutlined } from '@ant-design/icons-vue';
import { message, type TableColumnType } from 'ant-design-vue';
import { ref, watch } from 'vue';
import { tableActionDisabled, updateRecord, deleteRecord } from '../common/tableActions';
import RecordModel from '../components/RecordModel.vue';

const activeTableName = ref('');

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

const dataSource = ref<any[]>([]);
const updateDataSource = async () => {
  const tableName = activeTableName.value;
  const response = await fetch(`/api/view/table/${tableName}`);
  if (response.status === 200) {
    try {
      const result = await response.json();
      dataSource.value = result;
    } catch {
      message.error('更新表名时出错');
    }
  } else {
    try {
      const errorText = await response.text();
      message.error(errorText);
    } catch {
      message.error('获取表名时出错');
    }
  }
};

watch(activeTableName, updateDataSource);

const createTable = () => {

};

const recordModelVisibility = ref(false);
const showRecordModel = () => {

};
</script>

<template>
  <div id="table-view" class="view">

    <a-space id="toolbar">
      <a-radio-group v-model:value="activeTableName" v-bind="{
        id: 'toolbar-radio',
        optionType: 'button',
        buttonStyle: 'solid',
        options: tableNames,
      }" />
      <a-button @click="createTable">
        <template #icon>
          <PlusSquareOutlined />
        </template>
        新建表格
      </a-button>
    </a-space>

    <a-space v-if="!activeTableName">
      <InfoCircleOutlined />
      请在上方选择想要查看/编辑的表格名称。
    </a-space>

    <a-space v-else-if="!tableNames.includes(activeTableName)">
      <WarningOutlined />
      指定的表不存在，请重新选择，或刷新重试。
    </a-space>

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

          <a-button type="link" :disabled="tableActionDisabled" @click="updateRecord(
            activeTableName,
            record.record_id,
            updateDataSource,
          )">
            <template #icon>
              <EditOutlined />
            </template>
            修改
          </a-button>

          <a-button type="link" danger :disabled="tableActionDisabled" @click="deleteRecord(
            activeTableName,
            record.record_id,
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

</style>
