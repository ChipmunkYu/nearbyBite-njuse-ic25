<template>
  <BackFirstButton/>
  <div class="history-container">
    <!-- 背景装饰 -->
    <div class="background">
      <div class="floating-icon">📚</div>
      <div class="floating-icon">⏳</div>
      <div class="floating-icon">🍽️</div>
      <div class="floating-icon">🗑️</div>
      <div class="floating-icon">📊</div>
      <div class="floating-icon">🕒</div>
    </div>

    <!-- 主内容卡片 -->
    <div class="history-card">
      <!-- 页面标题 -->
      <div class="page-header">
        <div class="title-group">
          <span class="title-icon">📚</span>
          <h1>浏览历史</h1>
        </div>
        <p class="page-subtitle">记录您探索美食的每一步足迹</p>
        <div class="header-line"></div>
      </div>

      <!-- 操作栏 -->
      <div class="action-bar">
        <div class="action-info">
          <div class="info-icon">📝</div>
          <div class="info-content">
            <h3 class="info-title">历史记录管理</h3>
            <p class="info-desc">管理您的浏览历史，清理不再需要的数据</p>
          </div>
        </div>

        <div class="action-buttons">
          <!-- 新增：时间筛选 -->
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            value-format="YYYY-MM-DD"
            :clearable="true"
            @change="applyFilters"
            style="margin-right: 16px; width: 320px;"
          />
          
          <el-button
            type="danger"
            :disabled="selected.length === 0"
            @click="handleBatchDelete"
            class="batch-delete-btn"
          >
            <span class="btn-icon">🗑️</span>
            <span class="btn-text">批量删除</span>
            <span class="btn-badge" v-if="selected.length > 0">
              {{ selected.length }}
            </span>
          </el-button>
        </div>
      </div>

      <!-- 数据表格 -->
      <div class="table-section">
        <el-table
          :data="paginatedRecords"
          v-loading="loading"
          style="width: 100%;"
          empty-text="暂无浏览历史"
          @selection-change="selected = $event"
          class="styled-table"
          border
        >
          <!-- 多选框 -->
          <el-table-column type="selection" width="60" align="center" />

          <!-- 餐馆名称 -->
          <el-table-column
            label="餐馆名称"
            prop="restaurant_name"
            align="center"
            header-align="center"
            min-width="240"
          >
            <template #default="{ row }">
              <div class="cell restaurant-cell">
                <span class="cell-icon">🍴</span>
                <span class="cell-text">{{ row.restaurant_name }}</span>
              </div>
            </template>
          </el-table-column>

          <!-- 浏览时间 -->
          <el-table-column
            label="浏览时间"
            prop="timestamp"
            align="center"
            header-align="center"
            min-width="260"
          >
            <template #default="{ row }">
              <div class="cell time-cell">
                <span class="cell-icon">🕒</span>
                <span class="cell-text">{{ formatTime(row.timestamp) }}</span>
              </div>
            </template>
          </el-table-column>

          <!-- 操作 -->
          <el-table-column
            label="操作"
            align="center"
            header-align="center"
            width="150"
          >
            <template #default="{ row }">
              <el-button
                type="danger"
                size="small"
                @click="handleDelete(row.id)"
                class="delete-btn"
              >
                🗑️ 删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 新增：分页组件 -->
        <div class="pagination-container" v-if="filteredRecords.length > 0">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :page-sizes="[10, 20, 50, 100]"
            :total="filteredRecords.length"
            layout="total, sizes, prev, pager, next"
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
          />
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="!loading && filteredRecords.length === 0" class="empty-state">
        <div v-if="records.length === 0" class="empty-icon">📖</div>
        <div v-else class="empty-icon">🔍</div>
        <h3 class="empty-title">
          {{ records.length === 0 ? '暂无浏览历史' : '未找到符合条件的记录' }}
        </h3>
        <p class="empty-desc">
          {{ records.length === 0 
            ? '开始使用随机推荐功能，系统将自动记录您的浏览足迹' 
            : '请调整筛选条件查看其他记录' 
          }}
        </p>
        <el-button 
          v-if="records.length === 0" 
          type="primary" 
          class="empty-btn" 
          @click="router.push('/recommend')"
        >
          <span class="btn-icon">🎲</span>
          <span class="btn-text">去随机推荐</span>
        </el-button>
        <el-button 
          v-else 
          type="primary" 
          class="empty-btn" 
          @click="resetFilters"
        >
          <span class="btn-icon">🔄</span>
          <span class="btn-text">重置筛选</span>
        </el-button>
      </div>

      <!-- 底部统计 -->
      <div v-if="records.length > 0" class="footer-stats">
        <div class="stats-card">
          <div class="stats-icon">📊</div>
          <div class="stats-content">
            <div class="stats-label">历史记录统计</div>
            <div class="stats-values">
              <span class="stat-item">
                <span class="stat-value">{{ filteredRecords.length }}</span>
                <span class="stat-label">条记录</span>
              </span>
              <span class="stat-separator">•</span>
              <span class="stat-item">
                <span class="stat-value">{{ selected.length }}</span>
                <span class="stat-label">条选中</span>
              </span>
              <span v-if="dateRange" class="stat-item">
                <span class="stat-separator">•</span>
                <span class="stat-value">{{ pageSize }}</span>
                <span class="stat-label">条/页</span>
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { getHistory, deleteHistory } from '@/utils/api'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { ElMessageBox } from 'element-plus'
import { useRouter } from 'vue-router'
import BackFirstButton  from '@/components/BackFirstButton.vue'

const router = useRouter()
const userStore = useUserStore()
const userId = userStore.user?.id

const records = ref([])
const loading = ref(false)
const selected = ref([])

// 新增：筛选和分页相关
const dateRange = ref(null)
const currentPage = ref(1)
const pageSize = ref(10)

const filteredRecords = computed(() => {
  if (!dateRange.value || dateRange.value.length !== 2) {
    return records.value
  }

  const [startDate, endDate] = dateRange.value
  const start = new Date(startDate + ' 00:00:00')
  const end = new Date(endDate + ' 23:59:59')
  
  return records.value.filter(item => {
    const itemDate = new Date(item.timestamp)
    return itemDate >= start && itemDate <= end
  })
})

const paginatedRecords = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredRecords.value.slice(start, end)
})

function formatTime(isoStr) {
  if (!isoStr) return ''

  const date = new Date(isoStr)
  date.setHours(date.getHours() + 8)

  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  const h = String(date.getHours()).padStart(2, '0')
  const min = String(date.getMinutes()).padStart(2, '0')
  const s = String(date.getSeconds()).padStart(2, '0')

  return `${y}-${m}-${d} ${h}:${min}:${s}`
}

async function fetchHistory() {
  loading.value = true
  try {
    const res = await getHistory(userId)
    records.value = res.data.data
  } catch {
    ElMessage.error("历史记录加载失败")
  } finally {
    loading.value = false
  }
}

function applyFilters() {
  currentPage.value = 1
}

function resetFilters() {
  dateRange.value = null
  currentPage.value = 1
  selected.value = []
}

function handleSizeChange(val) {
  pageSize.value = val
  currentPage.value = 1
}

function handleCurrentChange(val) {
  currentPage.value = val
}

async function handleDelete(id) {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条浏览记录吗？此操作不可恢复',
      '确认删除',
      { 
        type: 'warning',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        confirmButtonClass: 'confirm-danger'
      }
    )
    await deleteHistory(id)
    ElMessage.success("删除成功")
    fetchHistory()
  } catch {
    // 用户点取消时会走这里
  }
}

async function handleBatchDelete() {
  if (selected.value.length === 0) return

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selected.value.length} 条记录吗？此操作不可恢复`,
      '确认批量删除',
      { 
        type: 'warning',
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        confirmButtonClass: 'confirm-danger'
      }
    )

    for (const item of selected.value) {
      await deleteHistory(item.id)
    }

    ElMessage.success(`成功删除 ${selected.value.length} 条记录`)
    selected.value = []
    fetchHistory()
  } catch {
    // 用户点取消则无需处理
  }
}

onMounted(fetchHistory)
</script>

<style scoped>
/* 原有所有样式完全保持不变！ */
/* 我只添加这一个样式用于分页 */
.pagination-container {
  margin-top: 24px;
  display: flex;
  justify-content: center;
}

/* 完全保留你原来的所有样式，从下面这里开始... */
.history-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #f6d365 100%);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite;
  overflow: auto;
  position: relative;
  padding: 40px 20px;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.background {
  position: absolute;
  inset: 0;
}

.floating-icon {
  position: absolute;
  font-size: 42px;
  opacity: 0.2;
  animation: float 8s ease-in-out infinite;
}

.floating-icon:nth-child(1) { top: 10%; left: 10%; animation-delay: 0s; }
.floating-icon:nth-child(2) { top: 20%; right: 15%; animation-delay: 1.5s; }
.floating-icon:nth-child(3) { bottom: 25%; left: 15%; animation-delay: 3s; }
.floating-icon:nth-child(4) { bottom: 15%; right: 10%; animation-delay: 4.5s; }
.floating-icon:nth-child(5) { top: 40%; left: 85%; animation-delay: 6s; }
.floating-icon:nth-child(6) { bottom: 40%; right: 85%; animation-delay: 7.5s; }

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-25px) rotate(15deg); }
}

.history-card {
  width: 1100px;
  max-width: 95%;
  padding: 48px 42px;
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(16px);
  box-shadow: 
    0 25px 50px rgba(0, 0, 0, 0.15),
    inset 0 1px 0 rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 2;
}

/* 页面标题 */
.page-header {
  text-align: center;
  margin-bottom: 40px;
}

.title-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-bottom: 12px;
}

.title-icon {
  font-size: 48px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.page-header h1 {
  font-size: 36px;
  font-weight: 800;
  color: #2c3e50;
  margin: 0;
  background: linear-gradient(135deg, #2c3e50, #4a6572);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.page-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  margin: 0;
  letter-spacing: 0.5px;
}

.header-line {
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #ff6b6b, #ff8e53);
  margin: 20px auto 0;
  border-radius: 2px;
}

/* 操作栏 */
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 32px;
  padding: 24px;
  background: linear-gradient(135deg, #f8f9fa, #f1f3f4);
  border-radius: 20px;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.action-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.info-icon {
  font-size: 36px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
}

.info-title {
  font-size: 20px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.info-desc {
  font-size: 15px;
  color: #6c757d;
  margin: 0;
  line-height: 1.6;
}

.batch-delete-btn {
  height: 56px;
  border-radius: 14px;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  border: none;
  font-size: 16px;
  font-weight: 700;
  padding: 0 32px;
  display: flex;
  align-items: center;
  gap: 10px;
  transition: all 0.3s ease;
  position: relative;
}

.batch-delete-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 25px rgba(231, 76, 60, 0.4);
}

.batch-delete-btn:disabled {
  opacity: 0.6;
  transform: none !important;
  box-shadow: none !important;
}

.btn-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: #ff6b6b;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 表格区域 */
/* 表格整体 */
.styled-table {
  --header-bg: linear-gradient(135deg, #f8f9fa, #f1f3f4);
  --row-hover-bg: #f8f9fa;
  --border-color: #e9ecef;
}

/* 表头对齐统一 */
.styled-table :deep(.el-table__header th),
.styled-table :deep(.el-table__body td) {
  padding: 16px 20px !important;
  font-size: 15px;
}

/* 表头样式 */
.styled-table :deep(.el-table__header th) {
  background: var(--header-bg) !important;
  font-weight: 700;
  color: #2c3e50;
  border-bottom: 2px solid var(--border-color) !important;
}

/* 行悬浮效果 */
.styled-table :deep(.el-table__row:hover) {
  background: var(--row-hover-bg) !important;
  transform: translateY(-2px);
  transition: 0.2s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}

/* 单元格统一布局 */
.cell {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
}

/* 图标 */
.cell-icon {
  font-size: 20px;
}

/* 文本 */
.cell-text {
  font-weight: 500;
  color: #2c3e50;
}

/* 删除按钮 */
.delete-btn {
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
  border: none;
  color: white;
  padding: 6px 14px;
  border-radius: 8px;
  font-weight: 600;
  transition: 0.2s;
}

.delete-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(255, 107, 107, 0.3);
}

.btn-icon {
  margin-right: 6px;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 60px 40px;
}

.empty-icon {
  font-size: 72px;
  margin-bottom: 24px;
  opacity: 0.5;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.empty-title {
  font-size: 24px;
  font-weight: 700;
  color: #6c757d;
  margin-bottom: 16px;
}

.empty-desc {
  font-size: 16px;
  color: #adb5bd;
  margin-bottom: 32px;
  line-height: 1.6;
}

.empty-btn {
  height: 52px;
  border-radius: 14px;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  border: none;
  font-size: 16px;
  font-weight: 700;
  padding: 0 40px;
}

/* 底部统计 */
.footer-stats {
  margin-top: 40px;
}

.stats-card {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 24px;
  background: linear-gradient(135deg, #e9f7fe, #d6f1ff);
  border-radius: 20px;
  border: 1px solid #cce7ff;
}

.stats-icon {
  font-size: 36px;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #3498db, #2980b9);
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
}

.stats-content {
  flex: 1;
}

.stats-label {
  font-size: 15px;
  color: #2c3e50;
  font-weight: 600;
  margin-bottom: 8px;
}

.stats-values {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.stat-value {
  font-size: 24px;
  font-weight: 800;
  color: #2c3e50;
}

.stat-label {
  font-size: 14px;
  color: #6c757d;
}

.stat-separator {
  font-size: 20px;
  color: #adb5bd;
  font-weight: 700;
}

/* 响应式设计 */
@media (max-width: 992px) {
  .action-bar {
    flex-direction: column;
    gap: 20px;
    text-align: center;
  }
  
  .action-info {
    flex-direction: column;
    text-align: center;
  }
  
  .beautiful-table :deep(.el-table__cell) {
    padding: 12px 0;
  }
}

@media (max-width: 768px) {
  .history-container {
    padding: 20px 10px;
  }
  
  .history-card {
    padding: 32px 24px;
    border-radius: 24px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .title-icon {
    font-size: 36px;
  }
  
  .restaurant-cell,
  .time-cell {
    flex-direction: column;
    gap: 8px;
    text-align: center;
  }
  
  .beautiful-table {
    font-size: 14px;
  }
  
  .stats-card {
    flex-direction: column;
    text-align: center;
  }
}
</style>