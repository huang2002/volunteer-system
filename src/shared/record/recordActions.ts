import { WarningOutlined } from '@ant-design/icons-vue';
import { message, Modal } from 'ant-design-vue';
import { h, ref } from 'vue';
import { CONTENT_TYPE_JSON, displayErrorMessage, type RecordModalState } from '../common';
import { finishRecord, inputRecord, recordModalPending, type ActivityRecord, type RecordIndex } from './recordModal';

export const recordActionDisabled = ref(false);

export const updateRecord = (
    tableName: string,
    oldRecord: ActivityRecord,
    onSuccess?: () => void,
) => {

    if (recordActionDisabled.value) {
        return;
    }
    recordActionDisabled.value = true;

    inputRecord(
        `修改记录（记录编号：${oldRecord.record_id}）`,
        oldRecord,
        async (submitted) => {

            if (!submitted) { // canceled
                recordActionDisabled.value = false;
                return;
            }

            const url = `/api/update/record/${tableName}/${oldRecord.record_id}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': CONTENT_TYPE_JSON,
                },
                body: JSON.stringify(submitted),
            });

            if (response.status === 200) {
                message.success('修改成功');
                finishRecord();
                onSuccess?.();
            } else {
                recordModalPending.value = false;
                await displayErrorMessage(response, '更新数据时出错');
            }

            recordActionDisabled.value = false;

        },
    );
};

export const appendingRecord = ref(false);

export const appendRecord = async (
    tableName: string,
    init: RecordModalState,
    onSuccess?: () => void,
) => {

    if (
        recordActionDisabled.value
        || appendingRecord.value
    ) {
        return;
    }
    recordActionDisabled.value = true;
    appendingRecord.value = true;

    inputRecord(
        '添加记录',
        init,
        async (submitted) => {

            if (!submitted) { // canceled
                recordActionDisabled.value = false;
                appendingRecord.value = false;
                return;
            }

            const url = `/api/append/table/${tableName}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': CONTENT_TYPE_JSON,
                },
                body: JSON.stringify([submitted]),
            });

            if (response.status === 200) {
                message.success('添加成功');
                finishRecord();
                onSuccess?.();
            } else {
                recordModalPending.value = false;
                await displayErrorMessage(response, '添加记录时出错');
            }

            recordActionDisabled.value = false;
            appendingRecord.value = false;

        },
        true,
    );

};

export const deleteRecord = (
    tableName: string,
    recordId: RecordIndex,
    onSuccess?: () => void,
) => {

    if (recordActionDisabled.value) {
        return;
    }
    recordActionDisabled.value = true;

    Modal.confirm({
        title: `删除记录#${recordId}`,
        content: '确定要删除此条记录吗？',
        icon: h(WarningOutlined, { style: { color: '#F90' } }),
        okButtonProps: { danger: true },
        okText: '确认',
        cancelButtonProps: { type: 'primary' },
        cancelText: '取消',
        autoFocusButton: 'cancel',
        async onOk() {
            const response = await fetch(
                `/api/delete/record/${tableName}/${recordId}`
            );
            if (response.status === 200) {
                message.success('删除成功');
                onSuccess?.();
            } else {
                await displayErrorMessage(response, '删除数据时出错');
            }
            recordActionDisabled.value = false;
        },
        onCancel() {
            recordActionDisabled.value = false;
        },
    });

};
