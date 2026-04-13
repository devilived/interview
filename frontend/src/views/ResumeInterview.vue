<template>
  <div class="max-w-4xl mx-auto">
    <h2 class="text-lg font-medium text-text mb-4">简历模拟面试</h2>

    <ResumeInput v-model="projectDescription" />

    <div class="flex justify-center mb-6">
      <button
        @click="handleGenerate"
        :disabled="!projectDescription || loading"
        class="px-6 py-2 bg-accent text-white rounded hover:bg-gray-700 transition disabled:opacity-50"
      >
        生成面试题
      </button>
    </div>

    <div v-if="loading" class="text-center py-8 text-accent">生成中...</div>
    <div v-else-if="error" class="text-center py-8 text-red-500">{{ error }}</div>

    <QuestionList
      v-else-if="questions.length > 0"
      :questions="questions"
      :showFavorite="true"
      :showRegenerate="false"
      :showDelete="true"
      @favorite="handleFavorite"
      @delete="handleDelete"
      @update="handleUpdate"
    />

    <div v-if="questions.length > 0" class="flex gap-4 justify-center mt-6">
      <button
        @click="handleFollowup"
        class="px-6 py-2 border border-accent text-accent rounded hover:bg-gray-50 transition"
      >
        下一批
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import ResumeInput from '../components/ResumeInput.vue'
import QuestionList from '../components/QuestionList.vue'
import {
  generateResumeQuestions,
  generateFollowup,
  favoriteResumeQuestion,
  deleteResumeQuestion,
  updateResumeQuestion
} from '../api'

const projectDescription = ref('')
const questions = ref([])
const resumeId = ref('')
const loading = ref(false)
const error = ref('')

async function handleGenerate() {
  loading.value = true
  error.value = ''
  try {
    const res = await generateResumeQuestions(projectDescription.value, 3)
    questions.value = res.data
    if (res.data.length > 0) {
      resumeId.value = res.data[0].resume_id || ''
    }
  } catch (e) {
    error.value = '生成问题失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleFollowup() {
  if (!resumeId.value) return
  loading.value = true
  error.value = ''
  try {
    const res = await generateFollowup(resumeId.value, projectDescription.value, 3)
    questions.value = [...questions.value, ...res.data]
  } catch (e) {
    error.value = '生成追问失败'
    console.error(e)
  } finally {
    loading.value = false
  }
}

async function handleFavorite(id) {
  try {
    await favoriteResumeQuestion(id)
    const q = questions.value.find(q => q.id === id)
    if (q) q.is_favorited = 1
  } catch (e) {
    console.error(e)
  }
}

async function handleDelete(id) {
  try {
    await deleteResumeQuestion(id)
    questions.value = questions.value.filter(q => q.id !== id)
  } catch (e) {
    console.error(e)
  }
}

async function handleUpdate({ id, question, answer }) {
  try {
    await updateResumeQuestion(id, question, answer)
    const q = questions.value.find(q => q.id === id)
    if (q) {
      q.question = question
      q.answer = answer
    }
  } catch (e) {
    console.error(e)
  }
}
</script>
