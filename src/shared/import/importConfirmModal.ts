import type { FormInstance } from 'ant-design-vue';
import { reactive, ref } from 'vue';
import type { RecordModalState } from '../common';
import type { ActivityRecord } from '../record/recordModal';
import { TABLE_NAME_PATTERN, validateTableName } from '../table/tableNames';

export interface ImportConfirmModalState {
    allowTableCreation: boolean;
}

export type ConstructedImport = Record<string, ActivityRecord[]>;
export type ImportConfirmModalCallback =
    (submitted: Readonly<ConstructedImport> | null) => void;

export const importConfirmModalDefaults: ImportConfirmModalState = {
    allowTableCreation: true,
};

export const importConfirmModalVisible = ref(false);
export const importConfirmModalCallback =
    ref<null | ImportConfirmModalCallback>(null);
export const importConfirmModalState =
    reactive<ImportConfirmModalState>({ ...importConfirmModalDefaults });
export const importConfirmModalPending = ref(false);
export const importConfirmModalForm = ref<FormInstance>();
export const constructedImport = ref<ConstructedImport | null>(null);

export const guessTableName = (
    record: RecordModalState,
): string => {

    let guess: string;

    const matchResult = record.student_class.trim()
        .match(TABLE_NAME_PATTERN);
    if (matchResult) {
        guess = matchResult[0];
        if (validateTableName(guess)) {
            return guess;
        }
    }

    guess = record.student_id.trim()
        .slice(0, 2);
    if (validateTableName(guess)) {
        return guess;
    }

    throw new Error(
        'Failed to guess the table name.'
        + ` (student_id: ${record.student_id},`
        + ` student_class: ${record.student_class})`
    );

};

export const constructImport = (
    data: ActivityRecord[],
) => {
    const result: ConstructedImport = Object.create(null);
    data.forEach((record) => {
        const tableName = guessTableName(record);
        if (tableName in result) {
            result[tableName].push(record);
        } else {
            result[tableName] = [record];
        }
    });
    return result;
};

export const inputImportConfirm = (
    data: ActivityRecord[],
    init = importConfirmModalDefaults,
) => (
    new Promise<ConstructedImport | null>((resolve) => {

        for (const key in importConfirmModalState) {
            if (key in init) {
                (importConfirmModalState as any)[key] = (init as any)[key];
            }
        }

        constructedImport.value = constructImport(data);
        importConfirmModalForm.value?.clearValidate();
        importConfirmModalCallback.value = resolve;
        importConfirmModalVisible.value = true;

    })
);
