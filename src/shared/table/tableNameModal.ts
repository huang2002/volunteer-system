import type { FormInstance } from 'ant-design-vue';
import { reactive, ref } from 'vue';

export interface TableNameModalState {
    name: string;
}

export type TableNameModalCallback =
    (submitted: Readonly<TableNameModalState> | null) => void;

export const tableNameModalDefaults: TableNameModalState = {
    name: '',
};

export const tableNameModalVisible = ref(false);
export const tableNameModalCallback =
    ref<null | TableNameModalCallback>(null);
export const tableNameModalTitle = ref('?');
export const tableNameModalState =
    reactive<TableNameModalState>({ ...tableNameModalDefaults });
export const tableNameModalPending = ref(false);
export const tableNameModalForm = ref<FormInstance>();

export const inputTableName = (
    title: string,
    init: Readonly<TableNameModalState>,
) => (
    new Promise<Readonly<TableNameModalState> | null>((resolve) => {
        for (const key in tableNameModalState) {
            if (key in init) {
                (tableNameModalState as any)[key] = (init as any)[key];
            }
        }
        tableNameModalTitle.value = title;
        tableNameModalForm.value?.clearValidate();
        tableNameModalCallback.value = resolve;
        tableNameModalVisible.value = true;
    })
);
