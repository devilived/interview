<template>
  <div class="bg-card rounded-lg shadow-sm p-5 mb-4 border border-gray-100">
    <div class="mb-3">
      <span class="text-sm text-accent font-medium">Q:</span>
      <div v-if="!editing">
        <p class="text-text mt-1">{{ question }}</p>
      </div>
      <div v-else class="mt-1">
        <textarea
          v-model="editQuestion"
          class="w-full p-2 border border-gray-200 rounded text-sm"
          rows="2"
        ></textarea>
      </div>
    </div>
    <div class="bg-gray-50 rounded-md p-4 mb-3">
      <span class="text-sm text-accent font-medium">A:</span>
      <div v-if="!editing" class="mt-1 text-sm markdown-body" v-html="renderedAnswer"></div>
      <div v-else class="mt-1">
        <textarea
          v-model="editAnswer"
          class="w-full p-2 border border-gray-200 rounded text-sm"
          rows="6"
        ></textarea>
      </div>
    </div>
    <div class="flex gap-2 justify-end">
      <template v-if="!editing">
        <button
          v-if="showFavorite"
          @click="$emit('favorite')"
          class="px-4 py-1.5 text-sm border border-accent text-accent rounded hover:bg-gray-50 transition"
        >
          收藏
        </button>
        <button
          v-if="showEdit && isFavorited"
          @click="startEdit"
          class="px-4 py-1.5 text-sm border border-blue-400 text-blue-400 rounded hover:bg-blue-50 transition"
        >
          修改
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
      </template>
      <template v-else>
        <button
          @click="saveEdit"
          class="px-4 py-1.5 text-sm bg-accent text-white rounded hover:bg-gray-700 transition"
        >
          保存
        </button>
        <button
          @click="cancelEdit"
          class="px-4 py-1.5 text-sm border border-gray-300 text-gray-600 rounded hover:bg-gray-50 transition"
        >
          取消
        </button>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import MarkdownIt from 'markdown-it'

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true
})

const props = defineProps({
  id: {
    type: Number,
    required: true
  },
  question: {
    type: String,
    required: true
  },
  answer: {
    type: String,
    default: ''
  },
  isFavorited: {
    type: Number,
    default: 0
  },
  showFavorite: {
    type: Boolean,
    default: false
  },
  showEdit: {
    type: Boolean,
    default: true
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

const emit = defineEmits(['favorite', 'regenerate', 'delete', 'update'])

const editing = ref(false)
const editQuestion = ref('')
const editAnswer = ref('')

function startEdit() {
  editQuestion.value = props.question
  editAnswer.value = props.answer
  editing.value = true
}

function cancelEdit() {
  editing.value = false
}

function saveEdit() {
  emit('update', { id: props.id, question: editQuestion.value, answer: editAnswer.value })
  editing.value = false
}

const renderedAnswer = computed(() => {
  return md.render(props.answer || '')
})
</script>

<style>
.markdown-body pre {
  background-color: #0d1117;
  color: #c9d1d9;
  border-radius: 6px;
  padding: 12px;
  margin: 8px 0;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
}

.markdown-body code {
  font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
  background-color: #f6f8fa;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
}

.markdown-body pre code {
  background-color: transparent;
  padding: 0;
}

.markdown-body p {
  margin: 8px 0;
  white-space: pre-line;
}

.markdown-body ul, .markdown-body ol {
  margin: 8px 0;
  padding-left: 24px;
}

.markdown-body li {
  margin: 6px 0;
  line-height: 1.6;
  white-space: pre-line;
}
</style>
