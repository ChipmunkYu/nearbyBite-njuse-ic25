<template>
  <BackFirstButton/> 
 <div class="recommend-container">
    <!-- 背景装饰 -->
    <div class="background">
      <div class="floating-food">🍕</div>
      <div class="floating-food">🍣</div>
      <div class="floating-food">🍔</div>
      <div class="floating-food">🍜</div>
      <div class="floating-food">🍰</div>
      <div class="floating-food">🍹</div>
    </div>

    <!-- 主卡片 -->
    <div class="recommend-card">
      <!-- 页面标题 -->
      <div class="page-header">
        <h1>🍽️ 吃什么 · 推荐页</h1>
        <p class="page-subtitle">让选择困难症不再烦恼，一键发现美食惊喜</p>
      </div>

      <!-- 筛选区域 -->
      <div class="filter-section">
        <!-- 价格筛选 -->
        <div class="filter-card">
          <div class="filter-title-box">
            <span class="filter-icon">💰</span>
            <span class="filter-label">人均消费</span>
          </div>
          <div class="filter-content">
            <div class="slider-wrapper">
              <el-slider
                v-model="priceRange"
                range
                :min="0"
                :max="500"
                :step="1"
                show-tooltip
                :format-tooltip="(value) => `${value}元`"
                class="beauty-slider"
              />
              <div class="price-range-display">
                <span class="price-value">{{ priceRange[0] }}元</span>
                <span class="range-separator">-</span>
                <span class="price-value">{{ priceRange[1] }}元</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 类型筛选 -->
        <div class="filter-card">
          <div class="filter-title-box">
            <span class="filter-icon">🏷️</span>
            <span class="filter-label">食物类型</span>
          </div>
          <div class="filter-content">
            <el-select
              v-model="selectedTypes"
              multiple
              filterable
              clearable
              placeholder="搜索或选择类型"
              class="beauty-select"
            >
              <el-option v-for="tag in foodTypes" :key="tag" :label="tag" :value="tag" />
            </el-select>
            <div class="selected-tags" v-if="selectedTypes.length > 0">
              <span class="tag-item" v-for="tag in selectedTypes" :key="tag">
                {{ tag }}
              </span>
            </div>
          </div>
        </div>

      <!-- 口味筛选
        <div class="filter-card">
          <div class="filter-title-box">
            <span class="filter-icon">🌶️</span>
            <span class="filter-label">口味风格</span>
          </div>
          <div class="filter-content">
            <el-select
              v-model="selectedFlavors"
              multiple
              filterable
              clearable
              placeholder="选择口味"
              class="beauty-select"
            >
              <el-option v-for="f in flavors" :key="f" :label="f" :value="f" />
            </el-select>
            <div class="selected-tags" v-if="selectedFlavors.length > 0">
              <span class="tag-item flavor-tag" v-for="tag in selectedFlavors" :key="tag">
                {{ tag }}
              </span>
            </div>
          </div>
        </div> -->
      </div>

      <!-- 推荐按钮 -->
      <div class="action-section">
        <el-button class="big-btn" type="primary" @click="getRecommendations">
          🎲 随机推荐
        </el-button>
        <div class="restaurant-count" v-if="restaurants.length">
          当前共有 <span class="count-number">{{ restaurants.length }}</span> 家餐馆待选
        </div>
      </div>
    </div>

    <!-- 模态弹窗 -->
    <transition name="fade">
      <div v-if="showModal" class="overlay">
        <div class="modal-card">
          <div class="modal-header">
            <h2>这顿去这里吃 🍜</h2>
            <div class="modal-subtitle">系统为您随机推荐</div>
          </div>

          <div class="modal-content">
            <div v-if="results.length" class="result-content">
              <!-- 餐厅名称 -->
              <div class="restaurant-name-box">
                <h3>{{ results[0].name }}</h3>
                <div class="restaurant-badge">⭐ 今日推荐</div>
              </div>

              <!-- 餐厅信息 -->
              <div class="restaurant-info-grid">
                <div class="info-item">
                  <div class="info-icon">📍</div>
                  <div class="info-content">
                    <div class="info-label">地址</div>
                    <div class="info-value">{{ results[0].location }}</div>
                  </div>
                </div>

                <div class="info-item">
                  <div class="info-icon">💰</div>
                  <div class="info-content">
                    <div class="info-label">人均</div>
                    <div class="info-value">{{ results[0].price }}元</div>
                  </div>
                </div>

                <div class="info-item">
                  <div class="info-icon">🏷️</div>
                  <div class="info-content">
                    <div class="info-label">类型</div>
                    <div class="info-value">
                      <span v-for="type in results[0].types" :key="type" class="type-tag">
                        {{ type }}
                      </span>
                    </div>
                  </div>
                </div>

                <div class="info-item">
                  <div class="info-icon">🍴</div>
                  <div class="info-content">
                    <div class="info-label">风格</div>
                    <div class="info-value">
                      <span v-for="flavor in results[0].flavors" :key="flavor" class="flavor-tag">
                        {{ flavor }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 推荐语 -->
              <div class="recommend-tip">
                <span class="tip-icon">💡</span>
                <span class="tip-text">这家店看起来不错，快去尝尝吧！</span>
              </div>
            </div>

            <div v-else class="empty-result">
              <div class="empty-icon">😔</div>
              <h3>没有找到合适的餐馆</h3>
              <p>请调整筛选条件再试一次～</p>
            </div>
          </div>

          <div class="modal-footer">
            <el-button type="primary" class="close-btn" @click="showModal = false">
              返回筛选
            </el-button>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { useUserStore } from '@/stores/user'
import { addHistory } from '@/utils/api/history'
import request from "@/utils/api/request";
import BackFirstButton from '@/components/BackFirstButton.vue'
const foodTypes = ["快餐", "火锅", "烧烤", "甜品", "奶茶", "小吃", "川菜", "韩餐", "日料", "西餐", "轻食","中餐"];
const flavors = ["清淡", "重口味", "辣", "甜", "咸香", "麻辣", "酸爽", "健康轻食"];

const selectedTypes = ref([]);
const selectedFlavors = ref([]);
const priceRange = ref([0, 500]);
const results = ref([]);
const showModal = ref(false);
const userStore = useUserStore();
const restaurants = ref([]);

onMounted(async () => {
  const res = await request.get("/api/restaurants");
  restaurants.value = res.data.data;  
});

const getRecommendations = async () => {
  try {
    const params = {
      price_min: priceRange.value[0],
      price_max: priceRange.value[1],
      types: selectedTypes.value.join(","),
      // flavors: selectedFlavors.value.join(","),  // 你后端取消了 flavors
    };

    const res = await request.get("/api/recommend/restaurants", { params });

    if (!res.data || res.data.length === 0) {
      results.value = [];
    } else {
      const r = res.data[0];
      results.value = [
        {
          id: r.id,
          name: r.name,
          location: r.location || "暂无地址",
          price: r.price,
          types: r.types || [],
          flavors: r.flavors || [], // 你这里可留可删
        }
      ];
    }

    showModal.value = true;
  } catch (err) {
    console.error("推荐接口失败：", err);
  }
};


watch(showModal, async (visible) => {
  if (visible === true && results.value.length > 0) {
    const restaurantName = results.value[0].name;
    const userId = userStore.user?.id;
    const restaurantId = results.value[0].id;
    
    if (!userId) {
      console.warn("未登录，不记录历史记录");
      return;
    }

    try {
      await addHistory(userId, restaurantName, restaurantId);
      console.log("历史记录已写入：", restaurantName);
    } catch (err) {
      console.error("写入历史失败：", err);
    }
  }
});
</script>

<style scoped>
.recommend-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #f6d365 100%);
  background-size: 400% 400%;
  animation: gradientShift 8s ease infinite;
  position: relative;
  overflow: hidden;
  font-family: "Microsoft Yahei", sans-serif;
  padding: 20px;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.background { 
  position: absolute; 
  inset: 0; 
}

.floating-food {
  position: absolute;
  font-size: 42px;
  opacity: 0.25;
  animation: float 6s ease-in-out infinite;
}

.floating-food:nth-child(1) { top: 8%; left: 12%; animation-delay: 0s; }
.floating-food:nth-child(2) { top: 18%; right: 15%; animation-delay: 1.8s; }
.floating-food:nth-child(3) { bottom: 25%; left: 20%; animation-delay: 3.2s; }
.floating-food:nth-child(4) { top: 40%; right: 8%; animation-delay: 4.6s; }
.floating-food:nth-child(5) { bottom: 15%; right: 25%; animation-delay: 2.4s; }
.floating-food:nth-child(6) { top: 60%; left: 5%; animation-delay: 1.2s; }

@keyframes float {
  0%,100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

.recommend-card {
  background: rgba(255, 255, 255, 0.93);
  backdrop-filter: blur(12px);
  padding: 50px 60px;
  border-radius: 28px;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.1);
  z-index: 2;
  text-align: center;
  width: 85%;
  max-width: 1000px;
  position: relative;
  overflow: hidden;
}

.recommend-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, #ff6b6b, #ffa726, #ff6b6b);
  background-size: 200% 100%;
  animation: shimmer 3s linear infinite;
}

@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

/* 页面标题 */
.page-header {
  margin-bottom: 40px;
}

.page-header h1 {
  color: #ff6b6b;
  margin-bottom: 10px;
  font-size: 38px;
  font-weight: 800;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  color: #666;
  font-size: 16px;
  margin: 0;
  letter-spacing: 0.5px;
}

/* 筛选区域 */
.filter-section {
  display: flex;
  flex-direction: column;
  gap: 25px;
  margin-bottom: 30px;
}

.filter-card {
  display: flex;
  align-items: flex-start;
  gap: 24px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 20px;
  border: 1px solid rgba(255, 107, 107, 0.1);
  box-shadow: 0 8px 20px rgba(255, 107, 107, 0.08);
  transition: all 0.3s ease;
}

.filter-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 25px rgba(255, 107, 107, 0.12);
}

.filter-title-box {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 110px;
}

.filter-icon {
  font-size: 24px;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  border-radius: 50%;
  color: white;
}

.filter-label {
  font-size: 17px;
  color: #555;
  font-weight: 600;
  white-space: nowrap;
}

.filter-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 滑块样式 */
.slider-wrapper {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.beauty-slider :deep(.el-slider__runway) {
  height: 8px;
  background: linear-gradient(90deg, #ffe0e0, #ffd8a8);
  border-radius: 4px;
}

.beauty-slider :deep(.el-slider__bar) {
  height: 8px;
  background: linear-gradient(90deg, #ff6b6b, #ffa726);
  border-radius: 4px;
}

.beauty-slider :deep(.el-slider__button) {
  width: 24px;
  height: 24px;
  border: 3px solid white;
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  box-shadow: 
    0 4px 12px rgba(255, 107, 107, 0.3),
    0 0 0 2px rgba(255, 107, 107, 0.1);
  transition: all 0.2s ease;
}

.beauty-slider :deep(.el-slider__button:hover) {
  transform: scale(1.15);
  box-shadow: 
    0 6px 16px rgba(255, 107, 107, 0.4),
    0 0 0 2px rgba(255, 107, 107, 0.2);
}

.price-range-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 14px 24px;
  background: linear-gradient(135deg, #fff5f5, #fff0e0);
  border-radius: 16px;
  border: 1px solid rgba(255, 107, 107, 0.2);
}

.price-value {
  font-size: 22px;
  font-weight: 700;
  color: #ff6b6b;
  font-family: 'Courier New', monospace;
  padding: 6px 16px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(255, 107, 107, 0.1);
}

.range-separator {
  font-size: 24px;
  font-weight: 600;
  color: #ffa726;
}

/* 选择器样式 */
.beauty-select :deep(.el-select__wrapper) {
  border-radius: 14px;
  border: 2px solid #ffe0e0;
  padding: 12px 20px;
  transition: all 0.3s ease;
  background: white;
  min-height: 50px;
}

.beauty-select:hover :deep(.el-select__wrapper) {
  border-color: #ff6b6b;
  box-shadow: 0 0 0 4px rgba(255, 107, 107, 0.1);
}

.beauty-select :deep(.el-tag) {
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  color: white;
  border: none;
  border-radius: 20px;
  padding: 8px 16px;
  font-weight: 600;
  margin-right: 8px;
  margin-bottom: 6px;
}

.selected-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}

.tag-item {
  background: linear-gradient(135deg, #6a11cb, #2575fc);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.flavor-tag {
  background: linear-gradient(135deg, #ff6b6b, #ff8e53);
}

/* 按钮区域 */
.action-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 25px;
  margin-top: 30px;
}

.big-btn {
  font-size: 28px;
  padding: 28px 100px;
  border-radius: 28px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  border: none;
  color: white;
  font-weight: 700;
  letter-spacing: 1px;
  box-shadow: 
    0 12px 30px rgba(255, 107, 107, 0.45),
    0 0 0 3px rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.big-btn:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 
    0 18px 40px rgba(255, 107, 107, 0.6),
    0 0 0 3px rgba(255, 255, 255, 0.3);
}

.big-btn:active {
  transform: translateY(-2px) scale(1.02);
}

.big-btn::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: 0.5s;
}

.big-btn:hover::after {
  left: 100%;
}

.restaurant-count {
  font-size: 16px;
  color: #666;
  padding: 12px 24px;
  background: white;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.count-number {
  font-size: 20px;
  font-weight: 700;
  color: #ff6b6b;
  margin: 0 4px;
}

/* 模态弹窗 */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(4px);
  z-index: 1000;
  padding: 20px;
}

.modal-card {
  background: white;
  padding: 40px;
  border-radius: 28px;
  box-shadow: 
    0 20px 40px rgba(255, 107, 107, 0.3),
    0 0 0 1px rgba(255, 107, 107, 0.1);
  text-align: center;
  max-width: 600px;
  width: 90%;
  animation: popIn 0.4s ease;
  position: relative;
  overflow: hidden;
}

.modal-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, #ff6b6b, #ffa726);
}

@keyframes popIn {
  0% { 
    opacity: 0;
    transform: scale(0.7) translateY(20px);
  }
  100% { 
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}

.modal-header {
  margin-bottom: 30px;
}

.modal-header h2 {
  color: #ff6b6b;
  margin-bottom: 8px;
  font-size: 32px;
  font-weight: 800;
}

.modal-subtitle {
  color: #888;
  font-size: 15px;
  margin: 0;
}

.modal-content {
  margin-bottom: 30px;
}

/* 结果内容 */
.result-content {
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.restaurant-name-box {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.restaurant-name-box h3 {
  font-size: 28px;
  font-weight: 700;
  color: #333;
  margin: 0;
  line-height: 1.2;
}

.restaurant-badge {
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: 700;
  white-space: nowrap;
}

.restaurant-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 25px;
}

.info-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  padding: 16px;
  background: #f9f9f9;
  border-radius: 16px;
  text-align: left;
  transition: all 0.3s ease;
}

.info-item:hover {
  background: #f0f0f0;
  transform: translateY(-2px);
}

.info-icon {
  font-size: 24px;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #ff6b6b, #ffa726);
  border-radius: 50%;
  color: white;
  flex-shrink: 0;
}

.info-content {
  flex: 1;
}

.info-label {
  font-size: 13px;
  color: #888;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 6px;
}

.info-value {
  font-size: 16px;
  color: #333;
  font-weight: 600;
  line-height: 1.4;
}

.type-tag, .flavor-tag {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 16px;
  font-size: 13px;
  font-weight: 600;
  margin-right: 8px;
  margin-bottom: 6px;
}

.type-tag {
  background: #e9ecef;
  color: #495057;
}

.flavor-tag {
  background: #fff3cd;
  color: #856404;
}

.recommend-tip {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 18px;
  background: linear-gradient(135deg, #e9f7fe, #d6f1ff);
  border-radius: 16px;
  border-left: 4px solid #3498db;
}

.tip-icon {
  font-size: 22px;
}

.tip-text {
  font-size: 15px;
  color: #2c3e50;
  font-weight: 600;
}

/* 空状态 */
.empty-result {
  padding: 40px 20px;
}

.empty-icon {
  font-size: 64px;
  margin-bottom: 20px;
  animation: bounce 2s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.empty-result h3 {
  font-size: 24px;
  color: #666;
  margin-bottom: 12px;
}

.empty-result p {
  color: #888;
  font-size: 16px;
  margin: 0;
}

/* 模态框底部 */
.modal-footer {
  display: flex;
  justify-content: center;
}

.close-btn {
  font-size: 18px;
  padding: 14px 40px;
  border-radius: 20px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  border: none;
  color: white;
  font-weight: 600;
  transition: all 0.3s ease;
  min-width: 200px;
}

.close-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3);
}

/* 过渡动画 */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .recommend-card {
    padding: 30px 20px;
    width: 95%;
  }
  
  .page-header h1 {
    font-size: 28px;
  }
  
  .filter-card {
    flex-direction: column;
    gap: 16px;
  }
  
  .filter-title-box {
    min-width: auto;
    justify-content: center;
  }
  
  .big-btn {
    font-size: 22px;
    padding: 22px 40px;
    width: 100%;
  }
  
  .restaurant-info-grid {
    grid-template-columns: 1fr;
  }
  
  .modal-card {
    padding: 30px 20px;
  }
  
  .restaurant-name-box {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
</style>