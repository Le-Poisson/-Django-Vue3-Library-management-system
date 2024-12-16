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

    },
        async deleteMessage(row) {

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
    });
    },

  };
  </script>
  
  <style lang="less" scoped>
  </style>