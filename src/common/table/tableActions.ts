import { message } from 'ant-design-vue';
import { ref } from 'vue';
import {
    createTableModalDefaults, createTableModalPending,
    createTableModalVisible, inputTableName, type CreateTableModalState,
} from './createTableModal';
import { updateTableNames } from './tableNames';

export const tableActionDisabled = ref(false);

export const createTable = async (
    onSuccess?: (newTableName: CreateTableModalState) => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    const submitted = await inputTableName(createTableModalDefaults);
    if (!submitted) { // canceled
        tableActionDisabled.value = false;
        return;
    }

    const response = await fetch(`/api/create/table/${submitted.name}`);
    if (response.status === 200) {
        await updateTableNames();
        onSuccess?.(submitted);
    } else {
        try {
            const errorText = await response.text();
            message.error(errorText);
        } catch {
            message.error('新建表格时出错');
        }
    }

    createTableModalPending.value = false;
    createTableModalVisible.value = false;
    tableActionDisabled.value = false;

};
