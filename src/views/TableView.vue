<script setup lang="ts">
import { tableNames, updateTableNames, loadingTableNames } from '@/shared/table/tableNames';
import { DeleteOutlined, DownOutlined, FormOutlined, PlusSquareOutlined, ReloadOutlined, SyncOutlined, ToolOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { computed, ref, watch, onBeforeMount, shallowRef, provide } from 'vue';
import { appendRecord, appendingRecord } from '@/shared/record/recordActions';
import { deleteTable, renameTable } from '@/shared/table/tableActions';
import RecordModal from '@/components/RecordModal.vue';
import { recordModalDefaults, type ActivityRecord } from '@/shared/record/recordModal';
import TableNameModal from '@/components/TableNameModal.vue';
import ToolbarButton from '@/components/ToolbarButton.vue';
import { displayErrorMessage, KEY_TABLE_MANAGEMENT_MODAL_VISIBLE } from '@/shared/common';
import RecordTable from '@/components/RecordTable.vue';
import type { SelectProps } from 'ant-design-vue/lib/vc-select';
import TableManagementModal from '@/components/TableManagementModal.vue';

onBeforeMount(() => {
  updateTableNames(false);
});

const activeTableName = ref<string | undefined>(undefined);

const tableManagementModalVisible = ref(false);
provide(KEY_TABLE_MANAGEMENT_MODAL_VISIBLE, tableManagementModalVisible);

const tableNotFound = computed(() => (
  !(tableNames.value as (string | undefined)[])
    .includes(activeTableName.value)
));

const tableNameOptions = computed((): SelectProps['options'] => (
  tableNames.value.map((name) => ({
    label: name,
    value: name,
    title: name,
  }))
));

const dataSource = shallowRef<ActivityRecord[]>([]);
const loadingDataSource = ref(false);
const updateDataSource = async (
  alertSuccess: boolean,
) => {
  const tableName = activeTableName.value;
  if (!tableName) {
    return;
  }
  loadingDataSource.value = true;
  const response = await fetch(`/api/table/view/${tableName}`);
  if (response.status === 200) {
    try {
      const result = await response.json();
      if (activeTableName.value !== tableName) {
        // loading other table
        return;
      }
      dataSource.value = result;
      if (alertSuccess) {
        message.success('刷新成功');
      }
    } catch {
      message.error('更新数据时出错');
    }
  } else {
    await displayErrorMessage(response, '获取数据时出错');
  }
  loadingDataSource.value = false;
};

watch(activeTableName, () => {
  updateDataSource(false);
});
</script>

<template>
  <div id="table-view" class="view">

    <div id="toolbar">

      <a-input-group id="toolbar-table-list" compact>

        <a-tooltip v-bind="{
          color: 'blue',
          title: '刷新表格列表',
        }">
          <a-button @click="updateTableNames(true)" v-bind="{
            loading: loadingTableNames,
          }">
            <template #icon>
              <SyncOutlined />
            </template>
          </a-button>
        </a-tooltip>

        <a-select v-if="tableNames.length" v-model:value="activeTableName" v-bind="{
          options: tableNameOptions,
          loading: loadingTableNames,
          disabled: loadingDataSource,
          placeholder: '请选择表格',
          style: {
            width: '10em',
          },
        }" />
        <a-button v-else disabled>
          暂无表格
        </a-button>

      </a-input-group>

      <ToolbarButton v-bind="{
        type: 'primary',
        loading: appendingRecord,
        disabled: !activeTableName || tableNotFound,
        onClick: () => {
          appendRecord(
            activeTableName!,
            recordModalDefaults,
            () => {
              updateDataSource(false);
            },
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
        disabled: !activeTableName || tableNotFound,
        onClick: () => {
          updateDataSource(true);
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

            <a-menu-item @click="tableManagementModalVisible = true" v-bind="{
              disabled: tableManagementModalVisible,
            }">
              <a-space>
                <ToolOutlined style="color: #19F;" />
                管理表格
              </a-space>
            </a-menu-item>

            <a-menu-item @click="renameTable(activeTableName!, true)" v-bind="{
              disabled: !activeTableName || tableNotFound,
            }">
              <a-space>
                <FormOutlined style="color: #F90;" />
                重命名表
              </a-space>
            </a-menu-item>

            <a-menu-item @click="deleteTable([activeTableName!], true)" v-bind="{
              disabled: !activeTableName || tableNotFound,
            }">
              <a-space>
                <DeleteOutlined style="color: #F31;" />
                删除表格
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

    <a-alert v-else-if="tableNotFound" v-bind="{
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

    <TableManagementModal />
    <RecordModal :suggestion-source="dataSource" />
    <TableNameModal />

  </div>
</template>

<style scoped>
#toolbar {
  display: flex;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow-x: auto;
}

#toolbar-table-list {
  margin-right: auto;
}

.toolbar-button {
  margin-left: 8px;
}
</style>
