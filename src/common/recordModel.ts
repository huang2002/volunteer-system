import { reactive, ref } from 'vue';

export interface RecordModelState {
    student_name: string;
    student_school: string;
    student_class: string;
    student_id: string;
    activity_length: number;
    activity_date: string;
    activity_name: string;
    activity_type: string;
    activity_host: string;
    manager_name: string;
    manager_qq: string;
    notes: string;
}

export interface ActivityRecord extends RecordModelState {
    record_id: number;
}

export type RecordModelCallback =
    (submittedRecord: RecordModelState | null) => void;

export const recordModelVisibility = ref(false);
export const recordModelCallback = ref<null | RecordModelCallback>(null);
export const recordModelState = reactive<RecordModelState>({
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
});

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
