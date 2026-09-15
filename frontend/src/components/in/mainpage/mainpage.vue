<style>
.main_vidlist{
    background-color: rgba(197, 157, 133, 0.534);
    width: 80%;
    max-height: 84vh;
    display:flex;
    margin: auto;
    overflow-y: auto;
    scrollbar-width: none;/* firefox */
    flex-wrap: wrap;
    justify-content:center;
    gap: 12px;
    padding: 12px;
    border-radius: 10px;
    align-content: flex-start;/* flex-wrap一般情况下和align-content一起用 */
}
::-webkit-scrollbar {
  display: none; /* Chrome Safari */
}
#box_vidlist{
    z-index: -1;
    /* background-color: rgb(255, 240, 240); */
    position: fixed;
    width: 100%;
    height: 100%;
    display: flex;
    gap: 12px;
}
#next_msg{
    width: 14rem;
    height: 3rem;
    text-align: center;
}
</style>
<template>
    <div id="box_vidlist"></div>

    <div class="main_vidlist" id="vidlist" @scroll="scrollEvent($event)" >
        
        <div v-for="vid_obj in vid_list">
            <file_card :vid_obj="vid_obj"/>
        </div>
        <h3 id="next_msg">{{ is_have_next }}</h3>
    </div>
</template>

<script>
import axios from 'axios';
import AVedio from './aVedio.vue';
import file_card from './file_card.vue';
export default{
    data(){
        const get_vl_len=3;
        return{
            vid_list:[],
            list_idx:0,
            get_vl_len,
            have_next:1,
            is_have_next:''
        }
    },
    components:{
        AVedio,
        file_card
    },
    created:function(){
        this.get_vid_list();
    },
    methods:{
        hasScrollbar() {
            return document.body.scrollHeight > (window.innerHeight || document.documentElement.clientHeight);
        },
        get_vid_list(){
            let url='/api/home/video/get_list/'+this.list_idx.toString()+'?l='+this.get_vl_len.toString();
            axios.get(url).then(res=>{
                console.log(res)
                if(res.data==0){
                    this.have_next=0;
                    this.is_have_next='=======没有了========'
                }else{
                    this.list_idx+=this.get_vl_len;
                    for (let i = 0; i < res.data.length; i++){
                        this.vid_list.push(res.data[i]);
                    }
                let e=document.getElementById('vidlist');
                if(e.scrollHeight==e.clientHeight){
                    this.get_vid_list();
                }
           /*      console.log(e.scrollHeight)
                console.log(e.clientHeight) */
                //console.log(this.vid_list)
                }
 
            })
        },
        scrollEvent(e) {
/*             console.log(e.target.scrollHeight)
            console.log(e.target.clientHeight) */
            if (e.target.scrollTop + e.target.offsetHeight >= e.target.scrollHeight-50 || e.target.scrollHeight == e.target.clientHeight) {
                clearInterval(this.timer)
                console.log('啦啦啦啦啦了触底')
                this.timer = setTimeout(() => {
                    console.log(this.have_next)
                    if(this.have_next==1){
                        this.is_have_next='=======加载中========'
                        this.get_vid_list();
                    }
                }, 500)

            }
        },
    }
}
</script>