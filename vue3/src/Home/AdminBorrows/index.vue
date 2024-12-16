<template>
  <div
    v-loading.fullscreen.lock="loading"
    :element-loading-text="loadingtext"
    element-loading-spinner="el-icon-loading"
    element-loading-background="rgba(0, 0, 0, 0.8)"
  >
    <el-input
      placeholder="请输入您要查找的用户姓名/图书名称"
      prefix-icon="el-icon-search"
      @keyup.enter.native="searchInfo"
      v-model="info"
    >
    </el-input>
    <el-table
      :data="flag == 0 ? borrowsList : searchMessage"
      style="width: 100%"
      :default-sort="{ prop: 'date', order: 'descending' }"
    >
      <el-table-column type="expand">
        <template #default="{ row }">
          <el-form label-position="left" class="demo-table-expand">
            <el-form-item label="借阅日期：">
              <span>{{ row['startTime'] }}</span>
            </el-form-item>
            <el-form-item label="应还日期"
              >&nbsp;
              <span>{{ row['DDL'] }}</span>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <!-- <el-table-column label="借阅日期" sortable prop="borrowDate">
        <template slot-scope="scope">
          <el-icon><Timer /></el-icon>
          <span style="margin-left: 10px">{{ scope.row.borrowDate }}</span>
        </template>
      </el-table-column>
      <el-table-column label="图书名称" sortable prop="bookID__title">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>编号: {{ scope.row.bookId }}</p>
            <p>名称: {{ scope.row.bookName }}</p>
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">{{ scope.row.bookName }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="读者姓名" sortable prop="userID__name">
        <template slot-scope="scope">
          <el-popover trigger="hover" placement="top">
            <p>编号: {{ scope.row.readerId }}</p>
            <p>姓名: {{ scope.row.readerName }}</p>
            <div slot="reference" class="name-wrapper">
              <el-tag size="medium">{{ scope.row.readerName }}</el-tag>
            </div>
          </el-popover>
        </template>
      </el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button
            size="default"
            type="danger"
            @click="handleDelete(row)"
            >删除记录</el-button
          >
        </template>
      </el-table-column> -->
      <el-table-column label="借阅编号" sortable prop="reserveID"></el-table-column>
      <el-table-column sortable label="借阅用户" prop="userID__name"></el-table-column>
      <el-table-column sortable label="借阅书籍" prop="bookID__title"></el-table-column>
      <el-table-column label="操作">
        <template #default="{ row }">
          <el-button
            size="default"
            type="primary"
            plain
            @click="sendMessage(row)"
            >提醒还书</el-button
          >
        </template>
      </el-table-column>
      
    </el-table>
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from 'axios';
import store from '@/store'; // 确保路径正确

export default {
  name: "AdminBorrows",
  data() {
    return {
      loading: false,
      loadingtext: "查询中...",
      info: "",
      searchMessage: [],
      flag: 0,
    };
  },
  computed: {
    ...mapState({
      borrowsList(state) {
        return state.Borrows.borrowsList;
      },
    }),
  },
  methods: {
    handleDelete(index, row) {
    },
    async searchInfo(e) {
      this.loading = true;
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          info: this.info,
        }, {
          headers: {
            'X-Requested-With': 'Search_Reserve', // 自定义标识
          },
        });
        if (response.data.success) {
          this.flag = 1;
          this.searchMessage = response.data.reserves
          console.log(this.searchMessage)
        } else {
          this.$message.error(response.data.message || '搜索失败');
        }
        } catch (error) {
        console.error('搜索错误:', error);
        this.$message.error('搜索失败，请重试'); // 通用错误处理
      } finally {
        this.loading = false; // 结束加载状态
      }
    },
    async showAllReserves(){
      this.loading = true;
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {

        }, {
          headers: {
            'X-Requested-With': 'Get_All_Reserves', // 自定义标识
        },
        });
        if (response.data.success) {
          this.searchMessage = response.data.reserves
          store.commit('Borrows/INITBORROWSLIST', response.data.reserves)
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
    clear() {
      this.flag = 0;
      this.searchMessage = [];
    },
    alertPerson(row) {
      
    },
    async sendMessage(row) {
      console.log(row)
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          sender: this.$store.state.User.adminInfo.adminID,
          receiver: row.userID__name,
          reserveID: row.reserveID,
          content: `您好，您的《${row.bookID__title}》借阅即将到期，请及时归还。`
        }, {
          headers: {
            'X-Requested-With': 'Send_Message', // 自定义标识
          },
        });
        if (response.data.success) {
          this.$message.success('发送成功');
        } else {
          this.$message.error(response.data.message || '发送失败');
        }
      } catch (error) {
        console.error('发送错误:', error);
        this.$message.error('发送失败，请重试'); // 通用错误处理
      }
    }
  },
  mounted(){
    this.$nextTick(() => {
      store.commit('Utils/SET_INTRODUCE', false);
      this.showAllReserves(); // 在 DOM 更新后调用
  });
  }
};
</script>

<style lang="less" scoped>
</style>