import { message } from 'ant-design-vue';
import { ref } from 'vue';
import { displayErrorMessage } from '../common';
import { tableNameModalDefaults, tableNameModalPending, tableNameModalVisible, inputTableName, type TableNameModalState } from './tableNameModal';
import { updateTableNames } from './tableNames';

export const tableActionDisabled = ref(false);

export const createTable = async (
    onSuccess?: (newTableName: TableNameModalState) => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    const submitted = await inputTableName(
        '新建表格',
        tableNameModalDefaults,
    );
    if (!submitted) { // canceled
        tableActionDisabled.value = false;
        return;
    }

    const response = await fetch(
        `/api/create/table/${submitted.name}`
    );
    if (response.status === 200) {
        message.success('新建表格成功');
        await updateTableNames();
        onSuccess?.(submitted);
    } else {
        await displayErrorMessage(response, '新建表格时出错');
    }

    tableNameModalPending.value = false;
    tableNameModalVisible.value = false;
    tableActionDisabled.value = false;

};

export const renameTable = async (
    source: string,
    onSuccess?: (destination: TableNameModalState) => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    const submitted = await inputTableName('重命名表格', {
        ...tableNameModalDefaults,
        name: source,
    });
    if (!submitted) { // canceled
        tableActionDisabled.value = false;
        return;
    }

    const response = await fetch(
        `/api/rename/table/${source}/${submitted.name}`
    );
    if (response.status === 200) {
        message.success('重命名表格成功');
        await updateTableNames();
        onSuccess?.(submitted);
    } else {
        await displayErrorMessage(response, '重命名表格时出错');
    }

    tableNameModalPending.value = false;
    tableNameModalVisible.value = false;
    tableActionDisabled.value = false;

};
