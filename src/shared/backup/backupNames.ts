import { ref } from 'vue';
import { message } from 'ant-design-vue';
import { displayErrorMessage } from '../common';

const validateBackupNames = (names: unknown): names is string[] => (
    Array.isArray(names)
    && names.every(v => (typeof v === 'string'))
);

export const backupNames = ref<string[]>([]);
export const loadingBackupNames = ref(false);

export const updateBackupNames = async (
    onSuccess?: () => void,
) => {

    if (loadingBackupNames.value) {
        return;
    }
    loadingBackupNames.value = true;

    const response = await fetch('/api/backup/list');
    if (response.status === 200) {
        try {
            const result = await response.json();
            if (validateBackupNames(result)) {
                backupNames.value = result;
                onSuccess?.();
            } else {
                message.error('后台返回的备份列表格式有误');
            }
        } catch {
            message.error('更新备份列表时出错');
        }
    } else {
        await displayErrorMessage(response, '获取备份列表时出错');
    }

    loadingBackupNames.value = false;

};
