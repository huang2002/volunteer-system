import { ref, shallowRef } from 'vue';
import { message } from 'ant-design-vue';
import { displayErrorMessage } from '../common';

export const TABLE_NAME_PATTERN = /^[^\\/?:;~!@$%]+\d{2}级$/;
export const isValidTableName = (name: unknown): name is string => (
    (typeof name === 'string')
    && TABLE_NAME_PATTERN.test(name)
);

const isValidTableNames = (names: unknown): names is string[] => (
    Array.isArray(names)
    && names.every(isValidTableName)
);

export const tableNames = shallowRef<string[]>([]);
export const loadingTableNames = ref(false);

export const updateTableNames = async (
    alertSuccess: boolean,
) => {

    if (loadingTableNames.value) {
        return;
    }
    loadingTableNames.value = true;

    try {
        const response = await fetch('/api/table/list');
        if (response.status === 200) {
            const result = await response.json();
            if (isValidTableNames(result)) {
                tableNames.value = result;
                if (alertSuccess) {
                    message.success('刷新成功');
                }
            } else {
                message.error('后台返回的表名格式有误');
            }
        } else {
            await displayErrorMessage(response, '获取表名时出错');
        }
    } catch {
        message.error('更新表名失败');
    }

    loadingTableNames.value = false;

};
