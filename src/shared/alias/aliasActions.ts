import { message } from 'ant-design-vue';
import { ref } from 'vue';
import { confirmModal, CONTENT_TYPE_JSON, displayErrorMessage } from '../common';

export interface AliasViewResultItem {
    name: string;
    aliases: string[];
}
export type AliasViewResult = AliasViewResultItem[];

export const aliasActionDisabled = ref(false);

export const updateAliasList = async (
    columnName: string,
    listName: string,
    aliases: string[],
    onSuccess?: () => void,
) => {

    if (aliasActionDisabled.value) {
        return;
    }
    aliasActionDisabled.value = true;

    try {
        const url = `/api/alias/update/${columnName}/${listName}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': CONTENT_TYPE_JSON,
            },
            body: JSON.stringify(aliases),
        });
        if (response.status === 200) {
            message.success('更新成功');
            onSuccess?.();
        } else {
            await displayErrorMessage(response, '更新别名时出错');
        }
    } catch {
        message.error('更新别名失败');
    }

    aliasActionDisabled.value = false;

};

export const deleteAliasLists = async (
    columnName: string,
    listNames: string[],
    onSuccess?: () => void,
) => {

    if (aliasActionDisabled.value) {
        return;
    }
    aliasActionDisabled.value = true;

    confirmModal({
        title: `删除别名列表`,
        content: `将要删除别名列表：${listNames.join('、')}。`,
        async onOk() {
            try {
                const url = `/api/alias/delete/${columnName}`;
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'Content-Type': CONTENT_TYPE_JSON,
                    },
                    body: JSON.stringify(listNames),
                });
                if (response.status === 200) {
                    message.success('删除成功');
                    onSuccess?.();
                } else {
                    await displayErrorMessage(response, '删除别名列表时出错');
                }
            } catch {
                message.error('删除别名列表失败');
            }
            aliasActionDisabled.value = false;
        },
        onCancel() {
            aliasActionDisabled.value = false;
        },
    });

};
