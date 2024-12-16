<template>
  <el-table
    :data="borrows"
    style="width: 100%"
    height="450"
    v-loading.fullscreen.lock="loading"
    element-loading-text="正在处理..."
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)"
  >
    
    <el-table-column prop="bookID__title" label="书籍名称" sortable></el-table-column>
    <el-table-column prop="startTime" label="借阅日期" sortable></el-table-column>
    <el-table-column prop="DDL" label="应还日期" sortable></el-table-column>
    
    <el-table-column label="操作" width="200">
      <template #default="{ row }">
          <el-button
            size="default"
            type="primary"
            plain
            style="margin-right: 10px"
            slot="reference"
            @click="returnBook(row)"
          >
            还书
          </el-button>
          <el-button
            size="default"
            type="success"
            :disabled="row.status === '续借'"
            slot="reference"
            @click="continueBorrowBook(row)"
          >
            续借
          </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
import { mapState } from "vuex";
import axios from 'axios';
import store from '@/store'; // 确保路径正确

export default {
  name: "ReaderBorrow",
  data() {
    return {
      loading: false,
    };
  },
  methods: {
    // 还书
    async returnBook(row) {
      console.log(row);
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          reserveID : row.reserveID,
        }, {
          headers: {
            'X-Requested-With': 'Return_Book',
          },
        });
        if (response.data.success) {
          this.$message.success('还书成功');
          this.showBorrows(); // 更新借阅信息
        } else {
          this.$message.error(response.data.message || '还书失败');
        }
      } catch (error) {
        console.error('还书错误:', error);
        this.$message.error('还书失败，请重试'); // 通用错误处理
      }
    },
    // 续借
    async continueBorrowBook(row) {
      console.log(row);
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          reserveID : row.reserveID,
        }, {
          headers: {
            'X-Requested-With': 'Continue_Borrow_Book',
          },
        });
        if (response.data.success) {
          this.$message.success('续借成功');
          this.showBorrows(); // 更新借阅信息
        } else {
          this.$message.error(response.data.message || '续借失败');
        }
      } catch (error) {
        console.error('续借错误:', error);
        this.$message.error('续借失败，请重试'); // 通用错误处理
      }
    },
    async showBorrows() {
      this.loading = true;
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          userID : this.readerId,
        }, {
          headers: {
            'X-Requested-With': 'Get_Borrows',
          },
        });
        if (response.data.success) {
          console.log('该用户的借阅信息', response.data.borrows);
          store.commit('Borrows/INITBORROWS', response.data.borrows);
        } else {
          this.$message.error(response.data.message || '获取失败');
        }
      } catch (error) {
        console.error('获取错误:', error);
        this.$message.error('获取失败，请重试'); // 通用错误处理
      } finally {
        this.loading = false; // 结束加载状态
      }
  },
  },
  computed: {
    ...mapState({
      borrows(state) {
        return state.Borrows.borrows;
      },
      readerId(state) {
        return state.User.readerInfo.readerId;
      },
    }),
  },
  mounted() {
    this.$nextTick(() => {
      store.commit('Utils/SET_INTRODUCE', false);
      this.showBorrows(); // 在 DOM 更新后调用
  });
  },
};
</script>

<style lang="less" scoped>
</style>