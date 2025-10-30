import { createRouter, createWebHistory } from 'vue-router'
import Login from '../pages/Login.vue'
import Register from '../pages/Register.vue'
import Home from '../pages/Home.vue'
import First from '../pages/first.vue'
import Error from '../pages/Error.vue'
import Recommend from '../pages/Recommend.vue' 

//声明一些基础路由，后续增加页面从此处添加

const routes = [
{path: '/', component: Home},
{path: '/login', component: Login},
{path: '/register', component: Register},
{path: '/first', component: First},
{path: '/recommend', component: Recommend },

//...新增路由放在这里声明，注意不要放在错误之后！！！



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
export default router