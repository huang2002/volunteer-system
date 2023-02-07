import { ref } from 'vue';
import { message } from 'ant-design-vue';

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

    const response = await fetch('/api/list/backups');

    if (response.status === 200) {

        try {
            const result = await response.json();
            if (validateBackupNames(result)) {
                backupNames.value = result;
                onSuccess?.();
            } else {
                message.error('后台返回的备份名称格式有误');
            }
        } catch {
            message.error('更新表名时出错');
        }

    } else {

        try {
            const errorText = await response.text();
            message.error(errorText);
        } catch {
            message.error('获取表名时出错');
        }

    }

    loadingBackupNames.value = false;

};
