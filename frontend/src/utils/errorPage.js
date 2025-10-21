import router from '@/router'  // 直接导入 router 实例

export function goErrorPage(code = 500, message = '服务器错误') {
  router.push({
    name: 'NotFound',
    params: { code, message }
  })
}
