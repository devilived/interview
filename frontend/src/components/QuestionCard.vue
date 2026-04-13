<template>
  <div class="bg-card rounded-lg shadow-sm p-5 mb-4 border border-gray-100">
    <div class="mb-3">
      <span class="text-sm text-accent font-medium">Q:</span>
      <p class="text-text mt-1">{{ question }}</p>
    </div>
    <div class="bg-gray-50 rounded-md p-4 mb-3">
      <span class="text-sm text-accent font-medium">A:</span>
      <p class="text-text mt-1 text-sm whitespace-pre-wrap">{{ answer }}</p>
    </div>
    <div class="flex gap-2 justify-end">
      <button
        v-if="showFavorite"
        @click="$emit('favorite')"
        class="px-4 py-1.5 text-sm border border-accent text-accent rounded hover:bg-gray-50 transition"
      >
        收藏
      </button>
      <button
        v-if="showRegenerate"
        @click="$emit('regenerate')"
        class="px-4 py-1.5 text-sm border border-accent-green text-accent-green rounded hover:bg-green-50 transition"
      >
        生成新答案
      </button>
      <button
        v-if="showDelete"
        @click="$emit('delete')"
        class="px-4 py-1.5 text-sm border border-red-400 text-red-400 rounded hover:bg-red-50 transition"
      >
        删除
      </button>
    </div>
  </div>
</template>

<script setup>
defineProps({
  question: {
    type: String,
    required: true
  },
  answer: {
    type: String,
    default: ''
  },
  showFavorite: {
    type: Boolean,
    default: false
  },
  showRegenerate: {
    type: Boolean,
    default: false
  },
  showDelete: {
    type: Boolean,
    default: false
  }
})

defineEmits(['favorite', 'regenerate', 'delete'])
</script>
