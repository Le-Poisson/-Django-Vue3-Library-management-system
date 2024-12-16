<template>
    <el-table
    :data="readerList"
    style="width: 100%"
    :default-sort = "{prop: 'readerName', order: 'descending'}"
    v-loading.fullscreen.lock="loading"
      element-loading-text="正在处理..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    >
    <el-table-column
      prop="userID"
      label="用户ID"
      sortable
      >
    </el-table-column>
    <el-table-column
      prop="name"
      label="姓名"
      sortable
      >
    </el-table-column>
    <el-table-column
      prop="phoneNum"
      sortable
      label="电话"
      >
    </el-table-column>
    <el-table-column
      prop="borrowTimes"
      sortable
      label="借阅次数"
      >
    </el-table-column>
    <el-table-column
      prop="ovdTimes"
      sortable
      label="逾期次数"
      >
    </el-table-column>
    <el-table-column
      label="操作"
      ><template #default="{ row }">
       <el-popconfirm
          title="确认删除该用户吗？"
          @confirm="delPerson(row)"
        >
        <template #reference>
          <el-button
            size="default"
            type="danger"
            >删除用户</el-button
          >
        </template>
        </el-popconfirm>
      </template>

    </el-table-column>
  </el-table>
</template>

<script>
import {mapState} from 'vuex'
import axios from 'axios';
import store from '@/store';

export default {
    name: 'AdminPerson',
    data() {
        return {
            loading: false,
        };
    },
    computed:{
        ...mapState({
             readerList(state){
                return state.User.readerList
            }
        })
    },
    methods:{
      async delPerson(index,row){
        try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          'userID':index.userID,
        }, {
          headers: {
            'X-Requested-With': 'Delete_User', // 自定义标识
          },
        });

        if (response.data.success) {
          const userList = response.data.userList; // 假设返回的书籍数组在 response.data.books 中
          console.log('用户列表', userList);

          store.commit('User/INIT_READER_LIST', userList);
          // const storedInfo = store.getters['User/readerList'];
          // console.log('用户信息:', storedInfo); // 打印从 store 中获取的信息

        } else {
          this.$message.error(response.data.message || '搜索失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('搜索错误:', error);
        this.$message.error('搜索失败，请重试'); // 通用错误处理
      } finally {
        this.loading = false; // 结束加载状态
      }
      },
      async showAllUsers(){
        this.loading = true; // 开始加载状态
        try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
        
        }, {
          headers: {
            'X-Requested-With': 'Get_All_Users', // 自定义标识
          },
        });

        if (response.data.success) {
          const userList = response.data.userList; // 假设返回的书籍数组在 response.data.books 中
          console.log('用户列表', userList);

          store.commit('User/INIT_READER_LIST', userList);
          // const storedInfo = store.getters['User/readerList'];
          // console.log('用户信息:', storedInfo); // 打印从 store 中获取的信息

        } else {
          this.$message.error(response.data.message || '搜索失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('搜索错误:', error);
        this.$message.error('搜索失败，请重试'); // 通用错误处理
      } finally {
        this.loading = false; // 结束加载状态
      }
      }
    },
    mounted(){
      this.$nextTick(() => {
        store.commit('Utils/SET_INTRODUCE', false);
      this.showAllUsers(); // 在 DOM 更新后调用
  });
    }
};
</script>

<style lang="less" scoped>

</style>