import { message, Modal, TypographyText } from 'ant-design-vue';
import { h, ref } from 'vue';
import { backupNameModalDefaults, backupNameModalPending, backupNameModalVisible, inputBackupName, type BackupNameModalState } from './backupNameModal';
import { updateBackupNames } from './backupList';
import dayjs from 'dayjs';
import { WarningOutlined } from '@ant-design/icons-vue';
import { displayErrorMessage } from '../common';

export const backupActionDisabled = ref(false);

export const getDefaultBackupName = () => (
    dayjs().format('YYYY.MM.DD-HH.mm.ss_备份')
);

export const createBackup = async (
    onSuccess?: (newBackupName: BackupNameModalState) => void,
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

    const response = await fetch(
        `/api/backup/create/${submitted.name}`
    );
    if (response.status === 200) {
        message.success('新建备份成功');
        await updateBackupNames();
        onSuccess?.(submitted);
    } else {
        await displayErrorMessage(response, '新建备份时出错');
    }

    backupNameModalPending.value = false;
    backupNameModalVisible.value = false;
    backupActionDisabled.value = false;

};

export const renameBackup = async (
    source: string,
    onSuccess?: (destination: BackupNameModalState) => void,
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

    const response = await fetch(
        `/api/backup/rename/${source}/${submitted.name}`
    );
    if (response.status === 200) {
        message.success('重命名备份成功');
        await updateBackupNames();
        onSuccess?.(submitted);
    } else {
        await displayErrorMessage(response, '重命名备份时出错');
    }

    backupNameModalPending.value = false;
    backupNameModalVisible.value = false;
    backupActionDisabled.value = false;

};

export const loadBackup = (
    backupName: string,
    onSuccess?: () => void,
) => {

    if (backupActionDisabled.value) {
        return;
    }
    backupActionDisabled.value = true;

    Modal.confirm({
        title: `加载备份“${backupName}”`,
        content: h('div', null, [
            '确定要加载此备份吗？',
            h('br'),
            h(TypographyText, { type: 'danger' }, () => (
                '（将会清空当前所有数据！）' // default slot
            )),
        ]),
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
                `/api/backup/load/${backupName}`
            );
            if (response.status === 200) {
                message.success('加载成功');
                await updateBackupNames();
                onSuccess?.();
            } else {
                await displayErrorMessage(response, '加载备份时出错');
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
    onSuccess?: () => void,
) => {

    if (backupActionDisabled.value) {
        return;
    }
    backupActionDisabled.value = true;

    Modal.confirm({
        title: `删除备份“${backupName}”`,
        content: '确定要删除此条备份吗？',
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
                `/api/backup/delete/${backupName}`
            );
            if (response.status === 200) {
                message.success('删除成功');
                await updateBackupNames();
                onSuccess?.();
            } else {
                await displayErrorMessage(response, '删除备份时出错');
            }
            backupActionDisabled.value = false;
        },
        onCancel() {
            backupActionDisabled.value = false;
        },
    });

};
