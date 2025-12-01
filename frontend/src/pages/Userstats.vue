<template>
  <div class="stats-container">
    <!-- 背景装饰 -->
    <div class="background">
      <div class="floating-icon">📊</div>
      <div class="floating-icon">📈</div>
      <div class="floating-icon">🍽️</div>
      <div class="floating-icon">💰</div>
      <div class="floating-icon">🏆</div>
      <div class="floating-icon">📅</div>
    </div>

    <!-- 主内容卡片 -->
    <div class="stats-card">
      <!-- 页面标题 -->
      <div class="page-header">
        <div class="title-group">
          <span class="title-icon">📊</span>
          <h1>我的饮食统计</h1>
        </div>
        <p class="page-subtitle">了解您的饮食习惯，发现美食偏好</p>
      </div>

      <!-- 顶部概览卡片 -->
      <div class="overview-cards">
        <el-row :gutter="20">
          <el-col :span="6">
            <div class="stat-card visit-card">
              <div class="card-icon">👣</div>
              <div class="card-content">
                <div class="card-label">总访问次数</div>
                <div class="card-value">{{ data.total_visits || 0 }}</div>
                <div class="card-tip">您的美食探索历程</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card price-card">
              <div class="card-icon">💰</div>
              <div class="card-content">
                <div class="card-label">平均消费</div>
                <div class="card-value">
                  {{ data.avg_price != null ? `¥ ${data.avg_price.toFixed(1)}` : '—' }}
                </div>
                <div class="card-tip">每次用餐平均花费</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card restaurant-card">
              <div class="card-icon">🏪</div>
              <div class="card-content">
                <div class="card-label">光顾餐馆数</div>
                <div class="card-value">{{ data.unique_restaurants || 0 }}</div>
                <div class="card-tip">探索的美食地图</div>
              </div>
            </div>
          </el-col>
          <el-col :span="6">
            <div class="stat-card frequency-card">
              <div class="card-icon">🔄</div>
              <div class="card-content">
                <div class="card-label">平均每家访问</div>
                <div class="card-value">{{ avgPerRestaurant }}</div>
                <div class="card-tip">您的餐厅忠诚度</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 图表区域 -->
      <div class="charts-section">
        <!-- 菜系饼图 + 价位分布 -->
        <el-row :gutter="24" class="chart-row">
          <el-col :span="12">
            <div class="chart-card">
              <div class="chart-header">
                <div class="chart-title">
                  <span class="chart-icon">🥘</span>
                  常吃菜系占比
                </div>
                <div class="chart-subtitle">您的口味偏好分布</div>
              </div>
              <div ref="pieRef" class="chart-box"></div>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="chart-card">
              <div class="chart-header">
                <div class="chart-title">
                  <span class="chart-icon">💵</span>
                  消费区间分布
                </div>
                <div class="chart-subtitle">您的消费水平分布</div>
              </div>
              <div ref="barRef" class="chart-box"></div>
            </div>
          </el-col>
        </el-row>

        <!-- 趋势图 + 热门餐馆 -->
        <el-row :gutter="24" class="chart-row">
          <el-col :span="14">
            <div class="chart-card">
              <div class="chart-header">
                <div class="chart-title">
                  <span class="chart-icon">📈</span>
                  最近 7 天就餐趋势
                </div>
                <div class="chart-subtitle">您的外出就餐频率</div>
              </div>
              <div ref="lineRef" class="chart-box"></div>
            </div>
          </el-col>
          <el-col :span="10">
            <div class="chart-card">
              <div class="chart-header">
                <div class="chart-title">
                  <span class="chart-icon">🏆</span>
                  常去餐馆 TOP 5
                </div>
                <div class="chart-subtitle">您最喜欢的餐厅</div>
              </div>
              <div class="top-restaurants">
                <div 
                  v-for="(restaurant, index) in data.top_restaurants || []" 
                  :key="restaurant.id"
                  class="restaurant-item"
                  :class="`rank-${index + 1}`"
                >
                  <div class="restaurant-rank">
                    <span class="rank-number">{{ index + 1 }}</span>
                    <div class="rank-crown" v-if="index < 3">
                      {{ ['🥇', '🥈', '🥉'][index] }}
                    </div>
                  </div>
                  <div class="restaurant-info">
                    <div class="restaurant-name">{{ restaurant.name }}</div>
                    <div class="restaurant-stats">
                      <span class="stat-item">
                        <span class="stat-icon">🔄</span>
                        访问：{{ restaurant.count }}次
                      </span>
                      <span class="stat-item" v-if="restaurant.avg_price">
                        <span class="stat-icon">💰</span>
                        人均：¥{{ restaurant.avg_price.toFixed(1) }}
                      </span>
                    </div>
                    <div class="restaurant-tags">
                      <span 
                        v-for="tag in restaurant.tags || []" 
                        :key="tag"
                        class="tag"
                      >
                        {{ tag }}
                      </span>
                    </div>
                  </div>
                </div>
                <div v-if="!data.top_restaurants?.length" class="empty-restaurants">
                  <span class="empty-icon">😴</span>
                  <span class="empty-text">暂无餐厅数据</span>
                </div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import request from '@/utils/api/request'
import { ElMessage } from 'element-plus'

const data = ref({
  total_visits: 0,
  avg_price: null,
  unique_restaurants: 0,
  top_cuisines: [],
  cuisine_counts: {},
  price_buckets: {},
  daily_visits: [],
  top_restaurants: []
})

const pieRef = ref(null)
const barRef = ref(null)
const lineRef = ref(null)

const avgPerRestaurant = computed(() => {
  if (!data.value.unique_restaurants || data.value.total_visits === 0) return '—'
  return (data.value.total_visits / data.value.unique_restaurants).toFixed(1)
})

async function loadStats() {
  try {
    const res = await request.get('/api/users/me/stats')
    if (res.data.code !== 200) {
      ElMessage.error('统计数据加载失败')
      return
    }
    data.value = res.data.data
    nextTick(() => {
      drawAllCharts()
    })
  } catch (e) {
    console.error('无法获取统计数据:', e)
    ElMessage.error('无法获取统计数据')
  }
}

function drawAllCharts() {
  drawPie()
  drawBar()
  drawLine()
}

function drawPie() {
  if (!pieRef.value) return
  const chart = echarts.init(pieRef.value)
  const arr = data.value.top_cuisines || []
  const pieData = arr.map(([name, count]) => ({ name, value: count }))

  chart.setOption({
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}次 ({d}%)'
    },
    legend: {
      top: 'bottom',
      textStyle: {
        color: '#666'
      }
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '45%'],
        itemStyle: {
          borderRadius: 8,
          borderColor: '#fff',
          borderWidth: 2
        },
        data: pieData,
        label: {
          color: '#333',
          formatter: '{b}\n{d}%'
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ],
    color: ['#ff6b6b', '#ffa726', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57', '#ff9ff3']
  })
}

function drawBar() {
  if (!barRef.value) return
  const chart = echarts.init(barRef.value)
  const buckets = data.value.price_buckets || {}
  const names = Object.keys(buckets)
  const values = names.map(k => buckets[k])

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>次数：{c}'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: names,
      axisLine: {
        lineStyle: {
          color: '#ccc'
        }
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#ccc'
        }
      }
    },
    series: [
      {
        type: 'bar',
        data: values,
        barWidth: '60%',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#ff6b6b' },
            { offset: 1, color: '#ffa726' }
          ]),
          borderRadius: [6, 6, 0, 0]
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#ff5252' },
              { offset: 1, color: '#ff9800' }
            ])
          }
        }
      }
    ]
  })
}

function drawLine() {
  if (!lineRef.value) return
  const chart = echarts.init(lineRef.value)
  const dv = data.value.daily_visits || []
  const x = dv.map(d => d.date.slice(5)) // 显示 MM-DD
  const y = dv.map(d => d.count)

  chart.setOption({
    tooltip: {
      trigger: 'axis',
      formatter: '{b}<br/>次数：{c}'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: x,
      axisLine: {
        lineStyle: {
          color: '#ccc'
        }
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#ccc'
        }
      }
    },
    series: [
      {
        type: 'line',
        data: y,
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          width: 4,
          color: '#ff6b6b'
        },
        itemStyle: {
          color: '#ff6b6b',
          borderColor: '#fff',
          borderWidth: 2
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(255, 107, 107, 0.6)' },
            { offset: 1, color: 'rgba(255, 167, 38, 0.1)' }
          ])
        }
      }
    ]
  })
}

onMounted(() => {
  loadStats()
  window.addEventListener('resize', () => {
    if (pieRef.value) echarts.getInstanceByDom(pieRef.value)?.resize()
    if (barRef.value) echarts.getInstanceByDom(barRef.value)?.resize()
    if (lineRef.value) echarts.getInstanceByDom(lineRef.value)?.resize()
  })
})
</script>

<style scoped>
.stats-container {
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

.stats-card {
  width: 1200px;
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

/* 概览卡片 */
.overview-cards {
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 20px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  height: 100%;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
}

.visit-card { border-left: 4px solid #ff6b6b; }
.price-card { border-left: 4px solid #ffa726; }
.restaurant-card { border-left: 4px solid #4ecdc4; }
.frequency-card { border-left: 4px solid #45b7d1; }

.card-icon {
  font-size: 40px;
  width: 72px;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 50%;
  flex-shrink: 0;
}

.card-content {
  flex: 1;
}

.card-label {
  font-size: 14px;
  color: #6c757d;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 8px;
}

.card-value {
  font-size: 32px;
  font-weight: 800;
  color: #2c3e50;
  margin-bottom: 4px;
}

.card-tip {
  font-size: 13px;
  color: #adb5bd;
}

/* 图表区域 */
.charts-section {
  margin-top: 20px;
}

.chart-row {
  margin-bottom: 30px;
}

.chart-card {
  background: #f8f9fa;
  border-radius: 20px;
  padding: 24px;
  height: 100%;
  border: 1px solid rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.chart-card:hover {
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.08);
}

.chart-header {
  margin-bottom: 20px;
}

.chart-title {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.chart-icon {
  font-size: 24px;
}

.chart-subtitle {
  font-size: 14px;
  color: #6c757d;
}

.chart-box {
  width: 100%;
  height: 300px;
}

/* 热门餐馆 */
.top-restaurants {
  height: 300px;
  overflow-y: auto;
  padding-right: 10px;
}

.restaurant-item {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: white;
  border-radius: 16px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.restaurant-item:hover {
  transform: translateX(5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
}

.restaurant-item.rank-1 { border-left: 4px solid #ffd700; }
.restaurant-item.rank-2 { border-left: 4px solid #c0c0c0; }
.restaurant-item.rank-3 { border-left: 4px solid #cd7f32; }
.restaurant-item.rank-4 { border-left: 4px solid #4ecdc4; }
.restaurant-item.rank-5 { border-left: 4px solid #45b7d1; }

.restaurant-rank {
  position: relative;
  width: 40px;
  height: 40px;
  flex-shrink: 0;
}

.rank-number {
  position: absolute;
  top: 0;
  left: 0;
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 800;
  z-index: 1;
}

.rank-crown {
  position: absolute;
  top: -10px;
  left: -5px;
  font-size: 24px;
  z-index: 2;
  animation: crownGlow 2s ease-in-out infinite;
}

@keyframes crownGlow {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

.restaurant-info {
  flex: 1;
}

.restaurant-name {
  font-size: 16px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 8px;
}

.restaurant-stats {
  display: flex;
  gap: 16px;
  margin-bottom: 8px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #6c757d;
}

.stat-icon {
  font-size: 14px;
}

.restaurant-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.restaurant-tags .tag {
  background: linear-gradient(135deg, #e9ecef, #dee2e6);
  color: #495057;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 600;
}

.empty-restaurants {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.empty-icon {
  font-size: 48px;
  margin-bottom: 16px;
  opacity: 0.5;
}

.empty-text {
  font-size: 16px;
  color: #adb5bd;
}

/* 滚动条美化 */
.top-restaurants::-webkit-scrollbar {
  width: 6px;
}

.top-restaurants::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.top-restaurants::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  border-radius: 10px;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .stats-card {
    width: 95%;
    padding: 32px 24px;
  }
  
  .overview-cards .el-col {
    margin-bottom: 16px;
  }
  
  .chart-row .el-col {
    margin-bottom: 24px;
  }
}

@media (max-width: 768px) {
  .stats-container {
    padding: 20px 10px;
  }
  
  .stats-card {
    padding: 24px 16px;
    border-radius: 20px;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .title-icon {
    font-size: 36px;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
    padding: 20px;
  }
  
  .card-icon {
    width: 60px;
    height: 60px;
    font-size: 32px;
  }
  
  .card-value {
    font-size: 28px;
  }
  
  .overview-cards .el-col {
    width: 100%;
    margin-bottom: 16px;
  }
  
  .chart-row .el-col {
    width: 100%;
    margin-bottom: 24px;
  }
  
  .chart-box {
    height: 250px;
  }
  
  .restaurant-item {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
  
  .restaurant-stats {
    flex-direction: column;
    gap: 8px;
  }
}
</style>