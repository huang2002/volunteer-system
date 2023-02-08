<script setup lang="ts">
import { recordActionDisabled } from '@/shared/record/recordActions';

defineProps<{
  title: string;
  color: string;
  onClick: () => void;
}>();
</script>

<template>
  <a-tooltip :title="title" :color="color">
    <a-tag :color="color">
      <a-button @click="onClick" v-bind="{
        type: 'text',
        size: 'small',
        disabled: recordActionDisabled,
        style: {
          color: 'inherit',
        },
      }">
        <template #icon>
          <slot name="icon">?</slot>
        </template>
      </a-button>
    </a-tag>
  </a-tooltip>
</template>

<style scoped>
.ant-tag {
  margin: 0;
  padding: 0;
}
</style>
