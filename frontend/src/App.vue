<script setup>

import { RouterLink, RouterView } from 'vue-router'
import axios from "axios";
import { debounce } from 'lodash-es'
</script>


<template>
   <router-view />
   
</template>

<script>

 export default {
    data() {
      return {
        msg: "点我！",
      };
    },
    created:function() {
        //this.ruleForm.name='1111';
        this.debouncedClick = debounce(this.getMessage, 100)
  },
  unmounted:function() {
    // 清除掉防抖计时器
        //this.debouncedClick.cancel()
  },
    methods: {  
      getMessage() {
        axios.get("/api/").then((res) => {
          this.msg = res.data;        
        });
      },
      
    },//methods
  };
</script>

<style>
   .bt{
    background-color:rgba(107, 116, 116, 0.452);
    
  } 
</style>
 <!-- <style>
  #app {
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
  }
  .common-layout{
    position: absolute;
    top: 0;
    left: 0;
    width: 100vw;
    height:100vh;
  } 
  .el-container{
    top: 0;
    left: 0;
    width: 100vw;
    height:100vh;
  }
  .el-header, .el-footer {
        background-color: #fff8b8;
        color: #333;
        text-align: center;
        line-height: 60px;
    }

    .el-aside {
        background-color: #fffd80;
        color: #333;
        text-align: center;

    }

    .el-main {
        background-color: #f3faba;
        color: #333;
        text-align: center;
    }
</style>

 -->


<!-- <style scoped>
header {
  text-align: center;
  padding: 20px;
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: end;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style> -->
