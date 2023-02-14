<script setup lang="ts">
defineProps<{
  type?: string,
  size?: string,
  loading?: boolean;
  disabled?: boolean;
  danger?: boolean;
  onClick: () => void;
}>();
</script>

<template>
  <a-button @click="onClick" v-bind="{
    class: 'toolbar-button',
    type,
    loading,
    disabled,
    danger,
  }">
    <template #icon>
      <slot name="icon"></slot>
    </template>
    <slot>?</slot>
  </a-button>
</template>
