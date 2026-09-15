<template>
<div class="background">
    <div id="main">
        <div id="drag">
       <iframe class="iframe" id="bi_iframe" :onload="adjustIframe" :src="vid_src"
        frameborder="0" scrolling="auto"></iframe> 
        </div>
        <h3>按住右下角拖动</h3>
    </div>
</div>


</template>

<script>
export default{
    data(){
        let vid_obj;
        return {
            ifmwidth:0,
            ifmhight:0,
            vid_obj,
            vid_src:"/api/home/video/"+'3'
        }
    },
    created() {
        //this.ruleForm.name='1111';
        
        this.fetchData()
        
    },
    methods:{
        adjustIframe(){
            this.ifmhight=document.documentElement.clientHeight;
            this.ifmwidth=document.documentElement.clientWidth;
            console.log(this.ifmwidth/this.ifmhight)
            if((this.ifmwidth/this.ifmhight)>1){
                this.ifmwidth=55;
                this.ifmhight=55;
            }else{
                this.ifmwidth=93;
                this.ifmhight=30;
            }
        },
        fetchData() {
        this.vid_obj=this.$route.query;
   /*      console.log('""""""""""""""""""')
        console.log(this.vid_obj)
        console.log(this.vid_src) */
        this.vid_src='/api/home/video/'+this.vid_obj['vid'].toString()
        },
    }
}

</script>
<style>
#drag{
    width: v-bind(ifmwidth+'vw');
    height:v-bind(ifmhight+'vh');
    background-color: aliceblue;
    resize:both;
    overflow:auto; 
    display: flex;
}
.iframe{
    color: aliceblue;
    background-color: rgb(95, 95, 95);
    display: flex;
    flex-grow: 1;
    padding: 10px;
    

}
.main{
    width: 100vw;
    height: 100vh;
    display: flex;
    flex-grow: 1;
    flex-shrink: 0;
    justify-content: center;
}

.background{
      background-image: url("../images/BingWallpaper1.jpg");
        width: 100%;
        height: 100%;
        position:fixed;
        top: 0;
        left: 0;
        z-index:-10;
        zoom: 1;
        background-color: #fff;
        background-repeat: no-repeat;
        background-size: cover;
        -webkit-background-size: cover;
        -o-background-size: cover;
        background-position: center 0;
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items:center;
  }
</style>