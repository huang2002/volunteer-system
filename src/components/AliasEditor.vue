<script setup lang="ts">
import { aliasActionDisabled, updateAliasList, type AliasViewResult } from '@/shared/alias/aliasActions';
import { aliasEditorVisible } from '@/shared/alias/aliasEditor';
import { displayErrorMessage } from '@/shared/common';
import { CheckOutlined, ClearOutlined, CloseOutlined, DeleteOutlined, EditOutlined, PlusSquareOutlined, SyncOutlined, WarningOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';
import { computed, h, onBeforeMount, ref, shallowRef, watch } from 'vue';
import ToolbarButton from './ToolbarButton.vue';

const props = defineProps<{
  columnName: string;
  listName: string;
}>();

const emit = defineEmits<{
  (event: 'update'): void;
}>();

onBeforeMount(() => {
  loadAliases(false);
});
watch(props, () => {
  loadAliases(false);
});

const aliases = shallowRef<string[]>([]);
const loadingAliases = ref(false);
const loadAliases = async (
  alertSuccess: boolean,
) => {
  if (!props.columnName) {
    return;
  }
  loadingAliases.value = true;
  try {
    const response = await fetch(`/api/alias/view/${props.columnName}`);
    if (response.status === 200) {
      const result = await response.json() as AliasViewResult;
      aliases.value = result
        .find((item) => (item.name === props.listName))!
        .aliases;
      if (alertSuccess) {
        message.success('刷新成功');
      }
    } else {
      await displayErrorMessage(response, '获取数据时出错');
    }
  } catch {
    message.error('获取数据失败');
  }
  loadingAliases.value = false;
};

const updateAlias = (
  oldAlias: string,
) => {
  const newAlias = prompt('请输入新的别名：', oldAlias);
  if (!newAlias) {
    return;
  }
  updateAliasList(
    props.columnName,
    props.listName,
    aliases.value.map(
      (alias) => ((alias === oldAlias) ? newAlias : alias)
    ),
    () => {
      loadAliases(false);
      emit('update');
    },
  );
};

const deleteAlias = (
  targetAlias: string,
) => {
  Modal.confirm({
    title: `删除别名：${targetAlias}`,
    content: '确定要删除此条别名吗？',
    icon: h(WarningOutlined, { style: { color: '#F90' } }),
    okButtonProps: { danger: true },
    okText: '确认',
    cancelButtonProps: { type: 'primary' },
    cancelText: '取消',
    autoFocusButton: 'cancel',
    closable: true,
    maskClosable: true,
    onOk() {
      updateAliasList(
        props.columnName,
        props.listName,
        aliases.value.filter(
          (alias) => (alias !== targetAlias)
        ),
        () => {
          loadAliases(false);
          emit('update');
        },
      );
    },
  });
};

const appendAlias = () => {
  const newAlias = prompt('请输入新的别名：');
  if (!newAlias) {
    return;
  }
  updateAliasList(
    props.columnName,
    props.listName,
    aliases.value.concat(newAlias),
    () => {
      loadAliases(false);
      emit('update');
    },
  );
};

const selectedAliases = shallowRef<string[]>([]);
const deleteSelectedAliases = () => {
  Modal.confirm({
    title: `删除别名`,
    content: `即将删除别名：${selectedAliases.value.join('、')}。`,
    icon: h(WarningOutlined, { style: { color: '#F90' } }),
    okButtonProps: { danger: true },
    okText: '确认',
    cancelButtonProps: { type: 'primary' },
    cancelText: '取消',
    autoFocusButton: 'cancel',
    closable: true,
    maskClosable: true,
    onOk() {
      updateAliasList(
        props.columnName,
        props.listName,
        aliases.value.filter(
          (alias) => !selectedAliases.value.includes(alias)
        ),
        () => {
          loadAliases(false);
          emit('update');
        },
      );
    },
  });
};

const allChecked = computed(() => (
  selectedAliases.value.length === aliases.value.length
));

const indeterminate = computed(() => {
  const selected = selectedAliases.value;
  const all = aliases.value;
  return (selected.length > 0) && (selected.length < all.length);
});

const onClickCheckAll = () => {
  if (indeterminate.value || !allChecked.value) {
    selectedAliases.value = aliases.value.slice();
  } else {
    selectedAliases.value = [];
  }
};
</script>

<template>
  <a-drawer v-model:visible="aliasEditorVisible" v-bind="{
    title: `别名管理：${listName}`,
    width: 500,
    bodyStyle: {
      padding: '12px 24px',
    },
  }">

    <a-checkbox-group v-model:value="selectedAliases" :style="{
      width: '100%',
    }">
      <a-list v-bind="{
        loading: loadingAliases,
        dataSource: aliases,
      }">

        <template #header>
          <div id="alias-editor-header">

            <a-button @click="onClickCheckAll()" v-bind="{
              id: 'alias-editor-select-all',
              disabled: loadingAliases || !aliases.length,
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
              loading: loadingAliases,
              onClick: () => {
                loadAliases(true);
              },
            }">
              <template #icon>
                <SyncOutlined />
              </template>
              刷新列表
            </ToolbarButton>

            <ToolbarButton v-bind="{
              danger: true,
              disabled: aliasActionDisabled || loadingAliases || !selectedAliases.length,
              onClick: deleteSelectedAliases,
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

            <a-checkbox :value="item">
              {{ item as string }}
            </a-checkbox>

            <template #actions>

              <a-button @click="updateAlias(item as string)" v-bind="{
                type: 'link',
                size: 'small',
                disabled: aliasActionDisabled,
              }">
                <template #icon>
                  <EditOutlined />
                </template>
                修改
              </a-button>

              <a-button @click="deleteAlias(item as string)" v-bind="{
                type: 'link',
                size: 'small',
                danger: true,
                disabled: aliasActionDisabled,
              }">
                <template #icon>
                  <DeleteOutlined />
                </template>
                删除
              </a-button>

            </template>

          </a-list-item>
        </template>

        <template #loadMore>
          <div class="flex-centered" style="padding: 12px 0;">
            <a-button @click="appendAlias()" v-bind="{
              type: 'primary',
              disabled: loadingAliases,
            }">
              <template #icon>
                <PlusSquareOutlined />
              </template>
              添加别名
            </a-button>
          </div>
        </template>

      </a-list>
    </a-checkbox-group>

  </a-drawer>
</template>

<style scoped>
#alias-editor-header {
  display: flex;
  align-items: baseline;
}

#alias-editor-select-all {
  margin-right: auto;
}

.toolbar-button {
  margin-left: 12px;
}
</style>
