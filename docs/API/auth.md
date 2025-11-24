# Auth 模块 API 文档

> 本文档为占位版本  
> Auth 模块接口已在后端实现，但文档部分待补充。  
> 将在开发者提供关键信息后，由文档负责人统一补写。

---

# 1. 模块概述（待补充）

Auth（身份认证）模块用于：

- 用户注册  
- 用户登录（支持 username / user_id）  
- Token 生成与刷新  
- 保护需要登录访问的接口  

详细内容将在后续版本补写。

---

# 2. 数据结构（待补充）

预计包含：

- User Record（user_id / username / created_at / password_hash）  
- Token 结构（access_token / refresh_token）

---

# 3. API 列表（占位）

| Method | Path                  | Description |
|--------|-----------------------|-------------|
| POST   | /api/auth/register    | 用户注册（待补全文档） |
| POST   | /api/auth/login       | 用户登录（待补全文档） |
| POST   | /api/refresh          | 刷新 access_token（待补全文档） |

---

# 4. API 详情（待补充）

每个接口的：

- 请求参数（Body / Query）  
- 返回 JSON 示例  
- 错误码  
- 特殊逻辑  

将在后续版本由文档负责人统一补写。

---

# 5. 前端 API 封装（待补充）

格式示例：

```js
import request from '@/utils/request'

// 登录
export const login = (identifier, password) => {
  return request.post('/api/auth/login', { identifier, password })
}
```

具体方法需根据后端最终字段补写。

---

# 6. 权限控制（待补充）

- 登录后由前端 request.js 自动加入 Authorization 头  
- 受保护接口需携带 Bearer Token  
- Token 失效 → 自动重定向登录页  

相关说明将在后续版本补写。

---

# 7. 测试覆盖（待补充）

预计包含：

- 注册（成功 / 重复用户名）  
- 登录（成功 / 密码错误）  
- Token 刷新  

---

# 8. 后续扩展（待补充）

- 邮箱注册 / 验证码登录  
- 多端登录管理  
- 用户资料修改  
- 注销接口  

---
