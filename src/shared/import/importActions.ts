import { message, type UploadProps } from 'ant-design-vue';
import { ref } from 'vue';
import { displayErrorMessage } from '../common';
import type { ActivityRecord } from '../record/recordModal';

export type FileType = Parameters<
    Exclude<UploadProps['beforeUpload'], undefined>
>[0];

export const importActionDisabled = ref(false);

export const previewImport = async (
    fileList: FileType[],
    onSuccess?: (previewData: ActivityRecord[]) => void,
    onFailure?: () => void,
) => {

    if (importActionDisabled.value) {
        return;
    }
    if (!fileList.length) {
        message.warn('请选择待导入文件');
        return;
    }
    importActionDisabled.value = true;

    const formData = new FormData();
    fileList.forEach((file) => {
        formData.append('files[]', file);
    });

    const url = `/api/import/preview`;
    const response = await fetch(url, {
        method: 'POST',
        body: formData,
    });
    if (response.status === 200) {
        try {
            const previewData = await response.json();
            onSuccess?.(previewData);
            message.success('预览加载成功');
        } catch {
            message.error('预览加载失败');
            onFailure?.();
        }
    } else {
        await displayErrorMessage(response, '预览生成失败');
        onFailure?.();
    }

    importActionDisabled.value = false;

};
