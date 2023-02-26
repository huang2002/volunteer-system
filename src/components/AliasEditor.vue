<script setup lang="ts">
import { aliasActionDisabled, updateAliasList, type AliasViewResult } from '@/shared/alias/aliasActions';
import { aliasEditorVisible } from '@/shared/alias/aliasEditor';
import { displayErrorMessage } from '@/shared/common';
import { ClearOutlined, DeleteOutlined, EditOutlined, PlusSquareOutlined, SyncOutlined, TagOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { onBeforeMount, ref, shallowRef, watch } from 'vue';
import ToolbarButton from './ToolbarButton.vue';

const props = defineProps<{
  columnName: string;
  listName: string;
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
    },
  );
};

const deleteAlias = (
  targetAlias: string,
) => {
  updateAliasList(
    props.columnName,
    props.listName,
    aliases.value.filter(
      (alias) => (alias !== targetAlias)
    ),
    () => {
      loadAliases(false);
    },
  );
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
    },
  );
};

const selectedAliases = ref<string[]>([]);
const deleteAliases = () => {
  updateAliasList(
    props.columnName,
    props.listName,
    aliases.value.filter(
      (alias) => !selectedAliases.value.includes(alias)
    ),
    () => {
      loadAliases(false);
    },
  );
};
</script>

<template>
  <a-drawer v-model:visible="aliasEditorVisible" v-bind="{
    title: '别名管理',
    width: 600,
  }">

    <div id="alias-editor-toolbar">

      <p id="alias-editor-title">
        <span id="alias-editor-list-name">{{ listName }}</span>
        的别名：
      </p>

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
        onClick: deleteAliases,
      }">
        <template #icon>
          <ClearOutlined />
        </template>
        删除选中
      </ToolbarButton>

    </div>

    <a-checkbox-group v-model:value="selectedAliases" :style="{
      width: '100%',
    }">
      <a-list v-bind="{
        size: 'small',
        bordered: true,
        loading: loadingAliases,
        dataSource: aliases,
      }">

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
            <a-button type="primary" @click="appendAlias()">
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
#alias-editor-toolbar {
  display: flex;
  align-items: baseline;
  margin-bottom: 12px;
}

#alias-editor-title {
  margin: 0;
  margin-right: auto;
  font-size: 1.2em;
}

#alias-editor-list-name {
  font-weight: bold;
}

.toolbar-button {
  margin-left: 12px;
}
</style>
