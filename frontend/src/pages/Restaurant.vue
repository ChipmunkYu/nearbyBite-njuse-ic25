<template>
  <BackFirstButton/>
  <div class="restaurant-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <div class="title-section">
          <el-icon class="title-icon"><Food /></el-icon>
          <h1 class="title">餐馆管理</h1>
          <el-tag type="success" class="count-tag">
            {{ filteredRestaurants.length }} (●'◡'●)
          </el-tag>
        </div>
        <p class="subtitle">管理您的餐馆数据，支持新增、编辑和删除操作</p>
      </div>
    </div>

    <!-- 操作卡片 -->
    <el-card class="operation-card" shadow="never">
      <div class="toolbar">
        <div class="search-section">
          <el-input
            v-model="search"
            placeholder="搜索餐馆名称、标签或地址..."
            suffix-icon="Search"
            class="search-input"
            clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </div>
        
        <div class="action-buttons">
          <el-button 
            type="primary" 
            @click="openAddDialog"
            class="add-button"
          >
            <el-icon><Plus /></el-icon>
            新增餐馆
          </el-button>
        </div>
      </div>
    </el-card>


    
    <!-- 数据卡片 -->
    <el-card class="data-card" shadow="never">
      <template #header>
        <div class="card-header">
          <span class="card-title">餐馆列表</span>
          <el-button 
            text 
            :loading="loading" 
            @click="loadData"
            class="refresh-btn"
          >
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>

      <!-- 餐馆表格 -->
      <el-table 
        :data="paginatedRestaurants" 
        stripe 
        v-loading="loading"
        class="restaurant-table"
        empty-text="暂无餐馆数据"
      >
        <el-table-column label="餐馆信息" min-width="200">
          <template #default="scope">
            <div class="restaurant-info">
              <div class="name">{{ scope.row.name }}</div>
              <div class="address">
                <el-icon><Location /></el-icon>
                {{ scope.row.address || '暂无地址' }}
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="标签" width="180">
          <template #default="scope">
            <div class="tags-container">
              <el-tag
                v-for="tag in scope.row.tags || []"
                :key="tag"
                type="success"
                size="small"
                class="tag-item"
                effect="light"
              >
                {{ tag }}
              </el-tag>
              <span v-if="!scope.row.tags?.length" class="no-tags">暂无标签</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="人均" width="120" align="center">
          <template #default="scope">
            <div class="price">
              <span class="price-icon">¥</span>
              <span class="price-value">{{ scope.row.avg_price || 0 }}</span>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="评分" width="140" align="center">
          <template #default="scope">
            <div class="rating">
              <el-rate 
                v-model="scope.row.rating" 
                disabled 
                show-score 
                text-color="#ff9900"
                score-template="{value}"
                class="rating-stars"
              />
            </div>
          </template>
        </el-table-column>

        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <el-button 
                type="primary" 
                link 
                @click="openEditDialog(scope.row)"
                class="edit-btn"
              >
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-button 
                type="danger" 
                link 
                @click="deleteRestaurant(scope.row.id)"
                class="delete-btn"
              >
                <el-icon><Delete /></el-icon>
                删除
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页器 -->
<div class="pagination-wrapper">
  <el-pagination
    background
    layout="prev, pager, next"
    :total="filteredRestaurants.length"
    :page-size="pageSize"
    :current-page="currentPage"
    @current-change="handlePageChange"
  />
</div>

    </el-card>

    

    <!-- 新增/编辑弹窗 -->
    <el-dialog 
      v-model="dialogVisible" 
      :title="dialogTitle" 
      width="600px"
      class="restaurant-dialog"
      :close-on-click-modal="false"
    >
      <el-form :model="form" label-width="100px" class="dialog-form">
        <el-form-item label="餐馆名称">
          <el-input 
            v-model="form.name" 
            placeholder="请输入餐馆名称"
            clearable
          />
        </el-form-item>

        <el-form-item label="标签">
          <el-select 
            v-model="form.tags" 
            multiple 
            filterable 
            allow-create
            placeholder="选择或输入标签"
            class="tags-select"
          >
            <el-option 
              v-for="t in allTags" 
              :key="t" 
              :label="t" 
              :value="t" 
            />
          </el-select>
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="人均消费">
              <el-input-number 
                v-model="form.avg_price" 
                :min="0" 
                :max="9999"
                controls-position="right"
                class="price-input"
              >
                <template #prefix>¥</template>
              </el-input-number>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="评分">
              <el-rate 
                v-model="form.rating" 
                allow-half 
                show-text
                text-color="#ff9900"
                class="rating-input"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="地址">
          <el-input 
            v-model="form.address" 
            type="textarea"
            :rows="2"
            placeholder="请输入详细地址"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="submitForm"
            :loading="submitting"
          >
            {{ submitting ? '保存中...' : '保存' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import request from "@/utils/api/request";
import { ElMessage, ElMessageBox } from "element-plus";
import BackFirstButton from '@/components/BackFirstButton.vue'
import {
  Food,
  Search,
  Plus,
  Refresh,
  Location,
  Edit,
  Delete
} from '@element-plus/icons-vue'

const restaurants = ref([]);
const search = ref("");
const loading = ref(false);
const submitting = ref(false);

// 所有可能的标签
const allTags = ["快餐", "奶茶", "火锅", "烧烤", "日料", "西餐", "中餐", "小吃", "甜点", "咖啡"];

const dialogVisible = ref(false);
const dialogTitle = ref("新增餐馆");

const form = ref({
  id: null,
  name: "",
  tags: [],
  avg_price: 0,
  rating: null,
  address: "",
});

// 搜索过滤
const filteredRestaurants = computed(() => {
  if (!search.value) return restaurants.value;
  const keyword = search.value.toLowerCase();
  return restaurants.value.filter(r =>
    r.name.toLowerCase().includes(keyword) ||
    (r.tags?.some(tag => tag.toLowerCase().includes(keyword))) ||
    (r.address && r.address.toLowerCase().includes(keyword))
  );
});

// 打开新增弹窗
const openAddDialog = () => {
  dialogTitle.value = "新增餐馆";
  form.value = { 
    id: null, 
    name: "", 
    tags: [], 
    avg_price: 0, 
    rating: null, 
    address: "" 
  };
  dialogVisible.value = true;
};

// 打开编辑弹窗
const openEditDialog = (row) => {
  dialogTitle.value = "编辑餐馆";
  form.value = { ...row };
  dialogVisible.value = true;
};

// 提交表单
const submitForm = async () => {
  if (!form.value.name.trim()) {
    ElMessage.warning("请输入餐馆名称");
    return;
  }

  submitting.value = true;
  try {
    if (form.value.id) {
      await request.put(`/api/restaurants/${form.value.id}`, form.value);
      ElMessage.success("更新成功");
    } else {
      await request.post("/api/restaurants", form.value);
      ElMessage.success("新增成功");
    }
    dialogVisible.value = false;
    await loadData();
  } catch (err) {
    ElMessage.error("操作失败");
  } finally {
    submitting.value = false;
  }
};

// 删除餐馆
const deleteRestaurant = async (id) => {
  try {
    await ElMessageBox.confirm("确定要删除该餐馆吗？此操作不可恢复。", "警告", {
      type: "warning",
      confirmButtonText: "确定删除",
      cancelButtonText: "取消",
      confirmButtonClass: "el-button--danger"
    });
    
    await request.delete(`/api/restaurants/${id}`);
    ElMessage.success("删除成功");
    await loadData();
  } catch {
    // 用户取消删除
  }

};

  const currentPage = ref(1)
  const pageSize = ref(8)   // 每页展示 8 条，可自由调整

  const paginatedRestaurants = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  return filteredRestaurants.value.slice(start, start + pageSize.value)
})

  function handlePageChange(page) {
    currentPage.value = page
}


// 加载数据
const loadData = async () => {
  loading.value = true;
  try {
    const res = await request.get("/api/restaurants");
    restaurants.value = res.data.data;
  } catch (err) {
    ElMessage.error("加载失败");
  } finally {
    loading.value = false;
  }
};

onMounted(loadData);
</script>

<style scoped>
.restaurant-page {
  padding: 0;
  background: #f5f7fa;
  min-height: 100vh;
}

/* 页面头部 */
.page-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 30px 24px;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
}

.title-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.title-icon {
  font-size: 32px;
}

.title {
  font-size: 28px;
  font-weight: 600;
  margin: 0;
  color: white;
}

.count-tag {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  font-weight: 500;
}

.subtitle {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

/* 操作卡片 */
.operation-card {
  margin: 24px;
  border-radius: 12px;
  border: 1px solid #e4e7ed;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.search-section {
  flex: 1;
  max-width: 400px;
}

.search-input {
  border-radius: 8px;
}

.add-button {
  border-radius: 8px;
  padding: 10px 20px;
}

/* 数据卡片 */
.data-card {
  margin: 0 24px 24px;
  border-radius: 12px;
  border: 1px solid #e4e7ed;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.refresh-btn {
  color: #409eff;
}

/* 表格样式 */
.restaurant-table {
  border-radius: 8px;
}

.restaurant-info .name {
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.restaurant-info .address {
  font-size: 12px;
  color: #909399;
  display: flex;
  align-items: center;
  gap: 4px;
}

.tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  border-radius: 4px;
}

.no-tags {
  color: #c0c4cc;
  font-size: 12px;
}

.price {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 2px;
}

.price-icon {
  color: #ff6b6b;
  font-weight: 500;
}

.price-value {
  font-weight: 600;
  color: #ff6b6b;
}

.rating-stars {
  justify-content: center;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.edit-btn, .delete-btn {
  padding: 4px 8px;
}

/* 弹窗样式 */
.restaurant-dialog {
  border-radius: 12px;
}

.dialog-form {
  padding: 0 20px;
}

.tags-select {
  width: 100%;
}

.price-input, .rating-input {
  width: 100%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 20px 0 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    padding: 20px 16px;
  }
  
  .operation-card,
  .data-card {
    margin: 16px;
  }
  
  .toolbar {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-section {
    max-width: none;
  }

  .pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 24px 0 12px;
}

:deep(.el-pagination.is-background .el-pager li) {
  border-radius: 10px;
  transition: 0.25s;
}

:deep(.el-pagination button),
:deep(.el-pagination li) {
  border-radius: 10px !important;
  background-color: #fff6;
  backdrop-filter: blur(6px);
}

:deep(.el-pagination .el-pager li.is-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  font-weight: bold;
  box-shadow: 0 4px 10px rgba(118, 75, 162, 0.3);
}

}
</style>