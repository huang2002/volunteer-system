<script setup lang="ts">
import { merge } from '3h-utils';
import ToolbarButton from '@/components/ToolbarButton.vue';
import { displayErrorMessage } from '@/shared/common';
import { FolderOpenOutlined, QuestionCircleOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { reactive, ref } from 'vue';

interface ExportFormState {
  level: string;
  begin_date?: string;
  end_date?: string;
  format: string;
  encoding?: string;
  suffix_encoding: boolean;
}

const exportFormState = reactive<ExportFormState>({
  level: 'school',
  begin_date: undefined,
  end_date: undefined,
  format: 'xlsx',
  encoding: undefined,
  suffix_encoding: true,
});

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

  const url = `/api/export/create/${options.level}?${params.toString()}`;
  const response = await fetch(url);

  if (response.status === 200) {
    message.success('导出成功');
  } else {
    await displayErrorMessage(response, '导出失败');
  }

  exporting.value = false;

};

const openingExportFolder = ref(false);
const openExportFolder = async () => {

  if (openingExportFolder.value) {
    return;
  }
  openingExportFolder.value = true;

  const response = await fetch('/api/export/show');

  if (response.status === 200) {
    message.success('打开成功');
  } else {
    await displayErrorMessage(response, '打开失败');
  }

  openingExportFolder.value = false;

};
</script>

<template>
  <div id="export-view" class="view">

    <div id="export-header">
      <h2 id="export-title">导出报表</h2>
      <ToolbarButton v-bind="{
        loading: openingExportFolder,
        onClick: openExportFolder,
      }">
        <template #icon>
          <FolderOpenOutlined style="color: #F90;" />
        </template>
        打开导出目录
      </ToolbarButton>
    </div>

    <a-form :model="exportFormState" v-bind="{
      id: 'export-form',
      ...commonFormLayout
    }">

      <a-form-item label="导出级别" name="level" required>
        <a-radio-group v-model:value="exportFormState.level">
          <a-radio-button value="school">学院</a-radio-button>
          <a-radio-button value="grade">年级</a-radio-button>
          <a-radio-button value="class">班级</a-radio-button>
        </a-radio-group>
      </a-form-item>

      <a-form-item name="begin_date">
        <template #label>
          <a-space>
            开始日期
            <a-tooltip color="blue" title="筛选结束日期大于等于此日期的记录">
              <QuestionCircleOutlined style="color: #19F;" />
            </a-tooltip>
          </a-space>
        </template>
        <a-date-picker v-model:value="exportFormState.begin_date" v-bind="{
          placeholder: '不设限制',
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
            结束日期
            <a-tooltip color="blue" title="筛选开始日期小于等于此日期的记录">
              <QuestionCircleOutlined style="color: #19F;" />
            </a-tooltip>
          </a-space>
        </template>
        <a-date-picker v-model:value="exportFormState.end_date" v-bind="{
          placeholder: '不设限制',
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

      <a-form-item label="文件格式" name="format" required>
        <a-select v-model:value="exportFormState.format">
          <a-select-option value="xlsx">Excel表格（.xlsx）</a-select-option>
          <a-select-option value="csv">逗号分隔文件（.csv）</a-select-option>
          <a-select-option value="tsv">制表符分割文件（.tsv）</a-select-option>
        </a-select>
      </a-form-item>

      <a-form-item name="encoding">
        <template #label>
          <a-space>
            文件编码
            <a-tooltip color="blue" title="如果为空，将使用文件格式对应的默认编码">
              <QuestionCircleOutlined style="color: #19F;" />
            </a-tooltip>
          </a-space>
        </template>
        <a-auto-complete v-model:value="exportFormState.encoding" v-bind="{
          placeholder: '使用默认值',
          dataSource: ['utf8', 'gb2312', 'gbk'],
        }">
          <a-input name="encoding" allow-clear />
        </a-auto-complete>
      </a-form-item>

      <a-form-item name="suffix_encoding" v-bind="formTailLayout">
        <a-checkbox v-model:checked="exportFormState.suffix_encoding">
          将文件编码添加到文件名
        </a-checkbox>
      </a-form-item>

      <a-form-item v-bind="formTailLayout">
        <a-button @click="onSubmit()" v-bind="{
          type: 'primary',
          loading: exporting,
        }">
          导出
        </a-button>
      </a-form-item>

    </a-form>

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
</style>
