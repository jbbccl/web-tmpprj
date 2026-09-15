<template>
    <div class="exp">
        <div class="list">
            <div class="l_item"></div>
            <div class="l_item"></div>
            <div class="l_item"></div>
            <div class="l_item"></div>
            <div class="l_item"></div>
        </div>
        <div class="block">
            <div class="b_item">
                <img src="http://192.168.86.137:5173/api/home/toor/pic.jpg">
            </div>
            <div class="b_item">
                <object data="movie.mp4" width="320" height="240"></object>
            </div>
        </div>
        
        
    </div>

</template>
<script>
export default{
    data(){
        return {
            src_url:''

        }
    },
    created:function(){
        this.src_url = window.location.hostname
    },
    methods:{

    }

}
</script>

<style>
.exp{
    Flex-wrap:wrap;
    border: 1px solid #ffe4c1;
    margin: auto;
    border-radius: 10px;
    text-align: center;
    position: fixed;
    left:14vw;
    top:14vh;
  line-height: 1%;
  color: #d8c97583;
  background-color: #2e2e2e67;
  backdrop-filter: blur(2px);
  display: flex;
  width: 70%;
  min-height:80%;
}
.list{
    margin: auto;
    position: fixed;
    left:2%;
    top:3%;
    width: 33vw;
    height: 50vh;
    /* background-color: rgb(95, 95, 95); */
}
.l_item{
    display: flex;
    background-color: rgba(236, 236, 236, 0.329);
    width: 80%;
    height: 10%;
    display: inline-block;/* 流式 */
    margin:3%;
    border-radius: 12px;
    border: 2px solid #fdc883;
    padding: 5px;
}
.block{
    margin: auto;
    position: fixed;
    left:50%;
    top:3%;
    width: 33vw;
    height: 50vh;
    /* background-color: rgb(95, 95, 95); */
}
.b_item{
    display: flex;
    background-color: rgba(236, 236, 236, 0.329);
    width: 80%;
    height: 35.7%;
    display: inline-block;/* 流式 */
    margin:4%;
    border-radius: 12px;
    border: 2px solid #fdc883;
    padding: 5px;
}
</style>