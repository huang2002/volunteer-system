import { message, Modal } from 'ant-design-vue';
import type { InjectionKey, Ref } from 'vue';

export const CONTENT_TYPE_JSON = 'application/json; charset=utf8';

export const KEY_GET_CONTENT_CONTAINER =
    Symbol('KEY_GET_CONTENT_CONTAINER') as InjectionKey<() => HTMLElement>;
export const KEY_TABLE_MANAGEMENT_MODAL_VISIBLE =
    Symbol('KEY_TABLE_MANAGEMENT_MODAL_VISIBLE') as InjectionKey<Ref<boolean>>;

export const DATE_PATTERN = /^\d{4}\/\d{2}\/\d{2}$/;

export interface RecordModalState {
    student_name: string;
    student_school: string;
    student_class: string;
    student_id: string;
    student_contact: string;
    activity_length: number;
    activity_begin: string;
    activity_end: string;
    activity_name: string;
    activity_type: string;
    activity_host: string;
    manager_name: string;
    manager_contact: string;
    manager_qq: string;
    notes: string;
}

/**
 * Display the error message from response
 * if it is neither empty nor containing "DOCTYPE".
 * Otherwise, display `fallbackMessage`.
 */
export const displayErrorMessage = async (
    response: Response,
    fallbackMessage: string,
) => {
    try {
        const errorMessage = await response.text();
        if (
            errorMessage
            && !errorMessage.toLowerCase().includes('doctype')
        ) {
            Modal.error({
                title: fallbackMessage,
                content: errorMessage,
                closable: true,
                maskClosable: true,
            });
        } else {
            message.error(fallbackMessage);
        }
    } catch {
        message.error(fallbackMessage);
    }
};
