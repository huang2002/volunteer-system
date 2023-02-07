<script setup lang="ts">
const props = defineProps<{
  loading?: boolean;
  disabled?: boolean;
  onClick: () => void;
}>();
</script>

<template>
  <a-button @click="props.onClick" v-bind="{
    class: 'toolbar-button',
    loading: props.loading,
    disabled: props.disabled,
  }">
    <template #icon>
      <slot name="icon"></slot>
    </template>
    <slot>?</slot>
  </a-button>
</template>

<style scoped>
.toolbar-button {
  margin-left: 8px;
}
</style>
