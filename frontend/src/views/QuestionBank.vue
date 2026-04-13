<template>
  <div>
    <div class="mb-6">
      <h2 class="text-lg font-medium text-gray-700 mb-4">选择分类</h2>
      <div class="flex gap-4">
        <label 
          v-for="cat in categories" 
          :key="cat"
          class="flex items-center gap-2 cursor-pointer"
        >
          <input 
            type="radio" 
            :value="cat" 
            v-model="selectedCategory"
            class="w-4 h-4 text-gray-600 border-gray-300 focus:ring-gray-500"
          >
          <span class="text-sm text-gray-600">{{ cat }}</span>
        </label>
      </div>
    </div>

    <div v-if="loading" class="text-center py-8 text-gray-500">
      加载中...
    </div>

    <div v-else class="space-y-4">
      <QuestionCard
        v-for="q in questions"
        :key="q.id"
        :question="q"
        @favorite="handleFavorite"
        @delete="handleDelete"
        @regenerate="handleRegenerate"
      />
    </div>

    <div v-if="questions.length > 0" class="mt-6 flex justify-center gap-4">
      <button 
        @click="loadQuestions"
        class="px-6 py-2 border border-gray-300 rounded-md text-sm text-gray-600 hover:bg-gray-100 transition-colors"
      >
        下一批
      </button>
      <button 
        @click="generateNewQuestions"
        :disabled="generating"
        class="px-6 py-2 bg-gray-700 text-white rounded-md text-sm hover:bg-gray-800 transition-colors disabled:opacity-50"
      >
        {{ generating ? '生成中...' : '新问题' }}
      </button>
    </div>

    <div v-else class="text-center py-8">
      <p class="text-gray-500 mb-4">暂无问题，请点击"新问题"生成</p>
      <button 
        @click="generateNewQuestions"
        :disabled="generating"
        class="px-6 py-2 bg-gray-700 text-white rounded-md text-sm hover:bg-gray-800 transition-colors disabled:opacity-50"
      >
        {{ generating ? '生成中...' : '生成问题' }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { questionApi } from '../api'
import QuestionCard from '../components/QuestionCard.vue'

const categories = ['Agent', 'RAG', 'Memory', 'Tool Calling']
const selectedCategory = ref('Agent')
const questions = ref([])
const loading = ref(false)
const generating = ref(false)

const loadQuestions = async () => {
  loading.value = true
  try {
    const res = await questionApi.getQuestions(selectedCategory.value)
    questions.value = res.data
  } catch (e) {
    console.error(e)
  }
  loading.value = false
}

const generateNewQuestions = async () => {
  generating.value = true
  try {
    const res = await questionApi.generateQuestions(selectedCategory.value)
    questions.value = res.data
  } catch (e) {
    console.error(e)
  }
  generating.value = false
}

const handleFavorite = async (id) => {
  try {
    await questionApi.favoriteQuestion(id)
    const q = questions.value.find(x => x.id === id)
    if (q) q.is_favorited = 1
  } catch (e) {
    console.error(e)
  }
}

const handleDelete = async (id) => {
  try {
    await questionApi.deleteQuestion(id)
    questions.value = questions.value.filter(x => x.id !== id)
  } catch (e) {
    console.error(e)
  }
}

const handleRegenerate = async (id) => {
  try {
    const res = await questionApi.regenerateAnswer(id)
    const q = questions.value.find(x => x.id === id)
    if (q) q.answer = res.data.answer
  } catch (e) {
    console.error(e)
  }
}

onMounted(() => {
  loadQuestions()
})
</script>