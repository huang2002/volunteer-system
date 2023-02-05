import { ref } from 'vue';

export const tableActionDisabled = ref(false);

export const updateRecord = (
    tableName: string,
    recordId: number,
    onSuccess: () => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }

};

export const deleteRecord = (
    tableName: string,
    recordId: number,
    onSuccess: () => void,
) => {

    if (tableActionDisabled.value) {
        return;
    }

};
