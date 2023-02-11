import { ref } from 'vue';
import { message } from 'ant-design-vue';
import { displayErrorMessage } from '../common';

export const TABLE_NAME_PATTERN = /^\d{2}$/;
export const TABLE_NAME_PATTERN_SEARCH = /\d{2}/;
export const validateTableName = (name: unknown): name is string => (
    (typeof name === 'string')
    && TABLE_NAME_PATTERN.test(name)
);
export const validateTableNames = (names: unknown): names is string[] => (
    Array.isArray(names)
    && names.every(validateTableName)
);

export const tableNames = ref<string[]>([]);
export const loadingTableNames = ref(false);

export const updateTableNames = async (
    onSuccess?: () => void,
) => {

    if (loadingTableNames.value) {
        return;
    }
    loadingTableNames.value = true;

    const response = await fetch('/api/table/list');
    if (response.status === 200) {
        try {
            const result = await response.json();
            if (validateTableNames(result)) {
                tableNames.value = result;
                onSuccess?.();
            } else {
                message.error('后台返回的表名格式有误');
            }
        } catch {
            message.error('更新表名时出错');
        }
    } else {
        await displayErrorMessage(response, '获取表名时出错');
    }

    loadingTableNames.value = false;

};
