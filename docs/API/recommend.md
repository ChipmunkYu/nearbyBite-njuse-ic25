Recommend 模块 API 文档（v1.0）

# 1. 模块概述

Recommend（随机推荐）模块用于在 “吃什么 · 随机推荐页（Recommend.vue）” 中，基于一组筛选条件，为用户随机推荐一家餐馆。

触发方式：

用户在 Recommend.vue 中设置筛选条件（人均、地区、菜系、口味、距离等）

点击“随机推荐”按钮

前端向后端发起请求，从候选餐馆中随机返回 0~1 条记录

筛选条件包括（当前版本）：

人均价格（price_min / price_max）

地区（area）

菜系类型（types）

口味（flavors）

评分下限（min_rating，可选）

距离限制（max_distance_km + lat/lng，可选）

若未提供经纬度，后端会返回一个“伪距离”（假数据），用于前端展示。

该模块用于：

随机帮用户决定“吃什么”

为浏览历史（History 模块）提供数据来源

# 2. 数据结构（Restaurant Record）

实际数据来自数据库，这里给出后端返回的结构约定。

实际数据来自数据库，这里给出后端返回的数据结构约定。

| 字段名         | 类型          | 说明                                         |
|---------------|---------------|----------------------------------------------|
| id            | int           | 餐馆 ID（数据库主键或 mock ID）                |
| name          | string        | 餐馆名称                                      |
| location      | string        | 详细地址 / 商圈描述                            |
| area          | string        | 区域，如：鼓楼 / 仙林 / 新街口                 |
| price         | number        | 人均价格（单位：元）                           |
| rating        | number        | 评分（如 4.2）                                |
| types         | string[]      | 菜系类型数组，如：["火锅","烧烤"]              |
| flavors       | string[]      | 口味数组，如：["麻辣","重口味"]                |
| lat           | number / null | 餐馆纬度（可选，目前可能为空）                  |
| lng           | number / null | 餐馆经度（可选，目前可能为空）                  |
| distance_km   | number / null | 与用户的距离（km），或伪距离                    |

返回 JSON 示例（有推荐结果时，数组长度为 1）：
```js
[
  {
    "id": 1,
    "name": "麦当劳（鼓楼）",
    "location": "广州路",
    "area": "鼓楼",
    "price": 30,
    "rating": 4.2,
    "types": ["快餐"],
    "flavors": ["咸香"],
    "lat": 32.0565,
    "lng": 118.7792,
    "distance_km": 1.3
  }
]
```
无符合条件结果时返回空数组：
```js
[]
```

# 3. API 列表（统一前缀 /api）
| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/recommend/restaurants` | 获取一条随机推荐餐馆记录（Recommend 模块） |

当前版本 Recommend 模块只有一个核心接口，其他行为（如写入历史）由 History 模块负责。

# 4. API 详情

## 4.1 获取随机推荐餐馆
```js
GET /api/recommend/restaurants
```

用于在前端 Recommend.vue 中请求一条随机推荐餐馆。

### 4.1.1 请求参数（Query String）

支持以下筛选参数，全部可选：

| 参数名           | 类型    | 必填 | 默认值 | 说明 |
|------------------|---------|------|--------|------|
| price_min        | number  | 否   | 0      | 人均价格下限 |
| price_max        | number  | 否   | 200    | 人均价格上限 |
| min_rating       | number  | 否   | 无     | 评分下限，如 4.0 |
| area             | string  | 否   | 无     | 区域过滤，如 鼓楼 / 仙林 |
| types            | string  | 否   | 无     | 菜系，逗号分隔，如 火锅,烧烤 |
| flavors          | string  | 否   | 无     | 口味，逗号分隔，如 辣,咸香 |
| max_distance_km  | number  | 否   | 无     | 最大距离（km），需配合 lat/lng 使用 |
| lat              | number  | 否   | 无     | 用户当前纬度 |
| lng              | number  | 否   | 无     | 用户当前经度 |

说明：

如果未提供 lat / lng，后端不会计算真实距离，而是为每条候选餐厅生成一个 0.2–3.5 km 的 伪距离，仅用于前端展示。

推荐逻辑为：先根据筛选条件过滤，再从剩余列表中随机选出 0 或 1 条（满足“最近一次不重复”的约束）。

### 4.1.2 请求示例
```js
GET /api/recommend/restaurants?price_min=20&price_max=60&area=鼓楼&types=快餐,小吃
```

### 4.1.3 返回示例（有推荐结果）
```js
[
  {
    "id": 7,
    "name": "兰州拉面",
    "location": "汉口路",
    "area": "鼓楼",
    "price": 25,
    "rating": 4.0,
    "types": ["小吃"],
    "flavors": ["咸香"],
    "lat": null,
    "lng": null,
    "distance_km": 0.8
  }
]
```
### 4.1.4 返回示例（无符合条件）
```js
[]
```

前端可以根据数组长度是否为 0 来决定显示 “暂无符合条件的餐馆”。

### 4.1.5 错误码
| Code | 情况                                |
| ---- | --------------------------------- |
| 200  | 成功（无论有无推荐结果，都返回 200）              |
| 400  | 参数格式错误（如 `price_min > price_max`） |
| 500  | 服务器内部错误                           |


推荐接口通常不强制登录，但推荐页本身常与用户历史绑定，实际项目中可以按需要添加登录校验。

# 5. Recommend.vue 与推荐接口的交互机制

Recommend.vue 中的交互大致流程如下：

用户设置筛选条件（人均消费、地区、标签、距离等）

点击“随机推荐”按钮

前端调用 getRandomRestaurant(filters) → 访问 /api/recommend/restaurants

将返回的结果展示在弹窗 / 卡片中

弹窗打开时，由 History 模块自动写入浏览历史

## 伪代码示例（Recommend.vue）

```js
// API
import { getRandomRestaurant } from '@/utils/api/recommend'
import { addHistory } from '@/utils/api/history'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const results = ref([])
const showModal = ref(false)

const fetchRandom = async () => {
  const params = {
    price_min: priceRange.value[0],
    price_max: priceRange.value[1],
    area: selectedArea.value || '',
    types: selectedTypes.value.join(','),
    flavors: selectedFlavors.value.join(','),
    max_distance_km: distanceRange.value[1] || null,
    lat: currentLocation.value.lat,
    lng: currentLocation.value.lng
  }

  const res = await getRandomRestaurant(params)
  results.value = res.data || res
  showModal.value = results.value.length > 0
}

watch(showModal, async (visible) => {
  if (visible && results.value.length > 0) {
    await addHistory(
      userStore.id,
      results.value[0].name,
      new Date().toISOString()
    )
  }
})
```

# 6. 前端 API 封装（utils/api/recommend.js）
```js
import request from '@/utils/request'

export const getRandomRestaurant = (params) => {
  return request.get('/api/recommend/restaurants', {
    params
  })
}
```

在组件中使用：

```js
const res = await getRandomRestaurant({
  price_min: 10,
  price_max: 50,
  area: '鼓楼',
  types: '快餐,小吃'
})
```
# 7. 权限控制（前端）

当前版本推荐逻辑建议：

推荐接口本身可允许 未登录访问（用户也能随便“摇一摇吃什么”）。

但如果要写入 History（绑定到具体 user_id），则需要：

从 Pinia 的 userStore 中获取登录用户 ID

request.js 在有 token 时自动加 Authorization 头

token 失效时：History 写入失败 → 由 request.js 统一处理并跳转 login

也就是说：

推荐模块本身：可匿名使用

与用户绑定的行为（如历史记录）：依赖登录状态



# 8. 测试覆盖

Recommend 模块测试覆盖内容建议如下（可以和实际测试保持一致）：

✔ 不带任何筛选条件时，能够返回一条随机餐馆或空数组

✔ 带人均价格筛选时，只返回符合 price_min / price_max 的餐馆

✔ 带地区 / 菜系 / 口味筛选时，过滤逻辑正确

✔ 无符合条件时返回 []，不会报错

✔ 若提供 lat/lng + max_distance_km，返回结果的距离计算逻辑正确（或伪距离生成逻辑符合预期）

✔ 连续多次请求时，不会连续返回完全相同的一家餐馆（如有做“去重上一条推荐”的逻辑）

# 9. 后续扩展（未来版本）

未来 Recommend 模块可以扩展：

🔹 接入真实餐馆数据库（Restaurant 表）而不是 mock 数据

🔹 配合地图组件展示真实地理位置

🔹 支持“避开上一次吃过的店”或“优先推荐没去过的店”

🔹 增加“权重随机”机制（评分高 / 评价多的餐馆被抽中的概率更大）

当前版本先保持：伪距离展示，方便前后端联调与演示。