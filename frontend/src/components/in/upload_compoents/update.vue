
<template>
<div class="main1">
  <div class="zhan"></div>
  <div class="upload_table">
      <div class="select-container" @ondrop="handleFile">
        <input id="select_file" name="select_file" type="file" multiple="multiple" @change="handleFile" style="display: none;">
        <label for="select_file" id="sl_fl">{{show_name}}</label>
        <!-- 这是真的秒啊-->

    </div>
    <div class="kongde"></div>
    
    

      <div id="list_contianer" ref="container">
        <div class="file_list_item" v-for="(file,obj_key) in file_list" :key="obj_key" :ref="`item-${obj_key}`">

            <div class="flex_row" :ref="`name-${obj_key}`">
              <button @click="removeCom(obj_key)" id="removecom">X</button>
              <p id="filename">{{ file.name }}</p>
            </div>
            <auplfile :file="file" :key="obj_key"/>

        </div>
      </div>



  </div>
  <div class="zhan"></div>
</div>
</template>

<script type="text/javascript">
    //document.getElementById('select_btn').click=
import {createApp} from 'vue'
import { cutFile } from './cutfile.js';
import { debounce } from 'lodash-es'
import {uploadFile } from './uploadfile.js';
import auplfile from '@/components/in/upload_compoents/auplfile.vue'
export default{
  data() {
    //percent_w=this.finish_count_ref/this.chunkCount;
    //let finish_count_ref= 0;
    //let chunkCount_indata=1;
    //const proms=[];
    //let controller_list=[];
    return {
      file_list: {},
      file_idx:3,
      //finish_count_ref,
      //percent_w:0,
      //chunkCount_indata,
      //stop_bt_stus:'终止',
      //controller_list,
      //proms,
      show_name:'选择文件',
      //counter_a:[1],
      hide_height:''
    }
  },
  components:{
    auplfile,
  },
  created(){
  },
  unmounted() {
  },
  methods: {
    removeCom(index){
      const e_list= this.$refs[`item-${index}`];
      //const e_name = this.$refs[`name-${index}`];
      e_list[0].style.height='0'
      //e_name[0].style.height='0'
      e_list[0].style.opacity="0";
      console.log(index)
      setTimeout(() => {
        delete this.file_list[index]
        console.log(this.file_list)
      },350);
      
    },
    handleFile(event) {
      //for(let i=0;i<e
      //console.log(event.target.files)
      let lists = Array.from(event.target.files);
      for (const item of event.target.files){
        this.file_list[this.file_idx]=item;
        this.file_idx++;
      }
      console.log(this.file_list)
      //this.file_list.push(event.target.files[0]);
      //this.c_index++;
      const container = this.$refs.container;
      console.log('=======================')

      const myComponent = createApp({}).component(auplfile)
      //myComponent.mount(document.getElementById('container'))
      console.log('=======================')
    },
  },

}

</script>

<style>
.file_list_item{

  height: 6.2rem;
  transition-timing-function: cubic-bezier(.47,1.13,.63,-0.41);/* cubic-bezier(.6,1.23,.74,-0.17); *//* cubic-bezier(.68,1.57,.79,-0.71); *//* cubic-bezier(.53,1.45,.88,-0.96); */
  transition-property: opacity , height; 
  transition-duration:.35s , .35s;
  display: flex;
  flex-direction: column;
  border-radius: 2px;
  box-shadow: 6px 6px 10px rgba(0, 0, 0, 0.2);
}

.flex_row{
  display: flex;
  flex-shrink: 1;
  height: 1.5rem;
  align-items:center;
}
.kongde{

  width: 10px;
  height: 10px;

}
#list_contianer{
  background-color: rgba(221, 124, 45, 0.336);
  Flex-wrap:wrap;
  display: flex;
  gap: 1rem;
  height: auto;
  width: auto;
  overflow: auto;
  max-width: 32rem;
  max-height: 57vh;
  padding: 8px;
  border: 1px solid #fdc883;
  border-radius: 3px;
}
.select-container{
 /*  background-color: rgba(160, 45, 45, 0.281); */
  
  Flex-wrap:wrap;
  text-align: center;
  width: auto;
  max-width: 34rem;
}
#sl_fl{
  background-color: #eba95eab;
  font-size: 1rem;
    font-weight: 700;
    align-items: center;
    line-height: 1rem;
    color: white;
    display: inline-block;/**这是调整宽度的关键 */
    line-height:2.4rem;
    word-wrap:break-word;
    height: 2.3rem;
    max-width: 32rem;
    width: 100%;
    border: 1px solid #fdc883;
    border-radius: 3px;
}
#sl_fl:hover{
  background:rgba(255, 232, 102, 0.575);
  transition:background-color 0.1s linear;

}

.upload_table{
  background-color: rgba(139, 139, 139, 0.411);
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  flex-shrink: 1;
  width: 100px;
  border-radius: 5px;
  height: 70%;
  border: 1px solid #fdc883;
  padding: 25px;
  flex-grow: 10;
  flex-shrink: 0;
}
.zhan{
  display: flex;
  height: 300px;
  width: 1px;
  flex-grow: 3;
  flex-shrink: 1;
}

#select_b{
  height: 8vh;

}
.main1{
  display: flex;
  justify-content: center;
  gap: 10px;
  flex-grow: 1;

}
#filename{
    flex-shrink: 1;
    color: rgb(238, 231, 220);
    line-height: 0%;
    font-size: 1.1rem;
}
#removecom{
  flex-shrink: 1;
  background-color: rgba(255, 8, 8, 0.575);
  height: 1.2rem;
  width: 1.2rem;
  border-radius: 10px;
  border: #fdc883;
  color: aliceblue;
  text-align: center;
}
</style>

<!-- 

methods(){
scfzj(n){
    this.$emit('handleChild',n)//触发'handleChild'事件 父组件@handleChild='方法'
  },
} -->
