import type { FormInstance } from 'ant-design-vue';
import { reactive, ref } from 'vue';

export interface CreateBackupModalState {
    name: string;
}

export type CreateBackupModalCallback =
    (submitted: Readonly<CreateBackupModalState> | null) => void;

export const createBackupModalDefaults: CreateBackupModalState = {
    name: '',
};

export const createBackupModalVisible = ref(false);
export const createBackupModalCallback =
    ref<null | CreateBackupModalCallback>(null);
export const createBackupModalState =
    reactive<CreateBackupModalState>({ ...createBackupModalDefaults });
export const createBackupModalPending = ref(false);
export const createBackupModalForm = ref<FormInstance>();

export const inputBackupName = (
    init: CreateBackupModalState,
) => (
    new Promise<CreateBackupModalState | null>((resolve) => {
        for (const key in createBackupModalState) {
            if (key in init) {
                (createBackupModalState as any)[key] = (init as any)[key];
            }
        }
        createBackupModalForm.value?.clearValidate();
        createBackupModalCallback.value = resolve;
        createBackupModalVisible.value = true;
    })
);
