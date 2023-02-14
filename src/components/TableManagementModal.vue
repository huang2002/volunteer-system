<script setup lang="ts">
import { KEY_TABLE_MANAGEMENT_MODAL_VISIBLE } from '@/shared/common';
import { createTable, renameTable, deleteTable } from '@/shared/table/tableActions';
import { loadingTableNames, tableNames, updateTableNames } from '@/shared/table/tableNames';
import { ClearOutlined, DeleteOutlined, FileAddOutlined, FormOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { inject, ref, watch } from 'vue';

const tableManagementModalVisible = inject(KEY_TABLE_MANAGEMENT_MODAL_VISIBLE)!;
const selectedTableNames = ref<string[]>([]);

watch(tableNames, (names) => {
  selectedTableNames.value = selectedTableNames.value.filter(
    (name) => (names.includes(name))
  );
});
</script>

<template>
  <a-modal v-model:visible="tableManagementModalVisible" v-bind="{
    title: '表格管理',
    width: 600,
    footer: null,
    style: {
      top: '32px',
    },
  }">
    <a-checkbox-group v-model:value="selectedTableNames" :style="{
      width: '100%',
    }">
      <a-list v-bind="{
        dataSource: tableNames,
        size: 'small',
        bordered: true,
        pagination: {
          size: 'small',
          defaultPageSize: 8,
          pageSizeOptions: ['8'],
          showLessItems: true,
          showTotal: (total: number, range: [number, number]) => (
            `第${range[0]}项到第${range[1]}项（共${total}项）`
          )
        },
      }">

        <template #header>

          <a-button @click="updateTableNames(true)" v-bind="{
            class: 'table-action',
            loading: loadingTableNames,
          }">
            <template #icon>
              <SyncOutlined style="color: #19F;" />
            </template>
            刷新列表
          </a-button>

          <a-button @click="deleteTable(selectedTableNames, true)" v-bind="{
            class: 'table-action',
            disabled: !selectedTableNames.length,
          }">
            <template #icon>
              <ClearOutlined style="color: #F44;" />
            </template>
            批量删除
          </a-button>

          <a-button @click="createTable(null, true)" v-bind="{
            id: 'table-action-create',
            type: 'primary',
          }">
            <template #icon>
              <FileAddOutlined />
            </template>
            新建表格
          </a-button>

        </template>

        <template #renderItem="{ item }">
          <a-list-item>

            <a-checkbox :value="item">
              {{ item }}
            </a-checkbox>

            <template #actions>

              <a-button @click="renameTable(item as string, true)" v-bind="{
                type: 'link',
                size: 'small',
              }">
                <template #icon>
                  <FormOutlined />
                </template>
                重命名
              </a-button>

              <a-button @click="deleteTable([item as string], true)" v-bind="{
                type: 'link',
                size: 'small',
                danger: true,
              }">
                <template #icon>
                  <DeleteOutlined />
                </template>
                删除
              </a-button>

            </template>
          </a-list-item>
        </template>

      </a-list>
    </a-checkbox-group>
  </a-modal>
</template>

<style scoped>
.table-action {
  margin-right: 12px;
}

#table-action-create {
  float: right;
}
</style>
