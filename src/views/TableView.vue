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

const records = shallowRef<ActivityRecord[]>([]);
const loadingRecords = ref(false);
const loadRecords = async (
  alertSuccess: boolean,
) => {
  const tableName = activeTableName.value;
  if (!tableName) {
    return;
  }
  loadingRecords.value = true;
  try {
    const response = await fetch(`/api/table/view/${tableName}`);
    if (response.status === 200) {
      const result = await response.json();
      if (activeTableName.value !== tableName) {
        // loading other table
        return;
      }
      records.value = result;
      if (alertSuccess) {
        message.success('????????????');
      }
    } else {
      await displayErrorMessage(response, '?????????????????????');
    }
  } catch {
    message.error('??????????????????');
  }
  loadingRecords.value = false;
};

watch(activeTableName, () => {
  loadRecords(false);
});
</script>

<template>
  <div id="table-view" class="view">

    <div id="toolbar">

      <a-input-group id="toolbar-table-list" compact>

        <a-tooltip v-bind="{
          color: 'blue',
          title: '??????????????????',
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
          disabled: loadingRecords,
          placeholder: '???????????????',
          style: {
            width: '16em',
          },
        }" />
        <a-button v-else disabled>
          ????????????
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
              loadRecords(false);
            },
          );
        },
      }">
        <template #icon>
          <PlusSquareOutlined />
        </template>
        ????????????
      </ToolbarButton>

      <ToolbarButton v-bind="{
        loading: loadingRecords,
        disabled: !activeTableName || tableNotFound,
        onClick: () => {
          loadRecords(true);
        },
      }">
        <template #icon>
          <ReloadOutlined />
        </template>
        ????????????
      </ToolbarButton>

      <a-dropdown>
        <a-button type="link">
          ????????????
          <DownOutlined />
        </a-button>
        <template #overlay>
          <a-menu>

            <a-menu-item @click="tableManagementModalVisible = true" v-bind="{
              disabled: tableManagementModalVisible,
            }">
              <a-space>
                <ToolOutlined style="color: #19F;" />
                ????????????
              </a-space>
            </a-menu-item>

            <a-menu-item @click="renameTable(activeTableName!, true)" v-bind="{
              disabled: !activeTableName || tableNotFound,
            }">
              <a-space>
                <FormOutlined style="color: #F90;" />
                ????????????
              </a-space>
            </a-menu-item>

            <a-menu-item @click="deleteTable([activeTableName!], true)" v-bind="{
              disabled: !activeTableName || tableNotFound,
            }">
              <a-space>
                <DeleteOutlined style="color: #F31;" />
                ????????????
              </a-space>
            </a-menu-item>

          </a-menu>
        </template>
      </a-dropdown>

    </div>

    <a-alert v-if="!activeTableName" v-bind="{
      type: 'info',
      showIcon: true,
      message: '??????????????????????????????/????????????????????????',
    }" />

    <a-alert v-else-if="tableNotFound" v-bind="{
      type: 'warning',
      showIcon: true,
      message: '????????????????????????????????????????????????????????????',
    }" />

    <RecordTable v-else v-bind="{
      records,
      tableName: activeTableName,
      loading: loadingRecords,
      showActions: true,
      updater: loadRecords,
    }" />

    <TableManagementModal />
    <RecordModal :suggestion-source="records" />
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
