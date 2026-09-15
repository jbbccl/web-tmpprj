<template>

    <el-button @click="logout">登出</el-button>
    <el-button @click="handleGetData">发送请求</el-button>
    <el-button @click="handleCancel">取消请求</el-button>
</template>

<script>
import axios from 'axios';
export default{
    data(){
        return {
            source: null
        }
    },
    methods:{
        logout(){
            const self=this;
            axios.get('/api/logout',{
            headers:{
              'token':window.localStorage.getItem('token')
            }
          }).then(
                function(res){
                    if(res.data['status']=='logout'){
                        document.cookie="usr_status=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;"
                        self.$router.push({path:'/guest',})
                    }else{
                        alert('注销失败，稍后')
                    }
                }
            ) 
        },
        async handleGetData() {
      const source = axios.CancelToken.source()
      this.source = source
      // source接收的是axios内部提供用于取消请求的方法
      // 我个人的理解是，每一个请求都有对应自己的token，axios通过这个去取消对应的请求
      try {
        const res = await getDataList(source.token)
        console.log(res)
      } catch (error) {
        // console.log(error)
      }
    },
    // 取消请求
    handleCancel() {
      this.source.cancel('取消请求')
      // cancel内的取消请求可以当成是取消请求后抛出的提示文案，可打印this.source.cancel('取消请求')看看
    },
       
    }
}
</script>
