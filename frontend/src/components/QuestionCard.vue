<template>
  <div class="bg-white rounded-lg border border-gray-200 p-4">
    <div class="flex justify-between items-start mb-2">
      <h3 class="text-sm font-medium text-gray-800">{{ question.question }}</h3>
    </div>
    
    <div class="text-sm text-gray-600 whitespace-pre-wrap mb-3">{{ question.answer }}</div>
    
    <div class="flex gap-2">
      <template v-if="!question.is_favorited || question.is_favorited === 0">
        <button 
          @click="$emit('favorite', question.id)"
          class="px-3 py-1 text-xs border border-gray-300 rounded text-gray-600 hover:bg-gray-50"
        >
          收藏
        </button>
      </template>
      <template v-else>
        <button 
          @click="$emit('regenerate', question.id)"
          class="px-3 py-1 text-xs border border-gray-300 rounded text-gray-600 hover:bg-gray-50"
        >
          生成新答案
        </button>
        <button 
          @click="$emit('delete', question.id)"
          class="px-3 py-1 text-xs border border-gray-300 rounded text-red-500 hover:bg-red-50"
        >
          删除
        </button>
      </template>
    </div>
  </div>
</template>

<script setup>
defineProps({
  question: {
    type: Object,
    required: true
  }
})

defineEmits(['favorite', 'delete', 'regenerate'])
</script>