import { message } from 'ant-design-vue';
import { ref } from 'vue';
import { CONTENT_TYPE_JSON } from './common';
import { inputRecord, recordModelDefaults, type ActivityRecord } from './recordModel';

export const tableActionDisabled = ref(false);

export const updateRecord = async (
    tableName: string,
    oldRecord: ActivityRecord,
    onSuccess: () => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    const submittedRecord = await inputRecord(oldRecord);
    if (!submittedRecord) { // canceled
        tableActionDisabled.value = false;
        return;
    }

    const url = `/api/update/${tableName}/${oldRecord.record_id}`;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': CONTENT_TYPE_JSON,
        },
        body: JSON.stringify(submittedRecord),
    });

    if (response.status === 200) {
        onSuccess();
    } else {
        try {
            const errorText = await response.text();
            message.error(errorText);
        } catch {
            message.error('更新数据时出错');
        }
    }

    tableActionDisabled.value = false;

};

export const appendRecord = async (
    tableName: string,
    onSuccess: () => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    const submittedRecord = await inputRecord(recordModelDefaults);
    if (!submittedRecord) { // canceled
        tableActionDisabled.value = false;
        return;
    }

    const url = `/api/append/${tableName}`;
    const response = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': CONTENT_TYPE_JSON,
        },
        body: JSON.stringify(submittedRecord),
    });

    if (response.status === 200) {
        onSuccess();
    } else {
        try {
            const errorText = await response.text();
            message.error(errorText);
        } catch {
            message.error('添加记录时出错');
        }
    }

    tableActionDisabled.value = false;

};

export const deleteRecord = async (
    tableName: string,
    recordId: number,
    onSuccess: () => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }
    tableActionDisabled.value = true;

    // TODO: confirm

    const response = await fetch(`/api/delete/${tableName}/${recordId}`);
    if (response.status === 200) {
        onSuccess();
    } else {
        try {
            const errorText = await response.text();
            message.error(errorText);
        } catch {
            message.error('删除数据时出错');
        }
    }

    tableActionDisabled.value = false;

};

// TODO: append
