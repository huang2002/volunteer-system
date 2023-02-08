import { message } from 'ant-design-vue';
import type { InjectionKey } from 'vue';

export const CONTENT_TYPE_JSON = 'application/json; charset=utf8';

export const KEY_GET_CONTENT_CONTAINER =
    Symbol('KEY_GET_CONTENT_CONTAINER') as InjectionKey<() => HTMLElement>;

export interface RecordModalState {
    student_name: string;
    student_school: string;
    student_class: string;
    student_id: string;
    student_contact: string;
    activity_length: number;
    activity_date: string;
    activity_name: string;
    activity_type: string;
    activity_host: string;
    manager_name: string;
    manager_contact: string;
    manager_qq: string;
    notes: string;
}

export const onRefreshSuccess = () => {
    message.success('刷新成功');
};
