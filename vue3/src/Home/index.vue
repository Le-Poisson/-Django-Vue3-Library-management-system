<template>
    <div class="clearfix background">
        <header>
            <img src="../assets/logo2.png" alt="">
        </header>
        
        <el-row :gutter="20">
            <el-col :span="6">
                    <AdminBanner v-if="isAdmin"/>
                    <ReaderBanner v-else/>
            </el-col>
            <el-col :span="14">
                <div :class="['tablemain', { 'blur-effect': isIntroduce }]">
                    <router-view />
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>

import {mapState} from 'vuex'
import ReaderBanner from '@/components/ReaderBanner'
import AdminBanner from '@/components/AdminBanner'

export default {
    name: 'Home',
    data() {
        return {
            
        };
    },
    components: {
        ReaderBanner,
        AdminBanner,
    },
    computed:{
        ...mapState({
           isAdmin(state){
               return state.User.isAdmin
           },
           userName(state){
               if(this.isAdmin){
                   return state.User.adminName
               }else{
                   return state.User.readerName
               }
           },
           readerId(state){
               return state.User.readerInfo.readerId
           },
           isIntroduce(state){
                return state.Utils.isIntroduce
            }
        })
    },
   
};
</script>

<style lang="less" scoped>
header{
    text-align: center;
    color: rgb(16, 148, 93);
    font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
    img{
        height: 120px;
    }
}
.tablemain{
     box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
     border: 1px solid #eee;
     border-radius: 30px 30px 30px ;
     padding: 20px;
     min-height:450px;
     min-width: 800px;
     
     margin-left: -100px;
}

.blur-effect {
    background: rgba(255, 255, 255, 0.5); /* 半透明背景 */
    backdrop-filter: blur(10px); /* 毛玻璃效果 */
}

/* 如果不需要毛玻璃效果，可以设置背景不透明 */
.tablemain:not(.blur-effect) {
    backdrop-filter: none;
    background: white;
}


.main-content {
    background-color: #e0f7fa;  /* 浅蓝色背景 */
    min-height: calc(100vh - 120px); /* 使内容区域占满剩余高度 */
    display: flex;
    justify-content: center;  /* 水平居中 */
    align-items: center;      /* 垂直居中 */
}
.background {
    background-image: url('@/assets/background/1.jpg'); /* 替换为你的背景图片路径 */
    background-size: cover; /* 填充整个背景 */
    background-position: center; /* 居中显示 */
    height: 100vh; /* 使背景占满整个视口高度 */
}
</style>