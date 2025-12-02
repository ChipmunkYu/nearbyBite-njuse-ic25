<template>
  <div class="history-page">

    <!-- ⭐ 新增：数据概览区 -->
    <div class="overview-container">

      <!-- 📅 时间轴 -->
      <el-card class="overview-card">
        <h3 class="overview-title">📅 浏览时间线</h3>

        <div v-for="(items, date) in groupedByDate" :key="date" class="timeline-group">
          <div class="timeline-date">{{ date }}</div>
          <ul class="timeline-list">
            <li v-for="item in items" :key="item.id" class="timeline-item">
              {{ item.restaurant_name }}（{{ formatTime(item.timestamp) }}）
            </li>
          </ul>
        </div>
      </el-card>

      <!-- 🏆 Top3 -->
      <el-card class="overview-card">
        <h3 class="overview-title">🏆 最常浏览 Top3</h3>
        <div v-if="top3.length">
          <div v-for="(item, idx) in top3" :key="idx" class="top3-item">
            {{ idx + 1 }}. {{ item.name }}（{{ item.count }} 次）
          </div>
        </div>
        <div v-else>暂无数据</div>
      </el-card>

      <!-- 🍰 饼图 -->
      <el-card class="overview-card">
        <h3 class="overview-title">🍰 浏览类型占比</h3>
        <div ref="chartRef" class="chart-box"></div>
      </el-card>

    </div>
    <!-- ⭐ 新增区域结束 -->



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
import { ref, onMounted, computed, watch } from 'vue'
import { getHistory, deleteHistory } from '@/utils/api'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { ElMessageBox } from 'element-plus'

const userStore = useUserStore()
const userId = userStore.user?.id

const records = ref([])
const loading = ref(false)
const selected = ref([])

const chartRef = ref(null)
let chartInstance = null

// 饼图的餐馆 → 类型映射
const restaurantMeta = {
  "麦当劳": { types: ["快餐"] },
  "肯德基": { types: ["快餐"] },
  "海底捞": { types: ["火锅"] },
  "烤匠": { types: ["烧烤"] },
  "兰州拉面": { types: ["小吃"] }
}


// 时间轴：按日期分组
const groupedByDate = computed(() => {
  const map = {}
  records.value.forEach(item => {
    const date = item.timestamp.slice(0, 10)
    if (!map[date]) map[date] = []
    map[date].push(item)
  })
  return map
})

function formatTime(ts) {
  return ts.slice(11, 16)
}


// Top3 统计
const top3 = computed(() => {
  const counts = {}
  records.value.forEach(r => {
    counts[r.restaurant_name] = (counts[r.restaurant_name] || 0) + 1
  })

  return Object.entries(counts)
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 3)
})


// 饼图数据：按类型聚合
function updateChart() {
  if (!chartRef.value) return

  const typeCounts = {}

  records.value.forEach(r => {
    const meta = restaurantMeta[r.restaurant_name]
    if (meta && meta.types) {
      meta.types.forEach(t => {
        typeCounts[t] = (typeCounts[t] || 0) + 1
      })
    }
  })

  const pieData = Object.entries(typeCounts).map(([name, value]) => ({
    name, value
  }))

  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }

  chartInstance.setOption({
    tooltip: { trigger: 'item' },
    series: [
      {
        type: 'pie',
        radius: '70%',
        data: pieData,
        label: { formatter: '{b}: {d}%' }
      }
    ]
  })
}


// 加载、删除、批量删除

async function fetchHistory() {
  loading.value = true
  try {
    const res = await getHistory(userId)
    records.value = res.data.data
  } catch {
    ElMessage.error("历史记录加载失败")
  } finally {
    loading.value = false
    updateChart()   // 饼图实时更新
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
  } catch {}
}

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
  } catch {}
}

onMounted(fetchHistory)

//  records 更新时，重新渲染饼图
watch(records, updateChart)
</script>



<style scoped>
.history-page {
  padding: 20px;
}

/* 三栏概览区 */
.overview-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.overview-card {
  flex: 1;
  padding: 10px;
}

.overview-title {
  font-size: 18px;
  margin-bottom: 10px;
}

/* 时间轴 */
.timeline-group {
  margin-bottom: 12px;
}
.timeline-date {
  font-weight: bold;
  margin-bottom: 4px;
}
.timeline-list {
  margin-left: 10px;
}
.timeline-item {
  font-size: 14px;
  line-height: 20px;
}

/* Top3 */
.top3-item {
  font-size: 15px;
  margin: 4px 0;
}

/* 饼图 */
.chart-box {
  width: 100%;
  height: 220px;
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
