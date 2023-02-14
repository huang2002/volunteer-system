import { message, type FormInstance } from 'ant-design-vue';
import { reactive, ref, shallowRef } from 'vue';
import type { RecordModalState } from '../common';
import type { ActivityRecord } from '../record/recordModal';

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
export const constructedImport = shallowRef<ConstructedImport | null>(null);

export const SCHOOL_SEARCH_PATTERN = /(?<!年)[^-_a-zA-Z\d]+学院/;
export const GRADE_SEARCH_PATTERN = /\d{2}/;
export const guessTableName = (
    record: Readonly<RecordModalState>,
): string => {

    const school = record.student_school.trim();

    let matchResult: RegExpMatchArray | null = null;

    let grade: string | null = null;
    matchResult = record.student_class.trim().match(GRADE_SEARCH_PATTERN);
    if (matchResult) {
        grade = matchResult[0];
    } else {
        matchResult = record.student_id.trim().match(GRADE_SEARCH_PATTERN);
        if (matchResult) {
            grade = matchResult[0];
        }
    }
    if (!grade) {
        throw `年级识别失败（学号：${record.student_id}，班级：${record.student_class}）`;
    }

    return `${school}${grade}级`;

};

export const constructImport = (
    data: Readonly<ActivityRecord>[],
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
    data: Readonly<ActivityRecord>[],
    init = importConfirmModalDefaults,
) => (
    new Promise<Readonly<ConstructedImport> | null>((resolve) => {

        for (const key in importConfirmModalState) {
            if (key in init) {
                (importConfirmModalState as any)[key] = (init as any)[key];
            }
        }

        try {
            constructedImport.value = constructImport(data);
        } catch (error) {
            if (typeof error === 'string') {
                message.error(error);
            } else {
                message.error('处理导入数据时出错');
            }
            resolve(null);
            return;
        }
        importConfirmModalForm.value?.clearValidate();
        importConfirmModalCallback.value = resolve;
        importConfirmModalVisible.value = true;

    })
);
