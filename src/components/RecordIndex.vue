<script setup lang="ts">
import type { ActivityRecord } from '@/shared/record/recordModal';
import { CheckOutlined, CopyOutlined, EyeOutlined } from '@ant-design/icons-vue';
import { message } from 'ant-design-vue';
import { computed, ref } from 'vue';

const props = defineProps<{
  value: ActivityRecord['record_id'];
}>();

const hover = ref(false);
const copied = ref(false);
const color = computed(() => (
  hover.value ? (copied.value ? '#1C2' : '#FB0') : '#19F'
));
const text = computed(() => (
  hover.value ? (copied.value ? '复制成功' : '复制编号') : '查看编号'
));

const onClick = () => {
  const data = props.value;
  navigator.clipboard.writeText(data)
    .then(() => {
      copied.value = true;
      message.success('复制成功');
    }, () => {
      message.error('复制失败');
    });
};
</script>

<template>
  <a-tooltip color="blue" :title="value">
    <a-button type="text" size="small" :style="{ color }" v-on="{
      mouseenter: () => {
        copied = false;
        hover = true;
      },
      mouseleave: () => {
        copied = false;
        hover = false;
      },
      click: onClick,
    }">
      <template #icon>
        <CheckOutlined v-if="copied" />
        <CopyOutlined v-else-if="hover" />
        <EyeOutlined v-else />
      </template>
      {{ text }}
    </a-button>
  </a-tooltip>
</template>
