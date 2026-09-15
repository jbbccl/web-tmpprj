<script setup>

import { RouterLink, RouterView } from 'vue-router'
import axios from "axios";
import { debounce } from 'lodash-es'
</script>

<template>
  <div class="background">

    <header class="head">
      <div class="box" ><h1>  </h1></div>
      <div class="box" >  <el-button class="bt" @click="getMessage">{{ msg }}</EL-button>  </div>

      <div class="box" ><h1>      </h1></div>
      <div class="box" ><h1>      </h1></div>
      <div class="box" ><h1>      </h1></div>
      <div class="box" ><h1>      </h1></div>
      
      <div class="box" ><el-button class="logbt" @click="tologin">登陆</el-button></div>
      <div class="box" ><h1>      </h1></div>
    </header>

    <div class="main">
      <RouterView></RouterView>
    </div>
  </div> 

</template>

<script>
//import loginview  from '@/views/loginView.vue';
 export default {
    data() {
      return {
        msg: "点我！",
      };
    },
    created:function() {
        //this.ruleForm.name='1111';
        this.debouncedClick = debounce(this.getMessage, 500)
  },
  unmounted:function() {
    // 清除掉防抖计时器
        //this.debouncedClick.cancel()
  },
    methods: {  
      tologin(){
        this.$router.push({path:'/login'});
        console.log('niubi')
      },
      getMessage() {
        axios.get("/api/").then((res) => {
          this.msg = res.data;        
        });
      },
      
    },//methods
  };
</script>

 <style>

  .background{
      background-image: url("../images/BingWallpaper.jpg");
        width: 100%;
        height: 100%;
        position:fixed;
        top: 0;
        left: 0;
        width:100%;
        height:100%;
        min-width: 1000px;
        z-index:-10;
        zoom: 1;
        background-color: #fff;
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;

  }
  .head{
    /* margin: auto; */
    background: linear-gradient(to top, rgba(78, 78, 78, 0), 20%, rgba(0, 0, 0, 0.705));
    display: flex;
    position: fixed;
    width: 100%;
    background-color: #0a0a0a27;
    min-width: 10px;
    height: 8vh;
    z-index: 3;
    backdrop-filter: blur(0px);
    display: inline-flex;
    /* 默认值 从左向右排列 */
    flex-direction: row;
  }
  .main{
    position:fixed;
    top:8vh;
    width: 100%;
    height: 92vh;
  }
  .el-button{
    color: #d4d4d4;
    background-color :rgba(116, 94, 23, 0.329);
  }

.box{
  line-height: 8vh;
  min-width: 0vh;
  max-width: 24vh;
  width: 12%;
  display: flex;
  z-index: 5;
  display: inline-flex;
  align-items: center;
}
.logbt{

  font-size: 12px;
  background-color:rgba(107, 116, 116, 0.452);
  z-index: 5;
}
:root{
  --el-color-primary-light-3 : rgba(146, 143, 99, 0.329);
  --el-color-primary:rgb(95, 95, 80);
  --el-border-color:rgba(0, 0, 0, 0.26);
  --el-color-primary-light-9:rgba(255, 255, 255, 0.308);
  --el-color-primary-dark-2: rgba(255, 255, 255, 0.541);
  /* --el-border-width:2px; */
  --el-border-style:none;
  --el-color-primary-light-5:rgba(255, 255, 255, 0.541);
  --el-color-primary:rgba(216, 216, 216, 0.842);    /*鼠标进入按钮字体*/
  --el-color-primary-light-9 :rgba(180, 180, 180, 0.438);/*鼠标进入按钮*/
}
</style>
