/**
 * API 封装模块 - 统一处理前后端交互
 */
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 120000
})

export function getQuestions(category, limit = 5) {
  return api.get('/questions', { params: { category, limit } })
}

export function generateQuestions(category, count = 5) {
  return api.post('/questions/generate', { category, count })
}

export function favoriteQuestion(questionId) {
  return api.post(`/questions/${questionId}/favorite`)
}

export function deleteQuestion(questionId) {
  return api.delete(`/questions/${questionId}`)
}

export function regenerateAnswer(questionId, category) {
  return api.put(`/questions/${questionId}/regenerate`, { category })
}

export function updateQuestion(questionId, question, answer) {
  return api.put(`/questions/${questionId}/update`, { question, answer })
}

export function updateResumeQuestion(questionId, question, answer) {
  return api.put(`/resume/${questionId}/update`, { question, answer })
}

export function generateResumeQuestions(projectDescription, count = 3) {
  return api.post('/resume/generate', { project_description: projectDescription, count })
}

export function generateFollowup(resumeId, projectDescription, count = 3) {
  return api.post(`/resume/${resumeId}/followup`, { project_description: projectDescription, count })
}

export function favoriteResumeQuestion(questionId) {
  return api.post(`/resume/${questionId}/favorite`)
}

export function deleteResumeQuestion(questionId) {
  return api.delete(`/resume/${questionId}`)
}

export default api
