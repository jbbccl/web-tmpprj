<template>
  <div class="ch_name">
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" >
        <el-form-item type="text" label="用户名" prop="usrname">
        <el-input v-model="ruleForm.usrname"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
        <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item>
        <el-button id="fbt" type="primary" @click="debouncedClick('ruleForm')"  v-loading="buildloading" :disabled="btndis" >提交</el-button>
        <el-button id="fbt" @click="resetForm('ruleForm')">重置</el-button>
        </el-form-item>
        <p>{{ ruleForm.formsg }}</p>
    </el-form>
  </div>


</template>

<script>
import axios from 'axios';
import { disabledTimeListsProps } from 'element-plus/es/components/time-picker/src/props/shared.mjs';
import { ref } from 'vue'
import { debounce } from 'lodash-es'

  export default {
    data() {
      var namelist=new Array();
      const buildloading = ref(false)///////LOADING
      const btndis = ref(false)
      var usenameRepet = (tmpName)=>{
        return axios.post('/api/checkTmpName', {usrname:tmpName}) 
      }
      var usenameck = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('你要改成啥'));
        }
        else if(value.length>15){
          callback(new Error('太长'));
        }
        else{
          console.log('this.ruleForm.usrname')
          console.log(this.ruleForm.usrname)
          if(namelist.indexOf(this.ruleForm.usrname)===-1){//=====================添加块注释压力给到后端============================if(/*usenameRepetFlag==*/1)
            const self=this;
            usenameRepet(this.ruleForm.usrname).then(function (response) {
              if(response.data== 1){
                callback();
              }
              else{
                namelist.push(self.ruleForm.usrname);
                console.log(namelist);
                callback(new Error('被别人用了，换一个吧'));
              }
              }).catch(function (error) {
                callback(new Error(error));       //待处理 
              });
            }else{
              console.log(namelist)
              callback(new Error('用户名确实被别人用了'));
            }
          }
        }
      var validatePass = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          callback();
        }
      };

      return {
        buildloading,
        btndis,///////LOADING
        ruleForm: {
          pass: '',
          usrname: '',
          formsg:'',
        },
        rules: {
          pass: [
            { validator: validatePass, trigger: 'blur' }
          ],
          usrname: [
            { validator: usenameck, trigger: 'blur' }
          ]
        }
      };
    },
    created:function() {
        //this.ruleForm.name='1111';
        this.debouncedClick = debounce(this.submitForm, 200)
  },
  unmounted:function() {
    // 清除掉防抖计时器
        this.debouncedClick.cancel()
  },
    methods: {
      submitForm(formName) {
        this.$refs[formName].validate((valid) => {
          if (valid) {
            this.buildloading=true;
            this.btndis=true;
            const self =this;
            axios.post('/api/registry', {
              passwd: this.ruleForm.pass,
              usrname: this.ruleForm.usrname
            })
            .then(function (response) {
              console.log(response);
              if(response.data==1){
                self.$emit('childEvent', 'loginC')//===============向父组件传
                alert('修改成功');
              }else{
                alert('修改失败');
              }
              self.buildloading=false;
              self.btndis=false;
            })
            .catch(function (error) {
              alert('修改失败，网络问题');
              console.log(error);
              self.buildloading=false;
              self.btndis=false;
            });
            //this.ruleForm.formsg ="成啦";
            
          } else {
            console.log('error submit!!');
            return false;
          }
        });
      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      }
    }
  }
</script>


<style>
.el-form-item{
  color: rgb(170, 224, 119);
}
.el-form-item__label{
  font-size: 70%;
  color: rgb(170, 224, 119);
}
.el-form-item__error{
  font-size: 70%;

}
#fbt{
  margin:2%;
  width: 15%;
  height: 15%;
}
.el-form-item{
  display: flex;
}
.el-input{
  height: 70%;
}
.ch_name{


  right:5%;
  margin: auto;
  position: fixed;
  width: 72%;
  height: 30%;
  display: flex;
}
</style>