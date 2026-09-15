<template>

<div id="main">
    <div id="bord">
        <iframe class="iframe" id="bi_iframe" :onload="adjustIframe" :src="vid_src"
        frameborder="0" scrolling="auto"></iframe>
    </div>
</div>

</template>

<script>
export default{
    data(){
        return {
            ifmwidth:0,
            ifmhight:0,
            vid_src:"/api/home/video/3"

        }
    },
    created() {
        //this.ruleForm.name='1111';
    },
    methods:{
        get_which_vid(){
            console.log('1222222222222222')
            let e=document.getElementById('bi_iframe');
            e.src="/api/home/video/3" 
        },
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
        }
    }
}

</script>
<style>
.iframe{
    display: flex;
    width: v-bind(ifmwidth+'vw');
    height:v-bind(ifmhight+'vh');
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
#bord{
    background-color: rgba(0, 0, 0, 0.575);
}
</style>