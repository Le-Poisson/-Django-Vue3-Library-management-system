<template>
  <div class="main">
      <el-menu
          default-active="1"
          class="el-menu-vertical-demo"
          :collapse="isCollapse"
          @mouseenter="handleMouseEnter"
          @mouseleave="handleMouseLeave"
          active-text-color="#ffd04b">
          <el-menu-item index="1" @click="$router.push('/home/introduce')"> 
              <el-icon><HomeFilled /></el-icon>
              <span>首页</span>
          </el-menu-item>
          <el-menu-item index="2" @click="handleSearch">
              <el-icon><Search /></el-icon>
              <span>查询图书</span>
          </el-menu-item>
          <el-menu-item index="4" @click="$router.push('/home/readerborrows')">
              <el-icon><DocumentCopy /></el-icon>
              <span>借阅记录</span>
          </el-menu-item>
          <el-menu-item index="5" @click="$router.push('/home/ReaderMessage')">
            <el-icon><Message /></el-icon>
              <span>系统消息</span>
          </el-menu-item>
          <el-sub-menu index="7">
              <template #title>
                  <el-icon><Setting /></el-icon>
                  <span>设置</span>
              </template>
              <el-menu-item index="1-1" @click="toggleUser">
                  <el-icon><SwitchButton /></el-icon>
                  <span>退出账号</span>
              </el-menu-item>
          </el-sub-menu>
      </el-menu>
  </div>
</template>

<script>
import { mapState } from 'vuex';
import { ElMenu, ElSubMenu, ElMenuItem } from 'element-plus';

export default {
  name: "ReaderBanner",
  components: {
      ElMenu,
      ElSubMenu,
      ElMenuItem
  },
  data() {
      return {
          isCollapse: true
      };
  },
  computed: {
      ...mapState({
          readerId(state) {
              return state.User.readerInfo.readerId;
          }
      })
  },
  methods: {
      handleMouseEnter() {
          this.isCollapse = false; // 鼠标进入时展开
      },
      handleMouseLeave() {
          this.isCollapse = true; // 鼠标离开时收起
      },
      toggleUser() {
          this.$router.push("/login");
      },
      handleSearch() {
          this.$router.push('/home/search');
      }
  }
};
</script>

<style lang="less" scoped>
.main {
  float: left;
  margin-right: 200px;
}

.el-menu-vertical-demo {
  background-color: rgba(230, 230, 250, 0.5); /* 浅紫色，带透明度 */
  backdrop-filter: blur(10px); /* 毛玻璃效果 */
  border-radius: 20px; /* 圆角 */
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}
</style>