<script setup lang="ts">
import AliasEditor from '@/components/AliasEditor.vue';
import { type AliasViewResult, deleteAliasList, type AliasViewResultItem, updateAliasList } from '@/shared/alias/aliasActions';
import { showAliasEditor } from '@/shared/alias/aliasEditor';
import { displayErrorMessage } from '@/shared/common';
import { DeleteOutlined, EditOutlined, PlusOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { computed, onBeforeMount, ref, shallowRef, watch } from 'vue';

onBeforeMount(() => {
  loadAliasLists(false);
});

const columnName = ref('student_school');
const listName = ref('');
watch(columnName, () => {
  loadAliasLists(false);
});

const aliasLists = shallowRef<AliasViewResult>([]);
const aliasListNames = computed(() => (
  aliasLists.value.map(
    (item) => (item.name)
  )
));
watch(aliasListNames, (listNames) => {
  if (
    listNames.length
    && !listNames.includes(listName.value)
  ) {
    listName.value = listNames[0];
  }
});

const loadingAliasLists = ref(false);
const loadAliasLists = async (
  alertSuccess: boolean,
) => {
  if (!columnName.value) {
    return;
  }
  loadingAliasLists.value = true;
  try {
    const response = await fetch(`/api/alias/view/${columnName.value}`);
    if (response.status === 200) {
      const result = await response.json() as AliasViewResult;
      aliasLists.value = result;
      if (alertSuccess) {
        message.success('刷新成功');
      }
    } else {
      await displayErrorMessage(response, '获取数据时出错');
    }
  } catch {
    message.error('获取数据失败');
  }
  loadingAliasLists.value = false;
};

const editAliasList = (
  currentListName: string,
) => {
  listName.value = currentListName;
  showAliasEditor();
};

const createAliasList = () => {
  const newListName = prompt('请输入原始名称：');
  if (!newListName) {
    return;
  }
  updateAliasList(
    columnName.value,
    newListName,
    [],
    () => {
      loadAliasLists(false);
    },
  );
};

// TODO: batch deletion
</script>

<template>
  <div id="alias-view" class="view">

    <a-list v-bind="{
      id: 'alias-list',
      dataSource: aliasLists,
      bordered: true,
      loading: loadingAliasLists,
    }">

      <template #header>
        <div id="alias-list-header">

          <a-input-group id="alias-list-control" compact>
            <a-tooltip v-bind="{
              color: 'blue',
              title: '刷新别名列表',
            }">
              <a-button @click="loadAliasLists(true)" v-bind="{
                loading: loadingAliasLists,
              }">
                <template #icon>
                  <SyncOutlined />
                </template>
              </a-button>
            </a-tooltip>
            <a-select v-model:value="columnName" v-bind="{
              id: 'alias-list-select',
              disabled: loadingAliasLists,
            }">
              <a-select-option value="student_school">学院名称</a-select-option>
            </a-select>
          </a-input-group>

          <a-button type="primary" @click="createAliasList()">
            <template #icon>
              <PlusOutlined />
            </template>
            新建别名
          </a-button>

        </div>
      </template>

      <template #renderItem="{ item }">
        <a-list-item>

          <a-space>
            <a-typography-text>
              {{ (item as AliasViewResultItem).name }}
            </a-typography-text>
            <a-typography-text v-bind="{
              type: 'secondary',
              ellipsis: true,
              content: (item as AliasViewResultItem).aliases.join('，'),
            }" />
          </a-space>

          <template #actions>

            <a-button type="link" @click="editAliasList(
              (item as AliasViewResultItem).name
            )">
              <template #icon>
                <EditOutlined />
              </template>
              编辑
            </a-button>

            <a-button type="link" danger @click="deleteAliasList(
              columnName,
              (item as AliasViewResultItem).name,
            )">
              <template #icon>
                <DeleteOutlined />
              </template>
              删除
            </a-button>

          </template>

        </a-list-item>
      </template>

    </a-list>

    <AliasEditor :column-name="columnName" :list-name="listName" />

  </div>
</template>

<style scoped>
#alias-view {
  padding: 32px;
}

#alias-list-header {
  display: flex;
  white-space: nowrap;
  overflow-x: auto;
}

#alias-list-select {
  width: 6em;
}
</style>
