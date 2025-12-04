# 前端框架说明

目前初步搭建好前端框架（frontend）
新加入的文件文件夹可以在此处进行简单说明

## 目录结构说明

### src 目录

#### assets
存放需要使用的图片、样式、字体等文件
vue.svg

#### components
存放可复用的 Vue 组件
- AuthLayout.vue - 登录注册页面组件（保证相同风格）
- BackHomeButton.vue - 返回首页的小按钮
- EmptyState.vue - 页面数为空

#### pages
完整页面，新添加的页面放在此文件夹
- Error.vue - 错误页面
- first.vue - 登录后进入的首页  
- Home.vue - 进入登录或者注册的页面
- Login.vue - 登录页面
- Register.vue - 注册页面
- Recommend.vue - 推荐页面
- Userstats.vue - 饮食统计图表页面
- Settings.vue  - 用户设置页面
- Restaurant.vue - 餐馆管理页面（含增删改查）
- History.vue - 浏览历史页面

#### router
定义路由映射、配置路由行为、管理导航
- index.js - 主路由配置

#### stores
集中状态管理、状态共享、业务逻辑封装
- index.js - Pinia 实例创建和导出
- user.js - 用户状态管理模块

#### utils
放置工具函数、辅助方法

errorPage.js          # 错误处理跳转
loading.js            # 全局 Loading 效果

### api
- auth.js          # 登录 / 注册 API
- history.js       # 浏览历史 API
- index.js         # API 管理入口
- request.js       # 封装 axios 请求，自动注入 token、处理刷新

### api  封装 Axios 工具
- auth.js -  登录 / 注册 / token
- history.js - 浏览记录
- index.js - 统一出口（添加新文件后，之后记得在此处添加相应export!!!）

- errorPage.js - 错误页面跳转工具函数
- loading.js - 全局loading
- loading.js - 加载状态

### 根目录文件

#### App.vue
Vue 应用的根组件

#### main.js
Vue 应用的入口文件

#### style.css
全局样式文件

## 快速开始
cd ../frontend

安装依赖：
npm install

启动开发服务器：
npm run dev