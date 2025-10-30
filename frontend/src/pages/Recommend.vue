<!-- 随机推荐页面 -->
<template>
  <div class="recommend-container">
    <div class="background">
      <div class="floating-food">🍕</div>
      <div class="floating-food">🍣</div>
      <div class="floating-food">🍔</div>
      <div class="floating-food">☕</div>
    </div>

    <div class="recommend-card">
      <h1>🍽️ 吃什么 · 推荐页</h1>

      <div class="filter-bar">
        <div class="filter-group">
          <span class="label-text">人均消费：</span>
          <div class="slider-box">
            <el-slider
              v-model="priceRange"
              range
              :min="0"
              :max="200"
              :step="1"
              show-tooltip
            />
            <div class="price-display">{{ priceRange[0] }} 元 - {{ priceRange[1] }} 元</div>
          </div>
        </div>

        <div class="filter-group">
          <span class="label-text">食物类型：</span>
          <el-select
            v-model="selectedTypes"
            multiple
            filterable
            clearable
            placeholder="搜索或选择类型"
            style="min-width: 300px;"
          >
            <el-option v-for="tag in foodTypes" :key="tag" :label="tag" :value="tag" />
          </el-select>
        </div>

        <div class="filter-group">
          <span class="label-text">口味风格：</span>
          <el-select
            v-model="selectedFlavors"
            multiple
            filterable
            clearable
            placeholder="选择口味"
            style="min-width: 300px;"
          >
            <el-option v-for="f in flavors" :key="f" :label="f" :value="f" />
          </el-select>
        </div>
      </div>

      <div class="button-bar">
        <el-button class="big-btn" type="primary" @click="getRecommendations">
          🎲 随机推荐
        </el-button>
      </div>
    </div>

    <!-- 模态弹窗 -->
    <transition name="fade">
      <div v-if="showModal" class="overlay">
        <div class="modal-card">
          <h2>这顿去这里吃 🍜</h2>
          <div v-if="results.length">
            <h3>{{ results[0].name }}</h3>
            <p>📍 地址：{{ results[0].location }}</p>
            <p>💰 人均：{{ results[0].price }} 元</p>
            <p>🏷️ 类型：{{ results[0].types.join(' / ') }}</p>
            <p>🍴 风格：{{ results[0].flavors.join(' / ') }}</p>
          </div>
          <div v-else>
            <p>🙈 暂无符合条件的推荐，请调整筛选条件再试一次～</p>
          </div>
          <el-button type="primary" class="close-btn" @click="showModal = false">返回筛选</el-button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from "vue";

const foodTypes = ["快餐", "火锅", "烧烤", "甜品", "奶茶", "小吃", "川菜", "韩餐", "日料", "西餐", "轻食"];
const flavors = ["清淡", "重口味", "辣", "甜", "咸香", "麻辣", "酸爽", "健康轻食"];
const selectedTypes = ref([]);
const selectedFlavors = ref([]);
const priceRange = ref([0, 200]);
const results = ref([]);
const showModal = ref(false);

const restaurants = [
  { name: "麦当劳", location: "广州路", price: 30, types: ["快餐"], flavors: ["咸香"] },
  { name: "海底捞", location: "大学城", price: 90, types: ["火锅"], flavors: ["辣"] },
  { name: "烤匠", location: "仙林中心", price: 60, types: ["烧烤"], flavors: ["重口味", "麻辣"] },
  { name: "兰州拉面", location: "汉口路", price: 25, types: ["小吃"], flavors: ["咸香"] },
  { name: "胖哥俩肉蟹煲", location: "新街口", price: 75, types: ["川菜"], flavors: ["麻辣"] },
];

const getRecommendations = () => {
  let filtered = restaurants;
  if (selectedTypes.value.length)
    filtered = filtered.filter(r => selectedTypes.value.some(t => r.types.includes(t)));
  if (selectedFlavors.value.length)
    filtered = filtered.filter(r => selectedFlavors.value.some(f => r.flavors.includes(f)));
  filtered = filtered.filter(r => r.price >= priceRange.value[0] && r.price <= priceRange.value[1]);

  if (!filtered.length) {
    results.value = [];
  } else {
    const randomIndex = Math.floor(Math.random() * filtered.length);
    results.value = [filtered[randomIndex]];
  }
  showModal.value = true;
};
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
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.background { position: absolute; inset: 0; }
.floating-food {
  position: absolute;
  font-size: 36px;
  opacity: 0.25;
  animation: float 6s ease-in-out infinite;
}
.floating-food:nth-child(1) { top: 8%; left: 12%; animation-delay: 0s; }
.floating-food:nth-child(2) { top: 18%; right: 15%; animation-delay: 1.8s; }
.floating-food:nth-child(3) { bottom: 25%; left: 20%; animation-delay: 3.2s; }
.floating-food:nth-child(4) { bottom: 10%; right: 8%; animation-delay: 4.6s; }

@keyframes float {
  0%,100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(10deg); }
}

.recommend-card {
  background: rgba(255, 255, 255, 0.93);
  backdrop-filter: blur(12px);
  padding: 40px 80px;
  border-radius: 24px;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
  z-index: 2;
  text-align: center;
  width: 80%;
  max-width: 950px;
}

h1 {
  color: #ff6b6b;
  margin-bottom: 40px;
  font-size: 36px;
  font-weight: 700;
}

.filter-bar {
  display: flex;
  flex-direction: column;
  gap: 30px;
  margin-bottom: 30px;
}

.filter-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.label-text {
  font-size: 17px;
  color: #555;
  font-weight: 500;
  min-width: 90px;
  text-align: right;
}

.slider-box {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 320px;
}

.price-display {
  margin-top: 6px;
  font-size: 14px;
  color: #666;
}

.button-bar {
  display: flex;
  justify-content: center;
  margin: 35px 0;
}

.big-btn {
  font-size: 26px;
  padding: 26px 90px;
  border-radius: 24px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  border: none;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.45);
  transition: all 0.3s ease;
}
.big-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 12px 30px rgba(255, 107, 107, 0.55);
  background: linear-gradient(135deg, #ff7b7b 0%, #ffb347 100%);
}

/* 模态弹窗部分 */
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(3px);
  z-index: 99;
}
.modal-card {
  background: #fff;
  padding: 40px 60px;
  border-radius: 24px;
  box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
  text-align: center;
  max-width: 500px;
  width: 80%;
  animation: popIn 0.4s ease;
}
@keyframes popIn {
  0% { transform: scale(0.7); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.close-btn {
  margin-top: 20px;
  padding: 12px 36px;
  border-radius: 16px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  font-size: 18px;
  border: none;
}
</style>