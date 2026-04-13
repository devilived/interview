<template>
  <div class="min-h-screen bg-background">
    <Header />

    <div class="flex">
      <aside class="w-48 bg-white border-r border-gray-100 min-h-screen p-4">
        <nav class="space-y-2">
          <button
            @click="currentView = 'questionBank'"
            :class="[
              'w-full text-left px-4 py-2 rounded transition',
              currentView === 'questionBank'
                ? 'bg-gray-100 text-text font-medium'
                : 'text-accent hover:bg-gray-50'
            ]"
          >
            题库管理
          </button>
          <button
            @click="currentView = 'resumeInterview'"
            :class="[
              'w-full text-left px-4 py-2 rounded transition',
              currentView === 'resumeInterview'
                ? 'bg-gray-100 text-text font-medium'
                : 'text-accent hover:bg-gray-50'
            ]"
          >
            简历面试
          </button>
        </nav>
      </aside>

      <main class="flex-1 p-6">
        <QuestionBank v-if="currentView === 'questionBank'" />
        <ResumeInterview v-else-if="currentView === 'resumeInterview'" />
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Header from './components/Header.vue'
import QuestionBank from './views/QuestionBank.vue'
import ResumeInterview from './views/ResumeInterview.vue'

const currentView = ref('questionBank')
</script>
