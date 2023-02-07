<script setup lang="ts">
import { recordActionDisabled } from '@/common/record/recordActionsActions';

const props = defineProps<{
  title: string;
  color: string;
  onClick: () => void;
}>();
</script>

<template>
  <a-tooltip :title="props.title" :color="props.color">
    <a-tag :color="props.color">
      <a-button @click="props.onClick" v-bind="{
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
