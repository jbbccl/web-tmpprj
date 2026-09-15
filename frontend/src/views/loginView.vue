

<template>
  <div class="lon">

  </div>
<el-card style="max-width: 377px">
    <template #header>
      <div class="card-header">
        <span>
          <el-radio-group v-model="chCom" size="default">
            <el-radio-button label="loginC" value="loginC">登陆</el-radio-button>
            <el-radio-button label="siginC" value="siginC">注册</el-radio-button>
          </el-radio-group>
        </span>
      </div>
    </template>

    <component :is="chCom"  @childEvent="handleChild" ></component>
    
  </el-card>
</template>

<script>
import loginC  from '@/components/loginC.vue';
import siginC from '@/components/siginC.vue';
import {markRaw} from 'vue'
export default{
  data(){
    return {
      chCom: 'loginC'
    }
  },
  components:{
    loginC:markRaw(loginC),
    siginC:markRaw(siginC),
  },
  methods:{
    handleChild(data){
      //console.log('子组件传递');
      //console.log(data);
      this.chCom=data;
    }

  }
}
</script>

<style>
.el-card{
  margin: auto;
  line-height: 1%;
  color: #554d4d;
  background-color: #2e2e2e67;
  backdrop-filter: blur(5px);
}
.el-radio-button{
    color: #b85d5d;
    background-color: rgba(146, 143, 99, 0.329);
}
.lon{
  margin: auto;
  height: 15vh;
}
.el-radio-button__inner{
    background:none;
    color: white;
  }
  .el-loading-mask{
    background-color:rgba(250, 241, 165, 0.322);
    z-index: 5;
  }
  .el-button{
    color: #d4d4d4;
    background-color :rgba(116, 94, 23, 0.329);
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

