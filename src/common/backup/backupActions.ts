import { message } from 'ant-design-vue';
import { ref } from 'vue';
import { createBackupModalDefaults, createBackupModalPending, createBackupModalVisible, inputBackupName, type CreateBackupModalState } from './createBackupModal';
import { updateBackupNames } from './backupNames';

export const backupActionDisabled = ref(false);

export const createBackup = async (
    onSuccess?: (newBackupName: CreateBackupModalState) => void,
) => {

    if (backupActionDisabled.value) {
        return;
    }
    backupActionDisabled.value = true;

    const submitted = await inputBackupName(createBackupModalDefaults);
    if (!submitted) { // canceled
        backupActionDisabled.value = false;
        return;
    }

    const response = await fetch(`/api/create/backup/${submitted.name}`);
    if (response.status === 200) {
        await updateBackupNames();
        onSuccess?.(submitted);
    } else {
        try {
            const errorText = await response.text();
            message.error(errorText);
        } catch {
            message.error('新建表格时出错');
        }
    }

    createBackupModalPending.value = false;
    createBackupModalVisible.value = false;
    backupActionDisabled.value = false;

};
