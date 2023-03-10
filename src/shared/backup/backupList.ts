import { ref, shallowRef } from 'vue';
import { message } from 'ant-design-vue';
import { displayErrorMessage } from '../common';
import { isValidTableName } from '../table/tableNames';

export interface BackupItem {
    name: string;
    tables: string[];
}

const isValidBackupList = (list: unknown): list is BackupItem[] => (
    Array.isArray(list)
    && list.every((item) => (
        item
        && (typeof item === 'object')
        && (typeof item.name === 'string')
        && Array.isArray(item.tables)
        && item.tables.every(isValidTableName)
    ))
);

export const backupList = shallowRef<BackupItem[]>([]);
export const loadingBackupNames = ref(false);

export const updateBackupList = async (
    alertSuccess: boolean,
) => {

    if (loadingBackupNames.value) {
        return;
    }
    loadingBackupNames.value = true;

    try {
        const response = await fetch('/api/backup/list');
        if (response.status === 200) {
            const result = await response.json();
            if (isValidBackupList(result)) {
                backupList.value = result;
                if (alertSuccess) {
                    message.success('刷新成功');
                }
            } else {
                message.error('后台返回的备份列表格式有误');
            }
        } else {
            await displayErrorMessage(response, '获取备份列表时出错');
        }
    } catch {
        message.error('更新备份列表失败');
    }

    loadingBackupNames.value = false;

};
