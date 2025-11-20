import { createRouter, createWebHistory } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user' 
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Home from '../pages/Home.vue'
import First from '../pages/first.vue'
import Error from '../pages/Error.vue'
import Recommend from '../pages/Recommend.vue' 


//声明一些基础路由，后续增加页面从此处添加
//需要登录的路由在meta中添加requiresAuth: true

const routes = [
{path: '/', component: Home},
{path: '/login', component: Login},
{path: '/register', component: Register},
{path: '/first', component: First, meta: { requiresAuth: true } },
{path: '/recommend', component: Recommend, meta: { requiresAuth: true } },

{
  path: '/error/:code',
  name: 'ErrorPage',
  component: Error,
  props: route => ({
    code: Number(route.params.code) || 500,
    message: route.params.message || '服务器错误'
  })
},
//...新增路由放在这里之前声明，注意不要放在错误之后！！！
{
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: Error,
    props: route => ({
      code: route.params.code || 404,
      message: route.params.message || '抱歉，页面未找到'
    })
  }


]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth) {
    if (!userStore.token) {
      ElMessage.warning('请先登录后再访问～🍱')
      next({
        path: '/login',
        query: { redirect: to.fullPath }  
      })
    } else {
      next()
    }
  } else {
    next()
  }
})

export default router