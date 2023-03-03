import { message, TypographyText } from 'ant-design-vue';
import { h, ref } from 'vue';
import { backupNameModalDefaults, backupNameModalPending, backupNameModalVisible, inputBackupName } from './backupNameModal';
import { updateBackupList } from './backupList';
import dayjs from 'dayjs';
import { confirmModal, displayErrorMessage } from '../common';

export const backupActionDisabled = ref(false);

export const getDefaultBackupName = () => (
    dayjs().format('YYYY.MM.DD-HH.mm.ss_备份')
);

export const createBackup = async (
    alertSuccess: boolean,
) => {

    if (backupActionDisabled.value) {
        return;
    }
    backupActionDisabled.value = true;

    const submitted = await inputBackupName('新建备份', {
        ...backupNameModalDefaults,
        name: getDefaultBackupName(),
    });
    if (!submitted) { // canceled
        backupActionDisabled.value = false;
        return;
    }

    try {
        const response = await fetch(
            `/api/backup/create/${submitted.name}`,
            { method: 'POST' },
        );
        if (response.status === 200) {
            if (alertSuccess) {
                message.success('新建成功');
            }
            await updateBackupList(false);
        } else {
            await displayErrorMessage(response, '新建备份时出错');
        }
    } catch {
        message.error('新建备份失败');
    }

    backupNameModalPending.value = false;
    backupNameModalVisible.value = false;
    backupActionDisabled.value = false;

};

export const renameBackup = async (
    source: string,
    alertSuccess: boolean,
) => {

    if (backupActionDisabled.value) {
        return;
    }
    backupActionDisabled.value = true;

    const submitted = await inputBackupName('重命名备份', {
        ...backupNameModalDefaults,
        name: source,
    });
    if (!submitted) { // canceled
        backupActionDisabled.value = false;
        return;
    }

    try {
        const response = await fetch(
            `/api/backup/rename/${source}/${submitted.name}`,
            { method: 'POST' },
        );
        if (response.status === 200) {
            if (alertSuccess) {
                message.success('重命名成功');
            }
            await updateBackupList(false);
        } else {
            await displayErrorMessage(response, '重命名备份时出错');
        }
    } catch {
        message.error('重命名备份失败');
    }

    backupNameModalPending.value = false;
    backupNameModalVisible.value = false;
    backupActionDisabled.value = false;

};

export const loadBackup = (
    backupName: string,
    alertSuccess: boolean,
) => {

    if (backupActionDisabled.value) {
        return;
    }
    backupActionDisabled.value = true;

    confirmModal({
        title: `加载备份“${backupName}”`,
        content: h('div', null, [
            '确定要加载此备份吗？',
            h('br'),
            h(TypographyText, { type: 'danger' }, () => (
                '（将会清空当前所有数据！）' // default slot
            )),
        ]),
        async onOk() {
            try {
                const response = await fetch(
                    `/api/backup/load/${backupName}`,
                    { method: 'POST' },
                );
                if (response.status === 200) {
                    if (alertSuccess) {
                        message.success('加载成功');
                    }
                } else {
                    await displayErrorMessage(response, '加载备份时出错');
                }
            } catch {
                message.error('加载备份失败');
            }
            backupActionDisabled.value = false;
        },
        onCancel() {
            backupActionDisabled.value = false;
        },
    });

};

export const deleteBackup = (
    backupName: string,
    alertSuccess: boolean,
) => {

    if (backupActionDisabled.value) {
        return;
    }
    backupActionDisabled.value = true;

    confirmModal({
        title: `删除备份“${backupName}”`,
        content: '确定要删除此条备份吗？',
        async onOk() {
            try {
                const response = await fetch(
                    `/api/backup/delete/${backupName}`,
                    { method: 'POST' },
                );
                if (response.status === 200) {
                    if (alertSuccess) {
                        message.success('删除成功');
                    }
                    await updateBackupList(false);
                } else {
                    await displayErrorMessage(response, '删除备份时出错');
                }
            } catch {
                message.error('删除备份失败');
            }
            backupActionDisabled.value = false;
        },
        onCancel() {
            backupActionDisabled.value = false;
        },
    });

};
