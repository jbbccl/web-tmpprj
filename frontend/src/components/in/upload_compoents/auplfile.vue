<template>
    <div id="up_list" >
        <div id="loading-status"><div id="precent" ></div> </div>
        <div id="btns">
            <button id="stop" class="fil_btn" @click="UPL_btn" :disabled="stpbtndis">{{ stop_bt_stus }} </button>
            <button id="upup" class="fil_btn" @click="loadFile_d" :disabled="btndis" >上传</button> <!-- :disabled="btndis" -->
        </div>
    </div>
</template>

<script type="text/javascript">
    //document.getElementById('select_btn').click=

import { cutFile } from './cutfile.js';
import { debounce, reject } from 'lodash-es'
import {uploadFile } from './uploadfile.js';

import axios from 'axios';
import { resolveComponent } from 'vue';
export default{
    props:{
        file:{ 
            type:File,
            default:null    //默认值
        }
    },
    data() {
    //percent_w=this.finish_count_ref/this.chunkCount;
    let finish_count_ref= 0;
    let chunkCount_indata=1;
    let proms=[];
    let chunk_list;
    let controller_list=[];
    let file_name;
    return {
        finish_count_ref,
        percent_w:0,
        chunkCount_indata,
        stop_bt_stus:'终止',
        controller_list,
        proms,
        chunk_list,
        file_name,
        show_name:'选择文件',
        btndis:false,
        stpbtndis:false,
    }
    },
    created(){
    this.loadFile_d = debounce(this.loadFile, 200);
    
    },
    unmounted() {

        this.loadFile_d.cancel()
    },
    watch:{

    },
    methods: {
    wait(ms) {
        return new Promise((resolve, reject) => {
            setTimeout(() => {
                console.log("Done waiting");
                resolve(ms)
            }, ms)
        })
    },
    UPL_btn(){
        for (var i = 0; i < this.controller_list.length; i++) {
            //console.log(this.controller_list[i]);
            this.controller_list[i].abort();
            this.btndis=false;
            this.stpbtndis=true;
        }
        this.controller_list=[];
    },
    uploadChunks(chunk,deep=0){
        //console.log('======6===================')
        return new Promise((resolve)=>{
            const controller = new AbortController();
            this.controller_list.push(controller)
            axios.post('/api/home/upload_f',
                chunk, {
                signal: controller.signal,
                headers: {
                    'Content-Type': 'multipart/form-data',
                    'token':window.localStorage.getItem('token')
                }
                }).then(async e=>{
                    //this.controller_list.pop(controller);
                    if(e['data']['status_code']==114514){
                    this.finish_count_add();
                    resolve(e);
                    }else if(e['data']['status_code']==404){
                        if(deep<5){
                            await this.wait(1000);
                            console.log('deep=='+deep)
                            await this.uploadChunks(chunk,++deep)
                        }
                            resolve(e);
                    }
                }).catch(error=>{
                    console.log("========Catch=======  "+error)
                    resolve(error);
                })
        })
   
    },
    async loadFile() {
        //const self=this;
        this.btndis=true;
        this.stpbtndis=false;
        //console.log('======click===================');
        if (this.file) {
        const SIZE=5242880;//这里要和cutfile.js同步
        console.log(this.file)
        //console.log(this.file.size)
        const chunkCount=Math.ceil(this.file.size/SIZE);
        this.chunkCount_indata=chunkCount;
        this.finish_count_ref=0;
        //this.chunk_list
        if(typeof this.chunk_list == 'undefined'){
            console.log('===cut===')
            const rst = await cutFile(this.file)///同步12线程切文件
            console.log('===cut===')
            this.stop_bt_stus='终止'
            this.chunk_list=rst[0];
            this.file_name=rst[1];
        }
            let finish_file_url='/api/home/finish_file/'+this.file_name+'?n='+chunkCount.toString();
            //文件传了多少
            const finish_f_ls_row = await axios.get(finish_file_url,{
            headers:{
              'token':window.localStorage.getItem('token')
            }
          })

            let finish_f_ls=Object.values(finish_f_ls_row)[0];
            //console.log(finish_f_ls[0])//没有就是0

            for(let i=0;i<chunkCount;i++){
                console.log(this.chunk_list[i]['hash'])
                if(finish_f_ls[i]==this.chunk_list[i]['hash']){
                console.log('已存在'+i)
                this.finish_count_add();
                console.log(chunkCount);
                console.log(this.finish_count_ref);
                continue;
                
                }
                //console.log('===1======================')
                this.chunk_list[i]['file_name']=this.file_name;
                //console.log('===2=====================')


                console.log(this.chunk_list[i]);
                this.proms.push(this.uploadChunks(this.chunk_list[i]));
                //console.log(this.proms)
               // console.log('=====3====================')
            }//for end
            console.log('======4========proms===========')
            console.log(this.proms)
            if(this.proms.length){
                await Promise.all(this.proms);
            }
            //console.log('=======5==============================================')
            //console.log(up_result)
            
            
            let merge_url='/api/home//upload_f_end/'+this.file_name+'?n='+this.file.name+'&cc='+chunkCount;
            console.log('=======fin_status==============================================')
            console.log(chunkCount)
            console.log(this.finish_count_ref)

            if(chunkCount==this.finish_count_ref){
                //console.log('=======7==============================================')
                axios.get(merge_url,{
                    headers:{
                    'token':window.localStorage.getItem('token')
                    }
                }).then(merge_rst=>{
                    console.log('merge rst')
                    console.log(merge_rst)
                if(merge_rst['data']['status_code']==200){
                    console.log('=================finish==============================================')
                    this.stop_bt_stus='上传成功'
                }else if(merge_rst['data']['status_code']==401){
                    this.stop_bt_stus='重复上传或出错'
                }else{
                    this.stop_bt_stus='录入失败' 
                    this.btndis=false;       
                }
                this.finish_count_ref=0;
                this.stpbtndis=true;
            });
            }else{
                this.btndis=false;
                this.stop_bt_stus='中道崩殂';
            }
            console.log('结束了')
            console.log(this.proms)
//          IO密集型，多线程意义不大
/*           uploadFile(rst,chunkCount).then((up_rst)=>{
            const file_name=rst[1];
            let merge_url='/api/home//upload_f_end/'+file_name+'?n='+chunkCount.toString();
            axios.get(merge_url).then();
            }); */

        }
        
    },

    finish_count_add(){
        this.finish_count_ref++
        this.percent_w=100*(this.finish_count_ref/this.chunkCount_indata);
    }
    },
}

</script>

<style>
#btns{
    display: flex;
    flex-shrink: 1;
    gap: 2rem;
}

.fil_btn{
   width: 5rem;
    height: 1.7rem;
  background-color: rgba(255, 236, 66, 0.534);
    flex-shrink: 1;
  border-radius: 5px;
  border: 1px solid #fdc883;
  cursor: pointer;
}
.fil_btn:hover{
  background:rgba(241, 222, 42, 0.918);;
  transition:background-color 0.1s linear;
}
#up_list{
    flex-shrink: 1;
    gap: 5px;
    width: auto;
    max-width: 500px;
    height: auto;
    background-color: #cbd35dc9;
    padding: 10px;
    border-radius: 4px;
    margin-top: 1vh;
    display: flex;
    flex-direction: column;

}

#loading-status{
    width: 50vw;
    max-width: 490px;
       border: 1px #97c7cf solid;
       height: 15px;
       background: -webkit-gradient(linear, 0 0, 0 100%, from(#8da0ac9a), to(white));
       padding: 1px;
  }
#precent{
       /* background-color:linear-gradient(rgb(99, 194, 62),pink); */
       flex: 1;
       background:-webkit-gradient(linear, 0 0, 0 100%, from(#eaffd69a), to(rgb(88, 243, 31)));
       height: 100%;
       width: v-bind(percent_w+'%');
       transition: width 0.3s;
}




</style>
