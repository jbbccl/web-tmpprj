import axios from 'axios'
import { createRouter, createWebHistory } from 'vue-router'

function getCookie(cname){
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
      var c = ca[i].trim();
      if (c.indexOf(name)==0) { return c.substring(name.length,c.length); }
  }
  return "";
}

const router = createRouter({

  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/home',
      name: 'home',
      component: () => import('../views/HomeView.vue'),
    },
    {
      path: '/video',
      name: 'video',
      component: () => import('../views/aVedio.vue')
    },
    {
      path: '/guest',
      name: 'guest',
      component: () => import('../views/guestView.vue'),
      children:[
        {
          path: '/login',
          name: 'login',
          component: () => import('../views/loginView.vue')//需要这样的结构才能使用guestview下的<router-view> 否则使用app.vue下
        },
      ]
    },

/* path: '/about',
      name: 'about',
      route level code-splitting
      component: () => import('../views/AboutView.vue')*/
  ]
})

router.beforeEach((to,from,next)=>{
  const usr_status=getCookie('usr_status')
  if(usr_status.length>0){
    console.log('==================')
    if(to.path==='/'|| to.path==='/login' || to.path==='/guest'){//重定向在访问/前 跳转到home  登录后无需要停留的
     // console.log('++++++++++++++++++++')
      next('/home')
    }else{
      next()
    }
  }else{
    if(to.path==='/login'|| to.path==='/guest'||to.path==='/home/video'){//未登录可使用的页面
      next()
    }else{
      next('/guest')
    }
  }
  

})

export default router
