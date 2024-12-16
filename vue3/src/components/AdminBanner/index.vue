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
          <el-menu-item index="2" @click="$router.push('/home/person')">
              <el-icon><UserFilled /></el-icon>
              <span slot="title">人员管理</span>
          </el-menu-item>
          <el-menu-item index="3" @click="$router.push('/home/search')">
              <el-icon><Notebook /></el-icon>
              <span slot="title">图书管理</span>
          </el-menu-item>
          <el-menu-item index="4" @click="$router.push('/home/adminborrows')">
              <el-icon><Promotion /></el-icon>
              <span slot="title">借阅记录</span>
          </el-menu-item>
          <el-menu-item index="5" @click="$router.push('/home/adminmessage')">
              <el-icon><Message /></el-icon>
              <span slot="title">系统消息</span>
          </el-menu-item>
          <el-menu-item index="7" @click="$router.push('/home/adminaddbooks')">
              <el-icon><DocumentCopy /></el-icon>
              <span slot="title">添加图书</span>
          </el-menu-item>
          <el-menu-item index="8-1" @click="handleMenuClick('/home/adminaddquotations')">
                  <el-icon><Fold /></el-icon>
                  <span>语录</span>
              </el-menu-item>
          <el-sub-menu index="8">
              <template #title>
                  <el-icon><Setting /></el-icon>
                  <span>设置</span>
              </template>
              <el-menu-item index="8-2" class="el-menu-vertical-demo" @click="toggleUser">
                  <el-icon><SwitchButton /></el-icon>
                  <span slot="title">退出账号</span>
              </el-menu-item>
          </el-sub-menu>
      </el-menu>
  </div>
</template>

<script>
import { ElMenu, ElMenuItem, ElSubMenu } from 'element-plus';

export default {
  name: "AdminBanner",
  components: {
      ElMenu,
      ElMenuItem,
      ElSubMenu,
  },
  data() {
      return {
          isCollapse: true // 初始状态为收起
      };
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
      handleMenuClick(route) {
          this.$router.push(route);
          this.$nextTick(() => {
              const firstFocusableElement = this.$el.querySelector('input, button, [tabindex]');
              if (firstFocusableElement) {
                  firstFocusableElement.focus();
              }
          });
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