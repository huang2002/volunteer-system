import { message, type UploadProps } from 'ant-design-vue';
import { ref } from 'vue';
import { CONTENT_TYPE_JSON, displayErrorMessage } from '../common';
import type { ActivityRecord } from '../record/recordModal';
import { createTable } from '../table/tableActions';
import { tableNames, updateTableNames } from '../table/tableNames';
import { importConfirmModalPending, importConfirmModalVisible, inputImportConfirm } from './importConfirmModal';

export type FileType = Parameters<
    Exclude<UploadProps['beforeUpload'], undefined>
>[0];

export const importActionDisabled = ref(false);

export const previewImport = async (
    fileList: FileType[],
    onSuccess: (previewData: ActivityRecord[]) => void,
    onFailure: () => void,
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

    try {
        const url = `/api/import/preview`;
        const response = await fetch(url, {
            method: 'POST',
            body: formData,
        });
        if (response.status === 200) {
            const previewData = await response.json();
            onSuccess(previewData);
            message.success('预览加载成功');
        } else {
            await displayErrorMessage(response, '预览生成失败');
            onFailure();
        }
    } catch {
        message.error('预览加载失败');
        onFailure();
    }

    importActionDisabled.value = false;

};

export const createImport = async (
    data: ActivityRecord[],
    onSuccess?: () => void,
) => {

    if (importActionDisabled.value) {
        return;
    }
    importActionDisabled.value = true;

    await updateTableNames(false);

    const submitted = await inputImportConfirm(data);
    if (!submitted) { // canceled
        importActionDisabled.value = false;
        return;
    }

    try {

        for await (const tableName of Object.keys(submitted)) {

            if (!tableNames.value.includes(tableName)) {
                await createTable(
                    { name: tableName },
                    false,
                    false,
                );
            }

            const records = submitted[tableName];
            const url = `/api/table/append/${tableName}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': CONTENT_TYPE_JSON,
                },
                body: JSON.stringify(records),
            });

            if (response.status !== 200) {
                await displayErrorMessage(response, '导入记录时出错');
                throw new Error('导入记录失败');
            }

        }

        message.success('导入成功');
        onSuccess?.();

    } catch {
        // pass
    }

    importConfirmModalPending.value = false;
    importConfirmModalVisible.value = false;
    importActionDisabled.value = false;

};
