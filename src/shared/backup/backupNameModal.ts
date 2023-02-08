import type { FormInstance } from 'ant-design-vue';
import { reactive, ref } from 'vue';

export interface BackupNameModalState {
    name: string;
}

export type CreateBackupModalCallback =
    (submitted: Readonly<BackupNameModalState> | null) => void;

export const backupNameModalDefaults: BackupNameModalState = {
    name: '',
};

export const backupNameModalVisible = ref(false);
export const backupNameModalCallback =
    ref<null | CreateBackupModalCallback>(null);
export const backupNameModalTitle = ref('?');
export const backupNameModalState =
    reactive<BackupNameModalState>({ ...backupNameModalDefaults });
export const backupNameModalPending = ref(false);
export const backupNameModalForm = ref<FormInstance>();

export const inputBackupName = (
    title: string,
    init: BackupNameModalState,
) => (
    new Promise<BackupNameModalState | null>((resolve) => {
        for (const key in backupNameModalState) {
            if (key in init) {
                (backupNameModalState as any)[key] = (init as any)[key];
            }
        }
        backupNameModalTitle.value = title;
        backupNameModalForm.value?.clearValidate();
        backupNameModalCallback.value = resolve;
        backupNameModalVisible.value = true;
    })
);
