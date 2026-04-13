import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

export const questionApi = {
  getQuestions(category, limit = 5) {
    return api.get('/questions', { params: { category, limit } })
  },
  generateQuestions(category, count = 5) {
    return api.post('/questions/generate', { category, count })
  },
  favoriteQuestion(questionId) {
    return api.post(`/questions/${questionId}/favorite`)
  },
  deleteQuestion(questionId) {
    return api.delete(`/questions/${questionId}`)
  },
  regenerateAnswer(questionId, answer) {
    return api.put(`/questions/${questionId}/regenerate`, { answer })
  }
}

export const resumeApi = {
  generateQuestions(projectDescription, count = 3) {
    return api.post('/resume/generate', { project_description: projectDescription, count })
  },
  generateFollowup(resumeId, projectDescription, count = 3) {
    return api.post(`/resume/${resumeId}/followup`, { project_description: projectDescription, count })
  },
  getResumeQuestions(resumeId, limit = 3) {
    return api.get(`/resume/${resumeId}`, { params: { limit } })
  }
}

export default api