<script setup lang="ts">
import { tableNames, updateTableNames, loadingTableNames } from '@/shared/table/tableNames';
import { DownOutlined, FileAddOutlined, FormOutlined, PlusSquareOutlined, ReloadOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { message, type RadioGroupProps } from 'ant-design-vue';
import { computed, ref, watch, onBeforeMount } from 'vue';
import { appendRecord, appendingRecord } from '@/shared/record/recordActions';
import { createTable, renameTable } from '@/shared/table/tableActions';
import RecordModal from '@/components/RecordModal.vue';
import { recordModalDefaults, type ActivityRecord } from '@/shared/record/recordModal';
import TableNameModal from '@/components/TableNameModal.vue';
import { tableNameModalVisible } from '@/shared/table/tableNameModal';
import ToolbarButton from '@/components/ToolbarButton.vue';
import { onRefreshSuccess } from '@/shared/common';
import RecordTable from '@/components/RecordTable.vue';

onBeforeMount(updateTableNames);

const activeTableName = ref('');

const tableNameOptions = computed((): RadioGroupProps['options'] => (
  tableNames.value.map((name) => ({
    label: `表 ${name}`,
    value: name,
  }))
));

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

const renameActiveTable = () => {
  renameTable(activeTableName.value);
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
          disabled: loadingTableNames || loadingDataSource,
        }" />

      </a-input-group>

      <ToolbarButton v-bind="{
        type: 'primary',
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
          <PlusSquareOutlined />
        </template>
        添加记录
      </ToolbarButton>

      <ToolbarButton v-bind="{
        loading: loadingDataSource,
        disabled: !activeTableName,
        onClick: () => {
          updateDataSource(onRefreshSuccess);
        },
      }">
        <template #icon>
          <ReloadOutlined />
        </template>
        刷新表格
      </ToolbarButton>

      <a-dropdown>
        <a-button type="link">
          更多操作
          <DownOutlined />
        </a-button>
        <template #overlay>
          <a-menu>

            <a-menu-item @click="renameActiveTable" v-bind="{
              disabled: !activeTableName || tableNameModalVisible,
            }">
              <a-space>
                <FormOutlined style="color: #F90;" />
                重命名表
              </a-space>
            </a-menu-item>

            <a-menu-item @click="createAndViewTable" v-bind="{
              disabled: tableNameModalVisible,
            }">
              <a-space>
                <FileAddOutlined style="color: #192;" />
                新建表格
              </a-space>
            </a-menu-item>

          </a-menu>
        </template>
      </a-dropdown>

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

    <RecordTable v-else v-bind="{
      dataSource,
      tableName: activeTableName,
      loading: loadingDataSource,
      showActions: true,
      dataSourceUpdater: updateDataSource,
    }" />

    <TableNameModal />
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

.toolbar-button {
  margin-left: 8px;
}
</style>
