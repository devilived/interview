<template>
  <div>
    <QuestionCard
      v-for="q in questions"
      :key="q.id"
      :question="q.question"
      :answer="q.answer"
      :showFavorite="!q.is_favorited && showFavorite"
      :showRegenerate="q.is_favorited && showRegenerate"
      :showDelete="showDelete"
      @favorite="$emit('favorite', q.id)"
      @regenerate="$emit('regenerate', q.id)"
      @delete="$emit('delete', q.id)"
    />
  </div>
</template>

<script setup>
import QuestionCard from './QuestionCard.vue'

defineProps({
  questions: {
    type: Array,
    default: () => []
  },
  showFavorite: {
    type: Boolean,
    default: true
  },
  showRegenerate: {
    type: Boolean,
    default: true
  },
  showDelete: {
    type: Boolean,
    default: true
  }
})

defineEmits(['favorite', 'regenerate', 'delete'])
</script>
