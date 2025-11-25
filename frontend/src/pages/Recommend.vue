<template>
  <div class="recommend-container">
    <!-- 背景浮动图标 -->
    <div class="background">
      <div class="floating-food">🍕</div>
      <div class="floating-food">🍣</div>
      <div class="floating-food">🍔</div>
      <div class="floating-food">☕</div>
    </div>

    <!-- 中间米白色面板 -->
    <div class="recommend-card">
      <div class="card-inner">
        <h1>🍽️ 吃什么 · 推荐页</h1>

        <!-- 定位提示 -->
        <p class="location-status">{{ locationStatus }}</p>

        <!-- 筛选栏 -->
        <div class="filter-bar">

          <!-- 人均消费 -->
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
              <div class="price-display">
                {{ priceRange[0] }} 元 - {{ priceRange[1] }} 元
              </div>
            </div>
          </div>

          <!-- 食物类型 -->
          <div class="filter-group">
            <span class="label-text">食物类型：</span>
            <el-select
              v-model="selectedTypes"
              multiple
              filterable
              clearable
              placeholder="搜索或选择类型"
              style="min-width: 360px"
            >
              <el-option v-for="tag in foodTypes" :key="tag" :label="tag" :value="tag" />
            </el-select>
          </div>

          <!-- 口味风格 -->
          <div class="filter-group">
            <span class="label-text">口味风格：</span>
            <el-select
              v-model="selectedFlavors"
              multiple
              filterable
              clearable
              placeholder="选择口味"
              style="min-width: 360px"
            >
              <el-option v-for="f in flavors" :key="f" :label="f" :value="f" />
            </el-select>
          </div>

          <!-- 评分 -->
          <div class="filter-group">
            <span class="label-text">评分下限：</span>
            <el-select
              v-model="minRating"
              clearable
              placeholder="不限"
              style="min-width: 360px"
            >
              <el-option v-for="opt in ratingOptions" :key="opt.label" :label="opt.label" :value="opt.value" />
            </el-select>
          </div>

          <!-- 地区 -->
          <div class="filter-group">
            <span class="label-text">地区：</span>
            <el-select
              v-model="selectedArea"
              clearable
              placeholder="选择地区"
              style="min-width: 360px"
            >
              <el-option v-for="area in areas" :key="area" :label="area" :value="area" />
            </el-select>
          </div>

          <!-- 最大距离 -->
          <div class="filter-group">
            <span class="label-text">最大距离：</span>
            <div class="slider-box">
              <el-slider
                v-model="maxDistance"
                :min="0"
                :max="10"
                :step="0.5"
                show-tooltip
              />
              <div class="price-display">
                <span v-if="maxDistance === 0">不限距离</span>
                <span v-else>不超过 {{ maxDistance }} km</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 按钮固定在底部 -->
      <div class="button-bar">
        <el-button
          class="big-btn"
          type="primary"
          @click="getRecommendations"
          :loading="loading"
        >
          🎲 随机推荐
        </el-button>
      </div>
    </div>

    <!-- 模态弹窗 -->
    <transition name="fade">
      <div v-if="showModal" class="overlay">
        <div class="modal-card">
          <div v-if="results.length">
            <h2>这顿去这里吃</h2>
            <h3>{{ results[0].name }}</h3>
            <p>📍 地址：{{ results[0].location }}</p>
            <p>📌 地区：{{ results[0].area || "未知" }}</p>
            <p>💰 人均：{{ results[0].price }} 元</p>
            <p>⭐ 评分：{{ results[0].rating ?? "暂无评分" }}</p>
            <p>🚶 距离：{{ results[0].distance_km }} km</p>
            <p v-if="results[0].types?.length">🏷️ 类型：{{ results[0].types.join(" / ") }}</p>
            <p v-if="results[0].flavors?.length">🍴 风格：{{ results[0].flavors.join(" / ") }}</p>
          </div>
          <div v-else>
            <p>🙈 暂无符合条件的推荐，请调整筛选条件再试～</p>
          </div>
          <el-button type="primary" class="close-btn" @click="showModal = false">返回</el-button>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import { ElMessage } from "element-plus";
import request from "@/utils/api/request";
import { useUserStore } from "@/stores/user";
import { addHistory } from "@/utils/api";

const foodTypes = ["快餐", "火锅", "烧烤", "甜品", "奶茶", "小吃", "川菜", "韩餐", "日料", "西餐", "轻食"];
const flavors = ["清淡", "重口味", "辣", "甜", "咸香", "麻辣", "酸爽", "健康轻食"];
const ratingOptions = [
  { label: "不限", value: null },
  { label: "⭐ 4.0 以上", value: 4.0 },
  { label: "⭐ 4.3 以上", value: 4.3 },
  { label: "⭐ 4.5 以上", value: 4.5 },
  { label: "⭐ 4.8 以上", value: 4.8 },
];
const areas = ["鼓楼", "仙林", "新街口"];

const selectedTypes = ref([]);
const selectedFlavors = ref([]);
const priceRange = ref([0, 200]);
const minRating = ref(null);
const selectedArea = ref("");
const maxDistance = ref(0);

const userLat = ref(null);
const userLng = ref(null);
const locationStatus = ref("正在尝试获取当前位置…");

const results = ref([]);
const showModal = ref(false);
const loading = ref(false);
const userStore = useUserStore();

onMounted(() => {
  if (!navigator.geolocation) {
    locationStatus.value = "浏览器不支持定位，将按默认位置推荐（伪距离）";
    return;
  }
  navigator.geolocation.getCurrentPosition(
    pos => {
      userLat.value = pos.coords.latitude;
      userLng.value = pos.coords.longitude;
      locationStatus.value = "已获取当前定位（为伪距离展示）";
    },
    () => {
      locationStatus.value = "无法获取定位，将按默认位置推荐（伪距离）";
    }
  );
});

const getRecommendations = async () => {
  loading.value = true;
  try {
    const [minPrice, maxPrice] = priceRange.value;
    const params = {
      price_min: minPrice,
      price_max: maxPrice,
      types: selectedTypes.value.join(","),
      flavors: selectedFlavors.value.join(","),
      area: selectedArea.value || "",
    };
    if (minRating.value !== null) params.min_rating = minRating.value;

    if (maxDistance.value > 0) params.max_distance_km = maxDistance.value;
    if (userLat.value && userLng.value) {
      params.lat = userLat.value;
      params.lng = userLng.value;
    }

    const resp = await request.get("/api/recommend/restaurants", { params });
    let list = Array.isArray(resp.data) ? resp.data : resp.data.data || [];

    // 给每个餐厅加伪距离
    list = list.map(item => {
      const maxD = maxDistance.value > 0 ? maxDistance.value : 3.5;
      const minD = 0.2;
      const d = Math.random() * (maxD - minD) + minD;
      return { ...item, distance_km: d.toFixed(1) };
    });

    results.value = list;
    if (!list.length) ElMessage.info("无匹配餐厅，放宽筛选试试！");
  } catch (err) {
    ElMessage.error("获取推荐失败，请稍后重试");
    results.value = [];
  } finally {
    loading.value = false;
    showModal.value = true;
  }
};

watch(showModal, async v => {
  if (v && results.value.length) {
    const user = userStore.user;
    const userId = user?.user_id || user?.id || user?.username;
    if (!userId) return;
    try {
      await addHistory(userId, results.value[0].name);
    } catch (_) {}
  }
});
</script>

<style scoped>
/* ===== 背景区域（渐变 + 漂浮食物） ===== */
.recommend-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 40px 0;
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

.background {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.floating-food {
  position: absolute;
  font-size: 36px;
  opacity: 0.25;
  animation: float 6s ease-in-out infinite;
}

.floating-food:nth-child(1) { top: 8%;  left: 12%; animation-delay: 0s;   }
.floating-food:nth-child(2) { top: 18%; right: 15%; animation-delay: 1.8s; }
.floating-food:nth-child(3) { bottom: 25%; left: 20%; animation-delay: 3.2s; }
.floating-food:nth-child(4) { bottom: 10%; right: 8%; animation-delay: 4.6s; }

@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  50%      { transform: translateY(-20px) rotate(8deg); }
}

/* ===== 中间米白色整块界面 ===== */
.recommend-card {
  position: relative;
  width: 80%;
  max-width: 950px;
  background: #fdf7ef; /* 米白 */
  border-radius: 24px;
  padding: 40px 80px 52px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
  z-index: 2;
  overflow: hidden;
}

/* 背景暗纹（淡淡的小食物） */
.recommend-card::before {
  content: "🍣   🍕   🍜   🧋";
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 100px;
  color: rgba(0, 0, 0, 0.03);
  pointer-events: none;
}

.card-inner {
  position: relative;
  z-index: 1;
}

/* ===== 标题 + 状态 ===== */
h1 {
  color: #ff6b6b;
  margin-bottom: 12px;
  font-size: 32px;
  font-weight: 700;
  text-align: center;
}

.location-status {
  font-size: 14px;
  color: #777;
  text-align: center;
  margin-bottom: 24px;
}

/* ===== 筛选区域 ===== */
.filter-bar {
  display: flex;
  flex-direction: column;
  gap: 22px;
  margin-bottom: 24px;
}

.filter-group {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
}

.label-text {
  width: 90px;          /* 统一宽度 */
  min-width: 90px;
  font-size: 16px;
  color: #555;
  font-weight: 500;
  text-align: right;
  white-space: nowrap;  /* 不换行，保持一行 */
}

.slider-box {
  width: 360px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.price-display {
  margin-top: 4px;
  font-size: 14px;
  color: #666;
}

/* ===== 按钮区域 ===== */
.button-bar {
  display: flex;
  justify-content: center;
  margin-top: 16px;  /* 让按钮靠近筛选区域一点 */
}

.big-btn {
  font-size: 24px;
  padding: 20px 90px;
  border-radius: 26px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  border: none;
  color: #fff;
  font-weight: 600;
  box-shadow: 0 8px 26px rgba(255, 107, 107, 0.45);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.big-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 32px rgba(255, 107, 107, 0.6);
}

/* ===== 弹窗遮罩层 ===== */
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

/* ===== 推荐卡片（金光 + 弹出） ===== */
.modal-card {
  position: relative;
  background: #ffffff;
  padding: 38px 50px 30px;
  border-radius: 24px;
  text-align: center;
  max-width: 480px;
  width: 80%;
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.25);

  /* 卡片本身弹出动画 */
  animation: modalPop 0.4s ease-out;
}

/* 卡片的金色发光边框 */
.modal-card::before {
  content: "";
  position: absolute;
  inset: -2px;
  border-radius: inherit;
  border: 2px solid rgba(255, 215, 0, 0.9);
  box-shadow: 0 0 18px rgba(255, 215, 0, 0.9);
  opacity: 0.9;
  pointer-events: none;
  animation: goldPulse 2s ease-in-out infinite;
}

/* 卡片弹出 */
@keyframes modalPop {
  0%   { transform: scale(0.8) translateY(12px); opacity: 0; }
  100% { transform: scale(1)   translateY(0);    opacity: 1; }
}

/* 金光缓慢脉冲 */
@keyframes goldPulse {
  0%   { box-shadow: 0 0 10px rgba(255, 215, 0, 0.6); }
  50%  { box-shadow: 0 0 26px rgba(255, 215, 0, 1);   }
  100% { box-shadow: 0 0 10px rgba(255, 215, 0, 0.6); }
}

/* 关闭按钮 */
.close-btn {
  margin-top: 20px;
  padding: 12px 34px;
  border-radius: 16px;
  background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
  font-size: 18px;
  border: none;
  color: #fff;
}

/* ===== 过渡：fade 名字对应 <transition name="fade"> ===== */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.35s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
