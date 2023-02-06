import { reactive, ref } from 'vue';
import type { RecordModalState } from './common';

export interface ActivityRecord extends RecordModalState {
    record_id: number;
}

export type RecordModalCallback =
    (submitted: Readonly<RecordModalState> | null) => void;

export const recordModalDefaults: RecordModalState = {
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

export const recordModalVisibility = ref(false);
export const recordModalCallback =
    ref<null | RecordModalCallback>(null);
export const recordModalState =
    reactive<RecordModalState>({ ...recordModalDefaults });
export const recordModalPending = ref(false);

export const inputRecord = (
    init: RecordModalState,
) => (
    new Promise<RecordModalState | null>((resolve) => {
        for (const key in recordModalState) {
            if (key in init) {
                (recordModalState as any)[key] = (init as any)[key];
            }
        }
        recordModalCallback.value = resolve;
        recordModalVisibility.value = true;
    })
);
