import { ref } from 'vue';

export const aliasEditorVisible = ref(false);

export const showAliasEditor = () => {
    aliasEditorVisible.value = true;
};
