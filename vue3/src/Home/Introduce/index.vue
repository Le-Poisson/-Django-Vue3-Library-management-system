<template>
    <div class="content-container">
 <el-descriptions 
 title="用户信息" 
 :column="3" 
 border>
    <el-descriptions-item label="管理员ID" 
    v-if="isAdmin" 
    label-class-name="my-label"
    class-name="my-content"
    >
    {{adminInfo.adminID}}
  </el-descriptions-item>
    <el-descriptions-item label="用户ID" v-if="!isAdmin" label-class-name="my-label"
    class-name="my-content">{{readerInfo.readerId}}</el-descriptions-item>
    <el-descriptions-item label="管理员" v-if="isAdmin" label-class-name="my-label"
    class-name="my-content">{{adminInfo.adminName}}</el-descriptions-item>
    <el-descriptions-item label="用户名" v-else label-class-name="my-label"
    class-name="my-content">{{readerInfo.readerName}}</el-descriptions-item>
    <el-descriptions-item label="手机号" v-if="!isAdmin" label-class-name="my-label"
    class-name="my-content">{{readerInfo.readerPhone}}</el-descriptions-item>
     <el-descriptions-item label="备注" v-if="isAdmin"label-class-name="my-label"
     class-name="my-content">
      <el-tag size="small">管理员</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="备注" v-else label-class-name="my-label"
    class-name="my-content">
      <el-tag size="small">学生用户</el-tag>
    </el-descriptions-item>
    <el-descriptions-item label="借书次数" v-if="!isAdmin" label-class-name="my-label"
    class-name="my-content">{{readerInfo.borrowTimes}}</el-descriptions-item>
    <el-descriptions-item label="逾期次数" v-if="!isAdmin" label-class-name="my-label"
    class-name="my-content">{{readerInfo.ovdTimes}}</el-descriptions-item>
</el-descriptions>
<div class="carousel-container">
    <h3 class="mini_title">今日格言</h3>
<el-carousel v-if="RandomFiveQuotes.length > 0" :interval="4000" type="card" height="200px">
    <el-carousel-item v-for="quote in RandomFiveQuotes" :key="quote.quotationID">
        <div class="quote-content">
        <h3 class="quote-text">{{ quote.quotation }}</h3>
            <p>—— {{ quote.author__name }}</p>
        </div>
    </el-carousel-item>
  </el-carousel>
</div>
</div>
</template>

<script>
import axios from 'axios';
import {mapState} from 'vuex'
import store from '@/store'; // 确保路径正确

export default {
    name: 'Introduce',
    data() {
        return {
            QuotesList: [],
            RandomFiveQuotes: [],
            loading: false,
        }
    },
    methods: {
        async getallQuotes() {
        this.loading = true;
        try {
            const response = await axios.post('http://127.0.0.1:8000/library/post/', {

            }, {
              headers: {
                'X-Requested-With': 'Get_Quotations', // 自定义标识
              },
            });
            if (response.data.success) {
              this.QuotesList = response.data.quotations;
              this.getRandomFiveQuotes();
              } else {
              this.$message.error(response.data.message || '获取失败'); // 使用 Element Plus 的消息提示
              }
        } catch (error) {
            console.error('获取错误:', error);
            this.$message.error('获取失败，请重试'); // 通用错误处理
        } finally {
            this.loading = false;
        }
        },
        getRandomFiveQuotes() {
            // 清空 RandomFiveQuotes
            this.RandomFiveQuotes = [];
            
            // 创建一个副本以避免修改原始数组
            const quotesCopy = [...this.QuotesList];
            
            // 随机选择 5 个元素
            for (let i = 0; i < 5; i++) {
                // 检查是否还有可以选择的元素
                if (quotesCopy.length === 0) break;
                
                // 生成随机索引
                const randomIndex = Math.floor(Math.random() * quotesCopy.length);
                // 将选中的元素添加到 RandomFiveQuotes 中
                this.RandomFiveQuotes.push(quotesCopy[randomIndex]);
                // 从副本中移除已选择的元素
                quotesCopy.splice(randomIndex, 1);
        }
        console.log(this.RandomFiveQuotes);
        }
    },
    computed:{
        ...mapState({
            isAdmin(state){
                return state.User.isAdmin
            },
            adminInfo(state){
                if(this.isAdmin){
                    return state.User.adminInfo
                }else return ''
            },
            readerInfo(state){
                if(!this.isAdmin)
                return state.User.readerInfo
                else 
                return {}
            },
            isIntroduce(state){
                return state.Utils.isIntroduce
            }
        })
    },
   mounted(){
    this.$nextTick(() => {
      store.commit('Utils/SET_INTRODUCE', true);
      this.getallQuotes(); // 在 DOM 更新后调用
  });
   }
};
</script>

<style lang="less" scoped>

@import '@/assets/font/index.css';
.el-carousel__item h3 {
  color: #475669;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
  text-align: center;
}

.el-carousel__item{
  background-image: url('@/assets/card.png'); /* 替换为你的背景图片路径 */
  background-size: cover; /* 背景覆盖 */
  background-position: center; /* 背景居中 */
  height: 200px; /* 确保高度与 carousel 的高度一致 */
  display: flex; /* 使内容居中 */
  align-items: center; /* 垂直居中 */
  justify-content: center; /* 水平居中 */
}


.descriptions {
    background: rgba(255, 255, 255, 0.5); /* 半透明白色背景 */
    backdrop-filter: blur(10px); /* 毛玻璃效果 */
    border-radius: 10px; /* 圆角效果 */
    padding: 20px; /* 内边距 */
}

:deep(.my-label) {
  background: rgba(224, 176, 255, 0.5)!important;
}
:deep(.my-content) {
  background: rgba(135, 206, 250, 0.3) ;
}
:deep(.title){
  font-size: 40px;
}

:deep(.el-descriptions__title) {
  font-size: 30px; /* 设置字体大小，可以根据需要调整 */
  font-weight: bold; /* 可选：设置字体加粗 */
  font-family: 'DaoLiTi', serif;
  text-align: center; /* 标题居中 */
    background: linear-gradient(90deg, white, lightpink); /* 从白色到浅粉色的渐变 */
    background-clip: text; /* 标准属性 */
    -webkit-background-clip: text; /* 兼容 Chrome 和 Safari */
    -webkit-text-fill-color: transparent; /* 使文本填充为透明，以显示背景 */
    color: transparent; /* 确保兼容性 */
}

.mini_title{
  font-size: 36px; /* 设置字体大小，可以根据需要调整 */
  font-weight: bold; /* 可选：设置字体加粗 */
  font-family: "华文彩云"; /* 设置字体为华为彩云 */
  text-align: center; /* 标题居中 */
  background: linear-gradient(90deg, rgb(255, 195, 121), white);
    background-clip: text; /* 标准属性 */
    -webkit-background-clip: text; /* 兼容 Chrome 和 Safari */
    -webkit-text-fill-color: transparent; /* 使文本填充为透明，以显示背景 */
    color: transparent; /* 确保兼容性 */
}

.content-container {
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* 使内容区域占满剩余空间 */
  height: calc(100vh - 240px); /* 调整为适应父组件的高度，减去header高度 */
}

.carousel-container {
  margin-top: auto; /* 将轮播图推到底部 */
  text-align: center;
}

.quote-content {
  height: 100%; /* 确保内容填满整个容器 */
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中 */
  text-align: center; /* 文本居中 */
}

.quote-text {
  display: -webkit-box; /* 用于设置弹性盒子模型 */
  -webkit-box-orient: vertical; /* 设置主轴为垂直方向 */
  overflow: hidden; /* 隐藏溢出内容 */
  text-overflow: ellipsis; /* 使用省略号表示溢出 */
  
  /* 定义最大行数 */
  -webkit-line-clamp: 3; /* 支持的行数 */
  line-clamp: 3; /* 标准属性，可能不被所有浏览器支持 */
  white-space: normal; /* 允许换行 */
  word-wrap: break-word; /* 兼容老版浏览器 */
}
</style>