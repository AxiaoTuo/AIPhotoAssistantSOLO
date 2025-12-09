import request from './index'

/**
 * 上传图片进行AI分析
 * @param {FormData} formData - 包含图片文件和模型参数的FormData对象
 * @returns {Promise} - 分析结果
 */
export function analyzePhoto(formData) {
  return request.post('/photo/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 获取历史记录列表
 * @param {number} page - 页码
 * @param {number} pageSize - 每页数量
 * @returns {Promise} - 历史记录列表
 */
export function getHistory(page = 1, pageSize = 10) {
  return request.get('/photo/history', {
    params: { page, page_size: pageSize }
  })
}

/**
 * 获取分析详情
 * @param {number} photoId - 图片ID
 * @returns {Promise} - 分析详情
 */
export function getPhotoDetail(photoId) {
  return request.get(`/photo/${photoId}`)
}

/**
 * 删除分析记录
 * @param {number} photoId - 图片ID
 * @returns {Promise} - 删除结果
 */
export function deletePhoto(photoId) {
  return request.delete(`/photo/${photoId}`)
}
