<template>
    <div class="seting">

        <div class="side">
            <div class="kong"></div><br>
            <div class="set_item">
                <el-button class="sb" @click="chcp('usrInfo')">改名</el-button>
            </div>
            <div class="set_item">
                <el-button class="sb" @click="chcp('usrInfo')">22</el-button>
            </div>
            <div class="set_item">
                <el-button class="sb" @click="chcp('usrInfo')">22</el-button>
            </div>
            <div class="set_item">
                <el-button class="sb" @click="chcp('usrSafe')">登出</el-button>
            </div>
        </div>
        <div class="set_main">
            <component :is="chCom" ></component>
        </div>
    </div>
    
</template>

<script>
import {ref,markRaw} from 'vue'
import usrInfo from '@/components/in/setting_compoents/set_usrInfo.vue'
import usrSafe from '@/components/in/setting_compoents/set_usrSafe.vue'
export default{
    data(){

    return {
        chCom:usrInfo,
        tabPosition:'left'
        }
    },
    components:{
        usrInfo:markRaw(usrInfo),
        usrSafe:markRaw(usrSafe),
    },
    methods:{
        chcp(comp){
            this.chCom=comp;
        },
        handleOpen(key, keyPath) {
        console.log(key, keyPath);
      },
      handleClose(key, keyPath) {
        console.log(key, keyPath);
      }
    }
}

</script>
<style>
.set_main{
    margin: auto;
    position: fixed;
    right:5%;
    top:3%;
    width: 35vw;
    height: 100%;
    
}
.sb{
    border-radius:0;
    height: 100%;
    width: 100%;
    background-color: rgba(240, 248, 255, 0.151);
    border: none;
}
.set_item{
    border-style:solid;
    border-width:1px;
    height: 10%;
}
.side{
    border-style:solid;
    border-width:1px;
    position: fixed;
    flex-direction: column;/*主轴 */
    justify-content: center;/*在主轴上居中 */
    width: 20%;
    min-width: 18vw;
    height: 99%;
    flex-shrink: 0;
}
.kong{
    width: 100%;
    height: 7vh;
}
.seting{
    Flex-wrap:wrap;
    margin: auto;
    text-align: center;
  line-height: 1%;
  color: #d8c97583;
  background-color: #2e2e2e67;
  backdrop-filter: blur(2px);
  display: flex;
  width: 57%;
  min-width: 500px;
  min-height:80%;
}
.el-input__wrapper{
    background-color: rgba(65, 65, 65, 0.911);
    color: #d4d4d4;
  }
  .el-form-item__label{
    color: #d4d4d4;
  }
  .el-input__inner{
    color: #d4d4d4;
  }
</style>