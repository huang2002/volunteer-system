import { WarningOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';
import { h, ref } from 'vue';
import { displayErrorMessage } from '../common';
import { tableNameModalDefaults, tableNameModalPending, tableNameModalVisible, inputTableName, type TableNameModalState } from './tableNameModal';
import { updateTableNames } from './tableNames';

export const tableActionDisabled = ref(false);

export const createTable = async (
    init?: TableNameModalState | null,
    onSuccess?: (newTableName: TableNameModalState) => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    let submitted = init;
    if (!submitted) {
        submitted = await inputTableName(
            '新建表格',
            tableNameModalDefaults,
        );
        if (!submitted) { // canceled
            tableActionDisabled.value = false;
            return;
        }
    }

    const response = await fetch(
        `/api/create/table/${submitted.name}`
    );
    if (response.status === 200) {
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

export const deleteTable = (
    tableName: string,
    onSuccess?: () => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    Modal.confirm({
        title: `删除表格“${tableName}”`,
        content: '确定要删除此条表格吗？',
        icon: h(WarningOutlined, { style: { color: '#F90' } }),
        okButtonProps: { danger: true },
        okText: '确认',
        cancelButtonProps: { type: 'primary' },
        cancelText: '取消',
        autoFocusButton: 'cancel',
        closable: true,
        maskClosable: true,
        async onOk() {
            const response = await fetch(
                `/api/delete/table/${tableName}`
            );
            if (response.status === 200) {
                message.success('删除成功');
                await updateTableNames();
                onSuccess?.();
            } else {
                await displayErrorMessage(response, '删除表格时出错');
            }
            tableActionDisabled.value = false;
        },
        onCancel() {
            tableActionDisabled.value = false;
        },
    });

};
