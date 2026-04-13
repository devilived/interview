<template>
  <div class="min-h-screen bg-gray-50">
    <header class="bg-white border-b border-gray-200 px-6 py-4">
      <h1 class="text-xl font-semibold text-gray-800">Agent 面试题系统</h1>
    </header>
    
    <main class="flex">
      <aside class="w-48 bg-white border-r border-gray-200 p-4">
        <nav class="space-y-2">
          <button 
            v-for="tab in tabs" 
            :key="tab.id"
            @click="currentTab = tab.id"
            class="w-full text-left px-4 py-2 rounded-md text-sm transition-colors"
            :class="currentTab === tab.id ? 'bg-gray-100 text-gray-800 font-medium' : 'text-gray-500 hover:text-gray-700'"
          >
            {{ tab.name }}
          </button>
        </nav>
      </aside>
      
      <section class="flex-1 p-6">
        <QuestionBank v-if="currentTab === 'questionBank'" />
        <ResumeInterview v-else-if="currentTab === 'resume'" />
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import QuestionBank from './views/QuestionBank.vue'
import ResumeInterview from './views/ResumeInterview.vue'

const currentTab = ref('questionBank')
const tabs = [
  { id: 'questionBank', name: '题库管理' },
  { id: 'resume', name: '简历面试' }
]
</script>