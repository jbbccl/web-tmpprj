<template>
    <el-form :model="ruleForm" status-icon :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm" >
        <el-form-item label="用户名" prop="name">
            <el-input type="text" v-model="ruleForm.name" autocomplete="off"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pass">
            <el-input type="password" v-model="ruleForm.pass" autocomplete="off"></el-input>
        </el-form-item>

        <el-form-item>
            <el-button type="primary" @click="debouncedClick('ruleForm')" :disabled="btndis" v-loading="buildloading">提交</el-button>
            <el-button @click="resetForm('ruleForm')" >重置</el-button>
        </el-form-item>
  </el-form>

</template>

<script>
//import lodash from 'lodash'
import axios from 'axios';
import {ref} from 'vue';
import { debounce } from 'lodash-es'

 export default {
    
    data() {
      const buildloading = ref(false);
      const btndis = ref(false);


      var usrname = (rule, value, callback) => {
        if (!value) {
          return callback(new Error('请输入用户名'));
        }else{
          callback();
        }
      };
      var passwd = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入密码'));
        } else {
          if (value.length<3) {
            callback(new Error('密码小于5位'));
          }
          callback();
        }
      };

      return {
        buildloading,
        btndis,
        ruleForm: {
          pass: '',
          name: '',
        },
        rules: {
          pass: [
            { validator: passwd, trigger: 'blur' }
          ],
          name: [
            { validator: usrname, trigger: 'blur' }
          ]
        }
      };
    },
    created() {
        //this.ruleForm.name='1111';
        this.debouncedClick = debounce(this.submitForm, 200)
  },
  unmounted() {
    // 清除掉防抖计时器
        this.debouncedClick.cancel()
  },
    methods: {
      submitForm(formName) {
        console.log('clicked')
        const self=this
        this.$refs[formName].validate((valid) => {
          if (valid) {
            self.buildloading =true;
            self.btndis=true;
            axios.post('/api/login', {
              passwd: this.ruleForm.pass,
              usrname: this.ruleForm.name
            })
            .then(function (response) {
              //console.log(response.data['Hello']);
              //const token=response.data['token']//=================token
              if(response.data['Hello']===1){
                window.localStorage.setItem('token',response.data['token'])
               // alert('登陆成功');
                //var now=new Date();
                //now.setMinutes(now.getMinutes()+300)//设置时间300分钟过期
                //document.cookie="usr_status=login_"+response.data['id']+';expires='+now.toUTCString()+'secure=true;samesite=strict';
                self.$router.push({path:'/home/',query: {id:response.data['id']}})
              }else{
                alert('登陆失败');
              }
              self.buildloading =false;
              self.btndis=false;
            })
            .catch(function (error) {
              alert('登陆失败，');
              console.log(error);
              self.buildloading =false;
              self.btndis=false;
            });
          } else {
            console.log('error submit!!');
            return false;
          }
        });

      },
      resetForm(formName) {
        this.$refs[formName].resetFields();
      },
      
    }
  }
</script>

<style lang="scss" scoped>
@import "@/style/elstyle.scss";
</style>

<style>
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