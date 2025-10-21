#大概框架说明（可改）
目前初步搭建好前端框架（frontend）
这里说明一下大概的已创建用到的主要目录

*src：

--assets : 存放需要使用的图片，样式，字体等文件

--components : 存放可复用的Vue文件
    AuthLayout.vue : 登录注册页面组件（保证相同风格）

--pages : 完整页面，新添加的页面放在此文件
    Error.vue : 错误页面
    first.vue : 登录后进入的首页
    Home.vue  : 进入登录或者注册的页面
    Login : 登录页面
    Register : 注册页面

--router :  定义路由映射,配置路由行为,管理导航
    Index : 主路由配置

--stores : 集中状态管理, 状态共享, 业务逻辑封装
    index.js : Pinia 实例创建和导出

--utils  : 放置工具函数，辅助方法之类的
    api.js : 封装 Axios 工具
    errorPages.js : 错误页面跳转工具函数

*App.vue : Vue 应用的根组件

*main.js : Vue 应用的入口文件

*style.css : 全局样式文件