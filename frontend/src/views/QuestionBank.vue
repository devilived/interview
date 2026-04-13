<template>
  <div class="max-w-4xl mx-auto">
    <h2 class="text-lg font-medium text-text mb-4">题库管理</h2>

    <CategorySelector v-model="category" />

    <div v-if="loading" class="text-center py-8 text-accent">加载中...</div>
    <div v-else-if="error" class="text-center py-8 text-red-500">{{ error }}</div>

    <QuestionList
      v-else
      :questions="questions"
      :showFavorite="true"
      :showRegenerate="true"
      :showDelete="true"
      @favorite="handleFavorite"
      @regenerate="handleRegenerate"
      @delete="handleDelete"
    />

    <div class="flex gap-4 justify-center mt-6">
      <button
        @click="loadQuestions"
        class="px-6 py-2 border border-accent text-accent rounded hover:bg-gray-50 transition"
      >
        下一批
      </button>
      <button
        @click="handleGenerate"
        class="px-6 py-2 bg-accent text-white rounded hover:bg-gray-700 transition"
      >
        新问题
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import CategorySelector from '../components/CategorySelector.vue'
import QuestionList from '../components/QuestionList.vue'
import {
  getQuestions,
  generateQuestions,
  favoriteQuestion,
  deleteQuestion,
  regenerateAnswer
} from '../api'

const category = ref('Agent')
const questions = ref([])
const loading = ref(false)
const error = ref('')

async function loadQuestions() {
  loading.value = true
  error.value = ''
  try {
    const res = await getQuestions(category.value, 5)
    questions.value = res.data
  } catch (e) {
    error.value = '加载问题失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleGenerate() {
  loading.value = true
  error.value = ''
  try {
    const res = await generateQuestions(category.value, 5)
    questions.value = res.data
  } catch (e) {
    error.value = '生成问题失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleFavorite(id) {
  try {
    await favoriteQuestion(id)
    const q = questions.value.find(q => q.id === id)
    if (q) q.is_favorited = 1
  } catch (e) {
    console.error(e)
  }
}

async function handleRegenerate(id) {
  try {
    const res = await regenerateAnswer(id, category.value)
    const q = questions.value.find(q => q.id === id)
    if (q) q.answer = res.data.answer
  } catch (e) {
    console.error(e)
  }
}

async function handleDelete(id) {
  try {
    await deleteQuestion(id)
    questions.value = questions.value.filter(q => q.id !== id)
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadQuestions()
})
</script>
