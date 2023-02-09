import type { FormInstance } from 'ant-design-vue';
import { reactive, ref } from 'vue';
import type { RecordModalState } from '../common';

export interface ActivityRecord extends RecordModalState {
    record_id: number;
}

export type RecordModalCallback =
    (submitted: Readonly<RecordModalState> | null) => void;

export const recordModalStudentDefaults = {
    student_name: '',
    student_school: '',
    student_class: '',
    student_id: '',
    student_contact: '',
};

export const recordModalDefaults: RecordModalState = {
    ...recordModalStudentDefaults,
    activity_length: 0,
    activity_begin: '',
    activity_end: '',
    activity_name: '',
    activity_type: '',
    activity_host: '',
    manager_name: '',
    manager_contact: '',
    manager_qq: '',
    notes: '',
};

export const recordModalVisible = ref(false);
export const recordModalTitle = ref('?');
export const recordModalCallback =
    ref<null | RecordModalCallback>(null);
export const recordModalState =
    reactive<RecordModalState>({ ...recordModalDefaults });
export const recordModalPending = ref(false);
export const recordModalForm = ref<FormInstance>();
export const recordModalBatchMode = ref(true);
export const recordModalBatchModeAvailable = ref(false);

export const inputRecord = (
    title: string,
    init: RecordModalState,
    batchModeAvailable = false,
) => (
    new Promise<RecordModalState | null>((resolve) => {
        for (const key in recordModalState) {
            if (key in init) {
                (recordModalState as any)[key] = (init as any)[key];
            }
        }
        recordModalForm.value?.clearValidate();
        recordModalTitle.value = title;
        recordModalBatchModeAvailable.value = batchModeAvailable;
        recordModalCallback.value = resolve;
        recordModalVisible.value = true;
    })
);

export const finishRecord = () => {

    recordModalPending.value = false;

    if (
        recordModalBatchModeAvailable.value
        && recordModalBatchMode.value
    ) {
        Object.assign(recordModalState, recordModalStudentDefaults);
        recordModalForm.value?.clearValidate();
    } else {
        recordModalVisible.value = false;
    }

};
