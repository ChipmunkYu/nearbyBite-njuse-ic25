# 前端框架说明

目前初步搭建好前端框架（frontend）
新加入的文件文件夹可以在此处进行简单说明

## 目录结构说明

### src 目录

#### assets
存放需要使用的图片、样式、字体等文件

#### components
存放可复用的 Vue 组件
- AuthLayout.vue - 登录注册页面组件（保证相同风格）

#### pages
完整页面，新添加的页面放在此文件夹
- Error.vue - 错误页面
- first.vue - 登录后进入的首页  
- Home.vue - 进入登录或者注册的页面
- Login.vue - 登录页面
- Register.vue - 注册页面
- Recommend.vue - 推荐页面

#### router
定义路由映射、配置路由行为、管理导航
- index.js - 主路由配置

#### stores
集中状态管理、状态共享、业务逻辑封装
- index.js - Pinia 实例创建和导出
- user.js - 用户状态管理模块

#### utils
放置工具函数、辅助方法
- api.js - 封装 Axios 工具
- errorPage.js - 错误页面跳转工具函数

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