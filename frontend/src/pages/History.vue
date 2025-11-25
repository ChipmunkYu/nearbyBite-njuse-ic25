<template>
  <div class="history-page">
    <div class="header-row">
      <h2>浏览历史</h2>

      <!-- 批量删除按钮 -->
      <el-button
        type="danger"
        :disabled="selected.length === 0"
        @click="handleBatchDelete"
      >
        批量删除
      </el-button>
    </div>

    <el-table
      :data="records"
      v-loading="loading"
      style="width: 100%; margin-top: 20px;"
      empty-text="暂无浏览历史"
      @selection-change="selected = $event"
    >
      <!-- 多选框列 -->
      <el-table-column type="selection" width="55" />

      <el-table-column prop="restaurant_name" label="餐馆名称" width="240" />
      <el-table-column prop="timestamp" label="浏览时间" width="260" />

      <el-table-column label="操作" width="120">
        <template #default="scope">
          <el-button
            type="danger"
            size="small"
            @click="handleDelete(scope.row.id)"
          >
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getHistory, deleteHistory } from '@/utils/api'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const userId = userStore.user?.id

const records = ref([])
const loading = ref(false)

// ⭐ 新增：记录多选框选中的行
const selected = ref([])

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

async function handleDelete(id) {
  try {
    await ElMessageBox.confirm(
      '确定要删除这条浏览记录吗？',
      '确认删除',
      { type: 'warning' }
    )
    await deleteHistory(id)
    ElMessage.success("删除成功")
    fetchHistory()
  } catch {
    // 用户点取消时会走这里，但不需要报错
  }
}

// 批量删除
async function handleBatchDelete() {
  if (selected.value.length === 0) return

  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selected.value.length} 条记录吗？`,
      '确认批量删除',
      { type: 'warning' }
    )

    for (const item of selected.value) {
      await deleteHistory(item.id)
    }

    ElMessage.success("批量删除成功")
    selected.value = []
    fetchHistory()
  } catch {
    // 用户点取消则无需处理
  }
}

onMounted(fetchHistory)
</script>

<style scoped>
.history-page {
  padding: 20px;
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

h2 {
  font-size: 24px;
  margin-bottom: 20px;
}
</style>
