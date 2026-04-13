<template>
  <div class="flex gap-4 mb-6">
    <label
      v-for="cat in categories"
      :key="cat.value"
      class="flex items-center gap-2 cursor-pointer"
    >
      <input
        type="radio"
        :value="cat.value"
        v-model="selected"
        @change="handleChange"
        class="w-4 h-4 text-accent border-gray-300 focus:ring-accent"
      />
      <span class="text-text">{{ cat.label }}</span>
    </label>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'Agent'
  }
})

const emit = defineEmits(['update:modelValue'])

const categories = [
  { label: 'Agent', value: 'Agent' },
  { label: 'RAG', value: 'RAG' },
  { label: 'Memory', value: 'Memory' },
  { label: 'Tool Calling', value: 'Tool Calling' }
]

const selected = ref(props.modelValue)

watch(() => props.modelValue, (val) => {
  selected.value = val
})

function handleChange() {
  emit('update:modelValue', selected.value)
}
</script>
