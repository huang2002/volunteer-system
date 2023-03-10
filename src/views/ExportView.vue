<script setup lang="ts">
import { merge } from '3h-utils';
import ToolbarButton from '@/components/ToolbarButton.vue';
import { displayErrorMessage } from '@/shared/common';
import { loadingTableNames, tableNames, updateTableNames } from '@/shared/table/tableNames';
import { CheckOutlined, CloseOutlined, FolderOpenOutlined, QuestionCircleOutlined, SyncOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { computed, onMounted, reactive, ref, shallowRef, watch } from 'vue';

onMounted(async () => {
  await updateTableNames(false);
  selectedTableNames.value = tableNames.value.slice();
});

interface ExportFormState {
  level: string;
  begin_date: undefined | string;
  end_date: undefined | string;
  format: string;
  encoding: undefined | string;
  suffix_encoding: boolean;
}

const defaultExportFormState: ExportFormState = {
  level: 'school',
  begin_date: undefined,
  end_date: undefined,
  format: 'xlsx',
  encoding: undefined,
  suffix_encoding: true,
};

const exportFormState = reactive<ExportFormState>({ ...defaultExportFormState });

const tableSelectVisible = ref(false);
const selectedTableNames = shallowRef<string[]>([]);
watch(tableNames, (names) => {
  selectedTableNames.value = selectedTableNames.value.filter(
    (name) => names.includes(name)
  );
});

const allSelected = computed(() => (
  selectedTableNames.value.length === tableNames.value.length
));

const indeterminate = computed(() => {
  const selected = selectedTableNames.value;
  const all = tableNames.value;
  return (selected.length > 0) && (selected.length < all.length);
});

const onClickSelectAll = () => {
  if (indeterminate.value || !allSelected.value) {
    selectedTableNames.value = tableNames.value.slice();
  } else {
    selectedTableNames.value = [];
  }
};

const paramNames: (keyof ExportFormState)[] = [
  'begin_date',
  'end_date',
  'format',
  'encoding',
  'suffix_encoding',
];

const commonFormLayout = {
  labelCol: { span: 6 },
  wrapperCol: { span: 14 },
};

const formTailLayout = {
  wrapperCol: {
    offset: commonFormLayout.labelCol.span,
    span: 14,
  },
};

const exporting = ref(false);
const onSubmit = async () => {

  if (exporting.value) {
    return;
  }
  exporting.value = true;

  const options = merge(exportFormState);

  const params = new URLSearchParams();
  paramNames.forEach((name) => {
    if (options[name]) {
      params.append(name, String(options[name]));
    }
  });
  params.append(
    'tables',
    selectedTableNames.value.join(',')
  );

  try {
    const url = `/api/export/create/${options.level}?${params.toString()}`;
    const response = await fetch(url, { method: 'POST' });
    if (response.status === 200) {
      message.success('????????????');
    } else {
      await displayErrorMessage(response, '???????????????');
    }
  } catch {
    message.error('????????????');
  }

  exporting.value = false;

};

const onReset = () => {
  Object.assign(exportFormState, defaultExportFormState);
  selectedTableNames.value = tableNames.value.slice();
};

const openingExportFolder = ref(false);
const openExportFolder = async () => {

  if (openingExportFolder.value) {
    return;
  }
  openingExportFolder.value = true;

  try {
    const response = await fetch('/api/export/show', { method: 'POST' });
    if (response.status === 200) {
      message.success('????????????');
    } else {
      await displayErrorMessage(response, '??????????????????????????????');
    }
  } catch {
    message.error('????????????');
  }

  openingExportFolder.value = false;

};
</script>

<template>
  <div id="export-view" class="view">

    <div id="export-header">
      <h2 id="export-title">????????????</h2>
      <ToolbarButton v-bind="{
        loading: openingExportFolder,
        onClick: openExportFolder,
      }">
        <template #icon>
          <FolderOpenOutlined style="color: #F90;" />
        </template>
        ??????????????????
      </ToolbarButton>
    </div>

    <a-form :model="exportFormState" v-bind="{
      id: 'export-form',
      ...commonFormLayout
    }">

      <a-form-item label="????????????">
        <a-button @click="tableSelectVisible = true">
          ??????????????????
        </a-button>
      </a-form-item>

      <a-form-item label="????????????" name="level" required>
        <a-radio-group v-model:value="exportFormState.level">
          <a-radio-button value="school">??????</a-radio-button>
          <a-radio-button value="grade">??????</a-radio-button>
          <a-radio-button value="class">??????</a-radio-button>
        </a-radio-group>
      </a-form-item>

      <a-form-item name="begin_date">
        <template #label>
          <a-space>
            ????????????
            <a-tooltip color="blue" title="????????????????????????????????????????????????">
              <QuestionCircleOutlined style="color: #19F;" />
            </a-tooltip>
          </a-space>
        </template>
        <a-date-picker v-model:value="exportFormState.begin_date" v-bind="{
          placeholder: '????????????',
          mode: 'date',
          valueFormat: 'YYYY/MM/DD',
          format: [ // for parsing
            'YYYY/MM/DD',
            'YYYY-MM-DD',
            'YYYY.MM.DD',
            'YYYYMMDD',
          ],
          style: { width: '100%' },
        }" />
      </a-form-item>

      <a-form-item name="end_date">
        <template #label>
          <a-space>
            ????????????
            <a-tooltip color="blue" title="????????????????????????????????????????????????">
              <QuestionCircleOutlined style="color: #19F;" />
            </a-tooltip>
          </a-space>
        </template>
        <a-date-picker v-model:value="exportFormState.end_date" v-bind="{
          placeholder: '????????????',
          mode: 'date',
          valueFormat: 'YYYY/MM/DD',
          format: [ // for parsing
            'YYYY/MM/DD',
            'YYYY-MM-DD',
            'YYYY.MM.DD',
            'YYYYMMDD',
          ],
          style: { width: '100%' },
        }" />
      </a-form-item>

      <a-form-item label="????????????" name="format" required>
        <a-select v-model:value="exportFormState.format">
          <a-select-option value="xlsx">Excel?????????.xlsx???</a-select-option>
          <a-select-option value="csv">?????????????????????.csv???</a-select-option>
          <a-select-option value="tsv">????????????????????????.tsv???</a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item name="encoding">
        <template #label>
          <a-space>
            ????????????
            <a-tooltip color="blue" title="?????????????????????????????????????????????????????????">
              <QuestionCircleOutlined style="color: #19F;" />
            </a-tooltip>
          </a-space>
        </template>
        <a-auto-complete v-model:value="exportFormState.encoding" v-bind="{
          placeholder: '???????????????',
          dataSource: ['utf8', 'gb2312', 'gbk'],
        }">
          <a-input name="encoding" allow-clear />
        </a-auto-complete>
      </a-form-item>

      <a-form-item name="suffix_encoding" v-bind="formTailLayout">
        <a-checkbox v-model:checked="exportFormState.suffix_encoding">
          ?????????????????????????????????
        </a-checkbox>
      </a-form-item>

      <a-form-item v-bind="formTailLayout">
        <a-space>

          <a-button @click="onSubmit()" v-bind="{
            type: 'primary',
            loading: exporting,
          }">
            ??????
          </a-button>

          <a-button @click="onReset()">
            ??????
          </a-button>

        </a-space>
      </a-form-item>

    </a-form>

    <a-drawer v-model:visible="tableSelectVisible" v-bind="{
      title: '??????????????????',
      bodyStyle: {
        paddingTop: '0',
      },
    }">

      <template #extra>
        <a-button type="primary" @click="tableSelectVisible = false">
          ??????
        </a-button>
      </template>

      <a-checkbox-group v-model:value="selectedTableNames" style="width: 100%;">
        <a-list :data-source="tableNames" size="small">

          <template #header>
            <div id="export-table-select-header">

              <a-button @click="onClickSelectAll()" v-bind="{
                disabled: loadingTableNames || !tableNames.length,
              }">
                <template #icon>
                  <CloseOutlined v-if="allSelected" />
                  <CheckOutlined v-else />
                </template>
                <template v-if="allSelected">
                  ????????????
                </template>
                <template v-else>
                  ????????????
                </template>
              </a-button>

              <a-button @click="updateTableNames(true)" v-bind="{
                type: 'link',
                loading: loadingTableNames,
              }">
                <template #icon>
                  <SyncOutlined />
                </template>
                ????????????
              </a-button>

            </div>
          </template>

          <template #renderItem="{ item }">
            <a-list-item :title="item">
              <a-checkbox :value="item">{{ item }}</a-checkbox>
            </a-list-item>
          </template>

        </a-list>
      </a-checkbox-group>

    </a-drawer>

  </div>
</template>

<style scoped>
#export-view {
  display: flex;
  flex-direction: column;
  padding: 32px 40px;
}

#export-header {
  display: flex;
  margin-bottom: 24px;
}

#export-title {
  margin-right: auto;
  font-weight: bold;
}

#export-form {
  width: 500px;
  margin: 0 auto;
}

#export-table-select-header {
  display: flex;
  justify-content: space-between;
}
</style>
