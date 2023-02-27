import { WarningOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';
import { h, ref } from 'vue';
import { CONTENT_TYPE_JSON, displayErrorMessage } from '../common';
import { tableNameModalDefaults, tableNameModalPending, tableNameModalVisible, inputTableName, type TableNameModalState } from './tableNameModal';
import { updateTableNames } from './tableNames';

export const tableActionDisabled = ref(false);

export const createTable = async (
    init: TableNameModalState | null,
    alertSuccess: boolean,
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

    try {
        const response = await fetch(
            `/api/table/create/${submitted.name}`,
            { method: 'POST' },
        );
        if (response.status === 200) {
            await updateTableNames(false);
            if (alertSuccess) {
                message.success('新建成功');
            }
        } else {
            await displayErrorMessage(response, '新建表格时出错');
        }
    } catch {
        message.error('新建表格失败');
    }

    tableNameModalPending.value = false;
    tableNameModalVisible.value = false;
    tableActionDisabled.value = false;

};

export const renameTable = async (
    source: string,
    alertSuccess: boolean,
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

    try {
        const response = await fetch(
            `/api/table/rename/${source}/${submitted.name}`,
            { method: 'POST' },
        );
        if (response.status === 200) {
            await updateTableNames(false);
            if (alertSuccess) {
                message.success('重命名表格成功');
            }
        } else {
            await displayErrorMessage(response, '重命名表格时出错');
        }
    } catch {
        message.error('重命名表格失败');
    }

    tableNameModalPending.value = false;
    tableNameModalVisible.value = false;
    tableActionDisabled.value = false;

};

export const deleteTable = (
    tableNames: string[],
    alertSuccess: boolean,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    Modal.confirm({
        title: `删除表格`,
        content: `将要删除的表格：${tableNames.join('、')}。`,
        icon: h(WarningOutlined, { style: { color: '#F90' } }),
        okButtonProps: { danger: true },
        okText: '确认',
        cancelButtonProps: { type: 'primary' },
        cancelText: '取消',
        autoFocusButton: 'cancel',
        closable: true,
        maskClosable: true,
        onOk: async () => {
            try {
                const response = await fetch(`/api/table/delete`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': CONTENT_TYPE_JSON,
                    },
                    body: JSON.stringify(tableNames),
                });
                if (response.status === 200) {
                    if (alertSuccess) {
                        message.success('删除成功');
                    }
                    await updateTableNames(false);
                } else {
                    await displayErrorMessage(response, '删除表格时出错');
                }
            } catch {
                message.error('删除表格失败');
            }
            tableActionDisabled.value = false;
        },
        onCancel() {
            tableActionDisabled.value = false;
        },
    });

};
