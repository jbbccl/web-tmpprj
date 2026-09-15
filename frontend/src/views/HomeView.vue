<script setup>

import { RouterLink, RouterView } from 'vue-router'
import axios from "axios";
import { debounce } from 'lodash-es'
</script>

<template>
  <div class="background">

    <header class="head">
      
      <div class="box_test" >  <el-button class="bt" style="color: rgb(170, 224, 119);" @click="getMessage">{{ msg }}</EL-button>  </div>
      <div class="box" ><h1>  </h1></div>
      <div class="box_hello" ><h4 id="hello">你好{{ usr_name }}</h4></div>
      <div class="box" ><h1>      </h1></div>
      <div class="box" ><h1>      </h1></div>
      <div class="box" ></div>
      
      <div class="box_my" >
        <el-button class="bt" @click="gohen">主页</el-button>
        <el-select @isible-change="chslt" @change="chslt" v-model="value" placeholder="我的">
          <el-option
            v-for="item in options"
            :key="item.value"
            :label="item.label"
            :value="item.value"
            :disabled="item.disabled">
          </el-option>
        </el-select>
      </div>
      <div class="box" ></div>
    </header>

    <div class="main">
  
     <component :is="chCom"  ></component>
      
    </div>
  </div> 

</template>

<script>
import {ref , markRaw} from 'vue'
import setting from '@/components/in/setting_compoents/setting.vue';
import update from '@/components/in/upload_compoents/update.vue';
import explo from '@/components/in/explo.vue';
import mainpage from '@/components/in/mainpage/mainpage.vue';
//import loginview  from '@/views/loginView.vue';

 export default {
  setup(){
    count=ref(0)
    return {
      count
    }
  },
  data() {
      //
      return {
        chCom:'mainpage',//此处默认值============
        msg:'点我！',
        options: [{
            value: 'update',
            label: '上传'
          }, {
            value: 'setting',
            label: '设置',
            disabled: false
          }, {
            value: 'explo',
            label: '自爆'
          }
        ],
        value: '',
        usr_name:''
      }
    },
    created:function() {
        this.get_usr_info();
        //this.ruleForm.name='1111';
        this.debouncedClick = debounce(this.getMessage, 100)
  },
  unmounted:function() {
    // 清除掉防抖计时器
        //this.debouncedClick.cancel()
  },
  components:{
    explo:markRaw(explo),
    update:markRaw(update),
    setting:markRaw(setting),
    mainpage:markRaw(mainpage)
  },
    methods: {  
      gohen(){
        this.chCom=mainpage;
        this.value='';
      },
      
      get_usr_info(){
        
        const self=this;
        axios.get('/api/home/info',{
            headers:{
              'token':window.localStorage.getItem('token')
            }
          }).then(function(res){
          //console.log(res.data['usr_name'])
          self.usr_name=res.data['usr_name'];
        })

      },

      chslt(e){
        this.chCom=this.value;
      },
      tologin(){
        this.$router.push({path:'/login'});
        console.log('niubi')
      },
      getMessage() {
        axios.get("/api/home/",
          {
            headers:{
              'token':window.localStorage.getItem('token')
            }
          }
        ).then((res) => {
          this.msg = res.data;        
        });
      },
      
    },//methods
  };
</script>

 <style>
 .el-select{
  max-width: 100px;
  min-width: 80px;
  color:#fff;
 }
 .el-select__placeholder{
  color:#fffffff6;
 }
  .el-select__wrapper{/*下拉框*/
    background-color: rgba(78, 70, 21, 0.397);
    color:#fff;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    font-size:large;
    font-weight: bold;
  }
  .el-popper.is-light{/*下拉框展开的连接处*/
    background-color: rgba(0, 0, 0, 0);
    background:none;
    color:#fff;
  }
  .el-popper__arrow::before{/*下拉框展开的连接处*/
    background:rgba(236, 225, 67, 0.089);
  }
  .el-select-dropdown.el-select__placeholder{/*下拉框展开处*/
    background-color: rgba(78, 70, 21, 0.397);
    color:#fff;
  }
  .el-select-dropdown__wrap{
    color:#fff;
  }
  .el-select-dropdown__item{/*下拉框未选中字*/
    color: rgb(255, 255, 230);
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
    font-size:large;
    font-weight: bold;
  }
  .el-select-dropdown__item.is-selected {/*下拉框选中字*/
  color: rgb(255, 255, 230);
  font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
  font-weight: bolder;
  font-size:x-large;
}
.el-select-dropdown__item.is-hovering {
  background-color: rgba(99, 210, 243, 0.651);/*选中cover*/
}
  .background{
      background-image: url("../images/BingWallpaper1.jpg");
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
    /* overflow: scroll; */
    position:fixed;
    top:10vh;
    width: 100%;
    height: 92vh;
  }
  .el-button{
    color: #d4d4d4;
    background-color :rgba(116, 94, 23, 0.329);
  }

.box{
  flex-grow: 10;
  line-height: 8vh;
  display: flex;
  z-index: 5;
  /* display: inline-flex; */
  align-items: center;
}
.box_my{
  flex-grow: 4;
  line-height: 8vh;
  display: flex;
  z-index: 5;
  /* display: inline-flex; */
  align-items: center;
  gap:1.5rem;
}
.box_hello{
  display: flex;
  font-size: large;
  align-items: center;
}
.box_test{
  display: flex;
  align-items: center;
}
.bt{
  font-size: 1rem;
  line-height: 0.1rem;
  color: rgb(173, 245, 151);
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
p {
white-space: nowrap;
font-size: 0.8rem;
font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif;
color:rgba(252, 249, 104, 0.822)
}
#hello{
  color: rgb(211, 231, 120);
}
</style>