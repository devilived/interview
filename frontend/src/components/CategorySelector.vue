<template>
  <div class="flex flex-wrap gap-2 mb-6">
    <button
      v-for="cat in categories"
      :key="cat.value"
      @click="handleSelect(cat.value)"
      :class="[
        'px-4 py-2 rounded-full text-sm font-medium transition-all duration-200',
        selected === cat.value
          ? 'bg-accent text-white shadow-md'
          : 'bg-white text-accent border border-gray-200 hover:border-accent hover:bg-gray-50'
      ]"
    >
      {{ cat.label }}
    </button>
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

function handleSelect(value) {
  selected.value = value
  emit('update:modelValue', value)
}
</script>
