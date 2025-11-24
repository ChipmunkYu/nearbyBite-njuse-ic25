History 模块 API 文档（v1.0）

# 1. 模块概述

History（浏览历史）模块用于记录用户在 “随机推荐页（Recommend.vue）” 中 查看过的餐馆。

触发方式：

只要推荐详情弹窗打开，即认为用户浏览了一次推荐餐馆。

记录内容包括：

哪个用户浏览了

浏览的餐馆名称

浏览时间

该模块用于：

用户行为分析

历史记录页展示

推荐偏好挖掘（未来扩展）

# 2. 数据结构（History Record）
| 字段名           | 类型            | 说明                                |
|------------------|-----------------|-------------------------------------|
| id               | int             | 主键                                 |
| user_id          | string / int    | 浏览的用户 ID                        |
| restaurant_name  | string          | 推荐的餐馆名                         |
| timestamp        | string (ISO8601) | 浏览时间，如：2025-11-06T10:00:00Z   |

返回 JSON 中包含 fields：
```js
{
  "id": 1,
  "user_id": "u001",
  "restaurant_name": "麦当劳",
  "timestamp": "2025-11-06T10:00:00Z"
}
```

# 3. API 列表（统一前缀 /api）
| Method | Path                             | Description              |
|--------|----------------------------------|--------------------------|
| POST   | /api/users/<user_id>/history     | 新增一条历史记录         |
| GET    | /api/users/<user_id>/history     | 获取指定用户的所有历史   |
| DELETE | /api/history/<history_id>        | 删除某一条历史记录       |

# 4. API 详情
## 4.1 创建历史记录
```js
POST /api/users/<user_id>/history
```
请求体：
```js
{
  "restaurant_name": "麦当劳",
  "timestamp": "2025-11-06T10:00:00Z" 
}
```

timestamp 可不传 → 后端自动生成当前时间。

返回示例：
```js
{
  "message": "History record added successfully",
  "data": {
    "id": 12,
    "user_id": "u001",
    "restaurant_name": "麦当劳",
    "timestamp": "2025-11-06T10:00:00Z"
  }
}
```
错误码：
| Code | 情况                               |
|------|------------------------------------|
| 400  | `restaurant_name` 缺失             |
| 401  | token 无效（由 request.js 控制）   |
| 500  | 服务器错误                         |

## 4.2 获取用户历史记录
```js
GET /api/users/<user_id>/history
```

返回该用户按时间倒序排列的全部历史记录。

返回示例：
```js
{
  "data": [
    {
      "id": 5,
      "user_id": "u001",
      "restaurant_name": "海底捞",
      "timestamp": "2025-11-06T12:00:00Z"
    },
    {
      "id": 3,
      "user_id": "u001",
      "restaurant_name": "麦当劳",
      "timestamp": "2025-11-06T10:00:00Z"
    }
  ]
}
```
错误码：
| Code | 情况                 |
|------|----------------------|
| 200  | 成功（即使无记录）   |

## 4.3 删除历史记录
```js
DELETE /api/history/<history_id>
```
返回格式：
```js
{
  "message": "History record deleted successfully"
}
```
错误码：
| Code | 情况           |
|------|----------------|
| 200  | 删除成功       |
| 404  | 该 ID 不存在   |
| 401  | token 无效     |

# 5. Recommend.vue 写入历史的触发机制（关键章节）

历史记录由前端推荐页自动写入，不由用户手动触发。

触发逻辑：

在 Recommend.vue，当用户点击“随机推荐”后：

```js
results.value = [...]
showModal.value = true
```

然后 watch：

```js
watch(showModal, async (visible) => {
  if (visible && results.value.length > 0) {
    await addHistory({
      user_id: currentUser.id,
      restaurant_name: results.value[0].name,
      timestamp: new Date().toISOString()
    })
  }
})
```

即：

当 showModal 从 false → true 且有推荐结果时，向后端写入历史。

# 6. 前端 API 封装（utils/api/history.js）
```js
import request from '@/utils/request'

export const addHistory = (userId, name, timestamp) => {
  return request.post(`/api/users/${userId}/history`, {
    restaurant_name: name,
    timestamp
  })
}

export const getHistory = (userId) => {
  return request.get(`/api/users/${userId}/history`)
}

export const deleteHistory = (id) => {
  return request.delete(`/api/history/${id}`)
}
```

# 7. 权限控制（前端）

History 模块必须在登录状态下使用：

user_id 从 Pinia 的 userStore 获取

request.js 自动在请求头加 token

token 失效 → 自动跳转 login（request.js 内有逻辑）

# 8. 测试覆盖（已通过 pytest）

pytest 覆盖内容：

✔ 创建记录（成功/缺少字段）

✔ timestamp 自动生成

✔ 获取历史（空/多条/排序）

✔ 删除历史（成功/404）

✔ 用户隔离

✔ 全流程：创建 → 查询 → 删除

全部测试通过。

# 9. 后续扩展（未来版本 v2）

未来 History 模块可以扩展：

🔹 记录用户在首页的操作行为

🔹 添加餐馆 ID，支持点击跳转 restaurant detail

🔹 增加批量清空全部历史

🔹 记录用户收藏行为

🔹 增加 GPS 定位、偏好分析

当前版本先保持最小实现。