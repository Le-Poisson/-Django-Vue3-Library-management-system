<template>
    <el-table
      :data="messageList"
      style="width: 100%"
      height="450"
      v-loading.fullscreen.lock="loading"
      element-loading-text="正在处理..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    >
      
      <el-table-column prop="content" label="系统消息" sortable></el-table-column>
      <el-table-column prop="time" label="时间" width="200" sortable></el-table-column>
      
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
            <el-button
              size="default"
              type="danger"
              slot="reference"
              @click="deleteMessage(row)"
            >
              删除
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
        messageList: [],
      };
    },
    methods: {
      async showMessage() {
        this.loading = true;
        try {
          const response = await axios.post('http://127.0.0.1:8000/library/post/', {
            userID : this.readerId,
          }, {
            headers: {
              'X-Requested-With': 'Get_Messages',
            },
          });
          if (response.data.success) {
            this.messageList = response.data.messages;
            
            console.log(this.messageList);
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
        async deleteMessage(row) {
            try{
                const response = await axios.post('http://127.0.0.1:8000/library/post/', {
                    messageID: row.messageID,
          }, {
            headers: {
              'X-Requested-With': 'Delete_Message',
            },
          });
          if (response.data.success) {
            this.$message.success('删除成功');
            this.messageList = this.messageList.filter(item => item.messageID !== row.messageID);
          } else {
            this.$message.error(response.data.message || '删除失败');
          }
        } catch (error) {
          console.error('删除错误:', error);
          this.$message.error('删除失败，请重试'); // 通用错误处理
          }
            }
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
        this.showMessage(); // 在 DOM 更新后调用
    });
    },

  };
  </script>
  
  <style lang="less" scoped>
  </style>