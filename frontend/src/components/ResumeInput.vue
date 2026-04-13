<template>
  <div class="mb-4">
    <textarea
      v-model="content"
      :placeholder="placeholder"
      class="w-full h-32 p-4 border border-gray-200 rounded-lg text-sm focus:outline-none focus:border-accent resize-none"
    ></textarea>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    default: '在这里粘贴简历中的项目描述...'
  }
})

const emit = defineEmits(['update:modelValue'])

const content = ref(props.modelValue)

watch(content, (newVal) => {
  emit('update:modelValue', newVal)
})
</script>
