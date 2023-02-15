<script setup lang="ts">
import ImportConfirmModal from '@/components/ImportConfirmModal.vue';
import RecordTable from '@/components/RecordTable.vue';
import ToolbarButton from '@/components/ToolbarButton.vue';
import { type FileType, importActionDisabled, previewImport, createImport } from '@/shared/import/importActions';
import type { ActivityRecord } from '@/shared/record/recordModal';
import { ArrowRightOutlined, CloseOutlined, CloudUploadOutlined, DeleteOutlined, FileSearchOutlined, QuestionCircleOutlined } from '@ant-design/icons-vue';
import type { UploadProps } from 'ant-design-vue';
import { ref, shallowRef } from 'vue';

const UPLOAD_ACCEPT = '.xlsx,.csv,.tsv,.gz';

const previewData = shallowRef<ActivityRecord[]>([]);
const loadingPreview = ref(false);
const fileList = shallowRef<FileType[]>([]);
const fileCount = ref(0);

const beforeUpload: UploadProps['beforeUpload'] = (file) => {
  fileList.value = [...fileList.value, file];
  return false;
};

const onRemove: UploadProps['onRemove'] = (file) => {
  fileList.value = fileList.value.filter((f) => (
    (f !== file)
    && (f !== file.originFileObj)
  ));
};

const loadPreview = () => {
  if (loadingPreview.value) {
    return;
  }
  loadingPreview.value = true;
  previewImport(
    fileList.value,
    (data) => {
      loadingPreview.value = false;
      previewData.value = data;
      fileCount.value = fileList.value.length;
      fileList.value = [];
    },
    () => {
      loadingPreview.value = false;
    },
  );
};
</script>

<template>
  <div id="import-view" class="view">

    <div id="toolbar">

      <h2 id="toolbar-title">
        导入数据
        <a-tooltip color="blue" placement="right">
          <template #title>
            提交待导入数据
            <ArrowRightOutlined />
            后台程序尝试识别并生成预览
            <ArrowRightOutlined />
            查看预览后确认
            <ArrowRightOutlined />
            系统自动导入对应表格
          </template>
          <QuestionCircleOutlined :style="{
            color: '#19F',
            fontSize: '0.8em',
          }" />
        </a-tooltip>
      </h2>

      <template v-if="previewData.length">
        <ToolbarButton v-bind="{
          danger: true,
          disabled: importActionDisabled,
          onClick: () => {
            previewData = [];
          },
        }">
          <template #icon>
            <CloseOutlined />
          </template>
          取消预览
        </ToolbarButton>
        <ToolbarButton v-bind="{
          type: 'primary',
          loading: importActionDisabled,
          disabled: !previewData.length,
          onClick: () => {
            createImport(
              previewData,
              () => {
                previewData = [];
              },
            );
          },
        }">
          <template #icon>
            <CloudUploadOutlined />
          </template>
          提交导入
        </ToolbarButton>
      </template>

      <template v-else>
        <ToolbarButton v-bind="{
          danger: true,
          disabled: !fileList.length || importActionDisabled,
          onClick: () => {
            fileList = [];
          },
        }">
          <template #icon>
            <DeleteOutlined />
          </template>
          清除选择
        </ToolbarButton>
        <ToolbarButton v-bind="{
          type: 'primary',
          loading: loadingPreview,
          disabled: !fileList.length || importActionDisabled,
          onClick: loadPreview,
        }">
          <template #icon>
            <FileSearchOutlined />
          </template>
          生成预览
        </ToolbarButton>
      </template>

    </div>

    <RecordTable v-if="previewData.length || loadingPreview" v-bind="{
      dataSource: previewData,
      loading: loadingPreview,
      importPreviewMode: true,
    }" />
    <div id="upload-wrapper" v-else>
      <a-upload-dragger v-bind="{
        fileList,
        multiple: true,
        accept: UPLOAD_ACCEPT,
        beforeUpload,
        onRemove,
      }">
        <a-empty id="upload-placeholder">
          <template #description>
            <p>
              点击此处
              <a-typography-text strong>选择文件</a-typography-text>
              ，也可直接将文件拖拽至此。
            </p>
            <p>
              （修改文件后请移除并重新选择；支持的文件类型：
              {{ UPLOAD_ACCEPT.replace(/,/g, '/') }}
              。）
            </p>
          </template>
        </a-empty>
      </a-upload-dragger>
    </div>

    <ImportConfirmModal v-bind="{
      fileCount: fileCount,
      recordCount: previewData.length,
    }" />

  </div>
</template>

<style scoped>
#toolbar {
  display: flex;
  margin-bottom: 8px;
}

#toolbar-title {
  margin: 0;
  margin-right: auto;
  padding-left: 0.2em;
  font-weight: bold;
}

.toolbar-button {
  margin-left: 8px;
}

#upload-wrapper {
  padding-bottom: 1em;
}

#upload-placeholder {
  padding: 24px 0;
}
</style>
