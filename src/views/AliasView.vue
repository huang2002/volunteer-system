<script setup lang="ts">
import AliasEditor from '@/components/AliasEditor.vue';
import ToolbarButton from '@/components/ToolbarButton.vue';
import { type AliasViewResult, type AliasViewResultItem, updateAliasList, renameAliasList, deleteAliasLists, aliasActionDisabled } from '@/shared/alias/aliasActions';
import { showAliasEditor } from '@/shared/alias/aliasEditor';
import { displayErrorMessage } from '@/shared/common';
import { CheckOutlined, ClearOutlined, CloseOutlined, DeleteOutlined, EditOutlined, FormOutlined, PlusOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { computed, onBeforeMount, ref, shallowRef, watch } from 'vue';

onBeforeMount(() => {
  loadAliasLists(false);
});

const formatAliases = (item: AliasViewResultItem) => (
  item.aliases.join('，')
);

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

const selectedAliasListNames = shallowRef<string[]>([]);
const deleteSelectedAliasLists = () => {
  deleteAliasLists(
    columnName.value,
    selectedAliasListNames.value,
    () => {
      loadAliasLists(false);
    });
};

const allChecked = computed(() => (
  selectedAliasListNames.value.length === aliasLists.value.length
));

const indeterminate = computed(() => {
  const selected = selectedAliasListNames.value;
  const all = aliasLists.value;
  return (selected.length > 0) && (selected.length < all.length);
});

const onClickCheckAll = () => {
  if (indeterminate.value || !allChecked.value) {
    selectedAliasListNames.value = aliasListNames.value.slice();
  } else {
    selectedAliasListNames.value = [];
  }
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
</script>

<template>
  <div id="alias-view" class="view">

    <div id="alias-view-header">
      <h2 id="alias-view-title">别名管理</h2>
      <label for="alias-column-select">分类：</label>
      <a-select v-model:value="columnName" v-bind="{
        id: 'alias-column-select',
        disabled: loadingAliasLists,
        style: {
          width: '8em',
        },
      }">
        <a-select-option value="student_school">学院名称</a-select-option>
        <a-select-option value="student_class">班级名称</a-select-option>
      </a-select>
    </div>

    <a-checkbox-group v-model:value="selectedAliasListNames" :style="{
      width: '100%',
    }">
      <a-list v-bind="{
        id: 'alias-list',
        size: 'small',
        bordered: true,
        dataSource: aliasLists,
        loading: loadingAliasLists,
      }">

        <template #header>
          <div id="alias-list-header">

            <a-button @click="onClickCheckAll()" v-bind="{
              id: 'alias-list-select-all',
              disabled: loadingAliasLists,
            }">
              <template #icon>
                <CloseOutlined v-if="allChecked" />
                <CheckOutlined v-else />
              </template>
              <template v-if="allChecked">
                取消全选
              </template>
              <template v-else>
                全部选中
              </template>
            </a-button>

            <ToolbarButton v-bind="{
              type: 'primary',
              disabled: aliasActionDisabled,
              onClick: createAliasList,
            }">
              <template #icon>
                <PlusOutlined />
              </template>
              新建别名
            </ToolbarButton>

            <ToolbarButton v-bind="{
              disabled: aliasActionDisabled,
              loading: loadingAliasLists,
              onClick: () => {
                loadAliasLists(true);
              },
            }">
              <template #icon>
                <SyncOutlined />
              </template>
              刷新列表
            </ToolbarButton>

            <ToolbarButton v-bind="{
              danger: true,
              disabled: aliasActionDisabled || loadingAliasLists || !selectedAliasListNames.length,
              onClick: deleteSelectedAliasLists,
            }">
              <template #icon>
                <ClearOutlined />
              </template>
              删除选中
            </ToolbarButton>

          </div>
        </template>

        <template #renderItem="{ item }">
          <a-list-item>

            <div class="alias-list-item-text">
              <a-checkbox :value="(item as AliasViewResultItem).name">
                {{ (item as AliasViewResultItem).name }}
              </a-checkbox>
              <a-typography-text v-bind="{
                type: 'secondary',
                ellipsis: true,
                title: formatAliases(item as AliasViewResultItem),
                content: formatAliases(item as AliasViewResultItem),
              }" />
            </div>

            <template #actions>

              <a-button @click="editAliasList((item as AliasViewResultItem).name)" v-bind="{
                type: 'text',
                style: {
                  color: '#19F',
                },
              }">
                <template #icon>
                  <EditOutlined />
                </template>
                编辑
              </a-button>

              <a-button @click="renameAliasList(columnName, (item as AliasViewResultItem).name, () => { loadAliasLists(false); })" v-bind="{
                type: 'text',
                style: {
                  color: '#F90',
                },
              }">
                <template #icon>
                  <FormOutlined />
                </template>
                重命名
              </a-button>

              <a-button type="text" danger @click="deleteAliasLists(
                columnName,
                [(item as AliasViewResultItem).name],
                () => {
                  loadAliasLists(false);
                },
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
    </a-checkbox-group>

    <AliasEditor @update="loadAliasLists(false)" v-bind="{
      columnName,
      listName,
    }" />

  </div>
</template>

<style scoped>
#alias-view {
  padding: 32px;
}

#alias-view-header {
  display: flex;
  padding: 0 12px;
  margin-bottom: 12px;
  align-items: center;
}

#alias-view-title {
  margin: 0;
  margin-right: auto;
  font-weight: bold;
}

#alias-list-header {
  display: flex;
  padding: 5px 0;
  white-space: nowrap;
  overflow-x: auto;
}

#alias-list-select-all {
  margin-right: auto;
}

.toolbar-button {
  margin-left: 12px;
}

.alias-list-item-text {
  display: flex;
  white-space: nowrap;
  overflow: hidden;
}
</style>
