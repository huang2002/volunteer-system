import { reactive, ref } from 'vue';

export interface CreateTableModalState {
    name: string;
}

export type CreateTableModalCallback =
    (submitted: Readonly<CreateTableModalState> | null) => void;

export const createTableModalDefaults: CreateTableModalState = {
    name: '',
};

export const createTableModalVisibility = ref(false);
export const createTableModalCallback =
    ref<null | CreateTableModalCallback>(null);
export const createTableModalState =
    reactive<CreateTableModalState>({ ...createTableModalDefaults });
export const createTableModalPending = ref(false);

export const inputTableName = (
    init: CreateTableModalState,
) => (
    new Promise<CreateTableModalState | null>((resolve) => {
        for (const key in createTableModalState) {
            if (key in init) {
                (createTableModalState as any)[key] = (init as any)[key];
            }
        }
        createTableModalCallback.value = resolve;
        createTableModalVisibility.value = true;
    })
);
