/**
 * API 封装模块 - 统一处理前后端交互
 */
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000
})

/**
 * 获取题库问题列表
 * @param {string} category - 问题分类
 * @param {number} limit - 返回数量
 * @returns {Promise} 问题列表
 */
export function getQuestions(category, limit = 5) {
  return api.get('/questions', { params: { category, limit } })
}

/**
 * 生成新问题
 * @param {string} category - 问题分类
 * @param {number} count - 生成数量
 * @returns {Promise} 生成的问题列表
 */
export function generateQuestions(category, count = 5) {
  return api.post('/questions/generate', { category, count })
}

/**
 * 收藏问题
 * @param {number} questionId - 问题ID
 * @returns {Promise} 操作结果
 */
export function favoriteQuestion(questionId) {
  return api.post(`/questions/${questionId}/favorite`)
}

/**
 * 删除问题
 * @param {number} questionId - 问题ID
 * @returns {Promise} 操作结果
 */
export function deleteQuestion(questionId) {
  return api.delete(`/questions/${questionId}`)
}

/**
 * 重新生成答案
 * @param {number} questionId - 问题ID
 * @param {string} category - 问题分类
 * @returns {Promise} 新答案
 */
export function regenerateAnswer(questionId, category) {
  return api.put(`/questions/${questionId}/regenerate`, { category })
}

/**
 * 根据简历生成问题
 * @param {string} projectDescription - 项目描述
 * @param {number} count - 生成数量
 * @returns {Promise} 生成的问题列表
 */
export function generateResumeQuestions(projectDescription, count = 3) {
  return api.post('/resume/generate', { project_description: projectDescription, count })
}

/**
 * 生成追问
 * @param {string} resumeId - 简历ID
 * @param {string} projectDescription - 项目描述
 * @param {number} count - 生成数量
 * @returns {Promise} 生成的问题列表
 */
export function generateFollowup(resumeId, projectDescription, count = 3) {
  return api.post(`/resume/${resumeId}/followup`, { project_description: projectDescription, count })
}

/**
 * 收藏简历问题
 * @param {number} questionId - 问题ID
 * @returns {Promise} 操作结果
 */
export function favoriteResumeQuestion(questionId) {
  return api.post(`/resume/${questionId}/favorite`)
}

/**
 * 删除简历问题
 * @param {number} questionId - 问题ID
 * @returns {Promise} 操作结果
 */
export function deleteResumeQuestion(questionId) {
  return api.delete(`/resume/${questionId}`)
}

export default api
