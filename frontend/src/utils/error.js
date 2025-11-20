import { ElMessage } from 'element-plus';

export function showError(message) {
    ElMessage.error(message || '网络错误，请稍后重试')
}