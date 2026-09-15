<style>
.card{
    width: 14rem;
    height: 10rem;
    background: yellowgreen;
    border-radius: 5px;
}
.card:hover{
    background: rgb(140, 190, 39);
    transition: .15s background;
}
#vid_name{
    position: relative;
    left: 5%;
    top:3%;
    word-wrap:break-word;
    width: 13rem;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-box-orient: vertical;
    -webkit-line-clamp:3; /* 限制为三行 */
    overflow: hidden;
}

</style>
<template>
    <div class="card" @click="go_vid">
        <h4 id="vid_name">
            {{ vid_obj.v_name }}
        </h4>
        <img >
      
    </div>
</template>

<script type="text/javascript">
import { stringifyQuery } from 'vue-router';


export default{
    props:{//vid,v_name,type,like,date,info
        vid_obj:{ 
            type:Object,
            default:null    //默认值
        }
    },
    data() {

    return {

    }
    },
    created(){
    
    },
    unmounted() {

    },
    methods: {
        go_vid(){
            console.log('test')
            let newPage = this.$router.resolve({ 
            path: '/video', 
            query: this.vid_obj
            });
            window.open(newPage.href, '_blank');
        }
    },
}

</script>