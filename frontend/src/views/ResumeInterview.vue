<template>
  <div>
    <div class="mb-6">
      <h2 class="text-lg font-medium text-gray-700 mb-4">简历模拟面试</h2>
      <textarea
        v-model="projectDescription"
        placeholder="在这里粘贴简历中的项目描述..."
        class="w-full h-32 p-4 border border-gray-200 rounded-md text-sm resize-none focus:outline-none focus:border-gray-400"
      ></textarea>
      <button 
        @click="generateQuestions"
        :disabled="generating || !projectDescription.trim()"
        class="mt-4 px-6 py-2 bg-gray-700 text-white rounded-md text-sm hover:bg-gray-800 transition-colors disabled:opacity-50"
      >
        {{ generating ? '生成中...' : '生成面试题' }}
      </button>
    </div>

    <div v-if="loading" class="text-center py-8 text-gray-500">
      加载中...
    </div>

    <div v-else-if="questions.length > 0" class="space-y-4">
      <QuestionCard
        v-for="q in questions"
        :key="q.id"
        :question="q"
        @favorite="handleFavorite"
        @delete="handleDelete"
        @regenerate="handleRegenerate"
      />
      
      <div class="mt-6 flex justify-center">
        <button 
          @click="loadFollowup"
          :disabled="loading"
          class="px-6 py-2 border border-gray-300 rounded-md text-sm text-gray-600 hover:bg-gray-100 transition-colors"
        >
          下一批
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { resumeApi } from '../api'
import QuestionCard from '../components/QuestionCard.vue'

const projectDescription = ref('')
const questions = ref([])
const loading = ref(false)
const generating = ref(false)
const resumeId = ref('')

const generateQuestions = async () => {
  generating.value = true
  try {
    const res = await resumeApi.generateQuestions(projectDescription.value)
    questions.value = res.data
    resumeId.value = res.data[0]?.id ? '' : ''
    if (res.data.length > 0) {
      resumeId.value = 'resume_' + Date.now()
    }
  } catch (e) {
    console.error(e)
  }
  generating.value = false
}

const loadFollowup = async () => {
  if (!resumeId.value) {
    resumeId.value = 'resume_' + Date.now()
  }
  loading.value = true
  try {
    const res = await resumeApi.generateFollowup(resumeId.value, projectDescription.value)
    questions.value = [...questions.value, ...res.data]
  } catch (e) {
    console.error(e)
  }
  loading.value = false
}

const handleFavorite = async (id) => {
  try {
    const q = questions.value.find(x => x.id === id)
    if (q) q.is_favorited = 1
  } catch (e) {
    console.error(e)
  }
}

const handleDelete = async (id) => {
  questions.value = questions.value.filter(x => x.id !== id)
}

const handleRegenerate = async (id) => {
  const q = questions.value.find(x => x.id === id)
  if (q) q.answer = '生成的新答案...'
}
</script>