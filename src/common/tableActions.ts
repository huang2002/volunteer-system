import { message } from 'ant-design-vue';
import { ref } from 'vue';
import { inputRecord, type ActivityRecord } from './recordModel';

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
