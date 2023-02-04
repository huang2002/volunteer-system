import { ref } from 'vue';
import { message } from 'ant-design-vue';

const validateTableNames = (names: unknown): names is string[] => (
    Array.isArray(names)
    && names.every(v => (typeof v !== 'string'))
);

export const tableNames = ref<string[]>([]);
export const loadingTableNames = ref(false);

export const updateTableNames = async () => {

    if (loadingTableNames.value) {
        return;
    }
    loadingTableNames.value = true;

    const response = await fetch('/api/list/tables');

    if (response.status === 200) {

        try {
            const result = await response.json();
            if (validateTableNames(result)) {
                tableNames.value = result;
            } else {
                message.error('后台返回的数据格式有误');
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

    loadingTableNames.value = false;

};
