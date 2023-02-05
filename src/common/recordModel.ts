import { reactive, ref } from 'vue';
import type { RecordModelState } from './common';

export interface ActivityRecord extends RecordModelState {
    record_id: number;
}

export type RecordModelCallback =
    (submittedRecord: RecordModelState | null) => void;

export const recordModelDefaults: RecordModelState = {
    student_name: '',
    student_school: '',
    student_class: '',
    student_id: '',
    activity_length: 0,
    activity_date: '',
    activity_name: '',
    activity_type: '',
    activity_host: '',
    manager_name: '',
    manager_qq: '',
    notes: '',
};

export const recordModelVisibility = ref(false);
export const recordModelCallback = ref<null | RecordModelCallback>(null);
export const recordModelState = reactive<RecordModelState>(recordModelDefaults);

export const inputRecord = (
    init: RecordModelState,
) => (
    new Promise<RecordModelState | null>((resolve) => {
        for (const key in recordModelState) {
            if (key in init) {
                (recordModelState as any)[key] = (init as any)[key];
            }
        }
        recordModelCallback.value = resolve;
        recordModelVisibility.value = true;
    })
);
