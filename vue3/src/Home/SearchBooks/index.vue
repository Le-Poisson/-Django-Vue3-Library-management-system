<template>
  <div>
    <el-input placeholder="请输入您要搜索的书名/作者" prefix-icon="el-icon-search" @keyup.enter="searchBook" v-model="name">
      <template #prefix>
        <el-icon>
          <Search />
        </el-icon>
      </template>
    </el-input>
    <el-table :data="flag == 0 ? booksList : searchBooks" height="450" style="width: 100%"
      v-loading.fullscreen.lock="loading" element-loading-text="正在处理..." element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)">
      <el-table-column type="expand">
        <template #default="{ row }">
          <el-form label-position="left" class="demo-table-expand">
            <el-form-item label="图书名称：">
              <span>{{ row["title"] }}</span>
            </el-form-item>
            <el-form-item label="图书作者：">
              <span>{{ row["author__name"] }}</span>

            </el-form-item>
            <el-form-item label="总库存：">
              <span>{{ row["amount"] }}</span>
            </el-form-item>
            <el-form-item label="借出数量：">&nbsp;&nbsp; <span>{{ row["lend_amount"] }}</span>
            </el-form-item>
            <el-form-item label="图书介绍：">&nbsp;&nbsp; <span>{{ row["introduction"] }}</span>
            </el-form-item>

            <el-form-item label="管理员操作：" v-if="isAdmin">
              <el-button size="small" type="warning" @click="getBookInfo(row)">修改书籍信息</el-button>
              <el-dialog v-model="editBookInfo" title="请输入修改信息" width="500">
                <el-form>
                  <el-form-item label="图书名称" :label-width="formLabelWidth" style="margin-bottom: 15px;">
                    <el-input v-model="BookName" autocomplete="off" />
                  </el-form-item>
                  <el-form-item label="图书作者" :label-width="formLabelWidth" style="margin-bottom: 15px;">
                    <el-input v-model="BookAuthor" autocomplete="off" />
                  </el-form-item>
                  <el-form-item label="总库存" :label-width="formLabelWidth" style="margin-bottom: 15px;">
                    <el-input v-model="BookAmount" autocomplete="off" />
                  </el-form-item>
                  <el-form-item label="图书介绍" :label-width="formLabelWidth" style="margin-bottom: 15px;">
                    <el-input v-model="BookIntroduction" autocomplete="off" />
                  </el-form-item>
                </el-form>
                <template #footer>
                  <div class="dialog-footer">
                    <el-button @click="editBookInfo = false">取消</el-button>
                    <el-button type="primary" @click="changeBookInfo(row)">
                      确定
                    </el-button>
                  </div>
                </template>
              </el-dialog>
              <el-popconfirm title="确认删除该书籍吗？" style="float: right;" @confirm="delBook(row)">
                <template #reference>
                  <el-button size="small" type="danger">删除书籍</el-button>
                </template>
              </el-popconfirm>
            </el-form-item>
          </el-form>
        </template>
      </el-table-column>
      <el-table-column label="图书名称" sortable prop="title"></el-table-column>
      <el-table-column sortable label="图书作者" prop="author__name"></el-table-column>
      <el-table-column sortable label="总库存" prop="amount"></el-table-column>
      <el-table-column sortable label="借出数量" prop="lend_amount"></el-table-column>
      <el-table-column label="操作" v-if="!isAdmin">
        <template #default="{ row }">
          <el-button size="default" type="primary" plain @click="bookReserve(row)">借阅</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import { mapState } from "vuex";
import axios from 'axios';
import store from '@/store';


export default {
  name: "SearchBooks",
  data() {
    return {
      loading: false,
      name: "",
      flag: 0,
      borrowInfo: {
        borrowDate: "",
        realDate: "",
      },
      searchBooks: [],
      editBookInfo: false,
      BookName: "",
      BookAuthor: "",
      BookAmount: "",
      BookIntroduction: "",
      formLabelWidth: '80px',
      formIntroWidth: '160px',
    };
  },
  methods: {
    async bookReserve(row) {
      console.log('借阅书籍:', row);
      console.log('当前用户 ID:', this.readerId);
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          bookID: row.bookID, // 发送搜索的书名
          userID: this.readerId, // 发送当前用户的 ID
        }, {
          headers: {
            'X-Requested-With': 'Book_Reserve', // 自定义标识
          },
        });

        if (response.data.success) {
          this.$message.success('借阅成功'); // 使用 Element Plus 的消息提示
        } else {
          this.$message.error(response.data.message || '借阅失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('借阅错误:', error);
        this.$message.error('借阅失败，请重试'); // 通用错误处理
      }
    },
    async searchBook(e) {
      this.loading = true;
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          bookName: this.name, // 发送搜索的书名
        }, {
          headers: {
            'X-Requested-With': 'Search', // 自定义标识
          },
        });

        if (response.data.success) {
          this.flag = 1;
          this.searchBooks = response.data.books;
          console.log('搜索结果:', this.searchBooks);
        } else {
          this.$message.error(response.data.message || '搜索失败');
        }
      } catch (error) {
        console.error('搜索错误:', error);
        this.$message.error('搜索失败，请重试');
      } finally {
        this.loading = false;
      }
    },
    async showAllBooks() {
      this.loading = true;
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          bookName: this.name, // 发送搜索的书名
        }, {
          headers: {
            'X-Requested-With': 'Get_All_Books', // 自定义标识
          },
        });

        if (response.data.success) {
          this.searchBooks = response.data.books;
          console.log('数据库中的书籍:', this.searchBooks);

          store.commit('Books/INITBOOKSLIST', this.searchBooks);
          const storedInfo = store.getters['Books/booksList'];

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
    clear() {
      this.flag = 0;
      this.searchBooks = [];
    },
    async changeBookInfo(row) {
      console.log('修改图书信息:', row);
      this.editBookInfo = false
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          bookID: row.bookID, // 发送搜索的书ID
          bookName: this.BookName, // 发送修改后的书名
          bookAuthor: this.BookAuthor, // 发送修改后的作者
          bookAmount: this.BookAmount, // 发送修改后的总库存
          bookIntroduction: this.BookIntroduction, // 发送修改后的简介
        }, {
          headers: {
            'X-Requested-With': 'Change_Book_Info', // 自定义标识
          },
        });
        if (response.data.success) {
          this.searchBooks = response.data.books;
          console.log('数据库中的书籍:', this.searchBooks);

          store.commit('Books/INITBOOKSLIST', this.searchBooks);
          const storedInfo = store.getters['Books/booksList'];

        } else {
          this.$message.error(response.data.message || '修改失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('错误:', error);
        this.$message.error('失败，请重试'); // 通用错误处理
      }
      this.showAllBooks();

    },
    async delBook(row) {
      console.log('删除书籍:', row);
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
          bookID: row.bookID, // 发送搜索的书名
        }, {
          headers: {
            'X-Requested-With': 'Delete_Book', // 自定义标识
          },
        });

        if (response.data.success) {
          this.searchBooks = response.data.books;
          console.log('数据库中的书籍:', this.searchBooks);

          store.commit('Books/INITBOOKSLIST', this.searchBooks);
          const storedInfo = store.getters['Books/booksList'];

        } else {
          this.$message.error(response.data.message || '删除失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('错误:', error);
        this.$message.error('失败，请重试'); // 通用错误处理
      }
    },
    async getBookInfo(row) {
      console.log('获取书籍信息:', row);
      const bookInfo = this.searchBooks.find(item => item.bookID === row.bookID);
      console.log('书籍信息:', bookInfo);
      this.BookName = bookInfo.title;
      this.BookAuthor = bookInfo.author__name;
      this.BookAmount = bookInfo.amount;
      this.BookIntroduction = bookInfo.introduction;
      this.editBookInfo = true;
    }
  },
  computed: {
    ...mapState({
      booksList(state) {
        return state.Books.booksList;
      },
      readerId(state) {
        return state.User.readerInfo.readerId;
      },
      isAdmin(state) {
        return state.User.isAdmin;
      },
    }),
  },
  mounted() {
    // this.showAllBooks();
    this.$nextTick(() => {
      store.commit('Utils/SET_INTRODUCE', false);
      this.showAllBooks(); // 在 DOM 更新后调用
    });
  }
};
</script>

<style lang="less" scoped>
.demo-table-expand {
  font-size: 0;
}

.demo-table-expand label {
  width: 90px;
  color: #99a9bf;
}

.demo-table-expand .el-form-item {
  margin-right: 0;
  margin-bottom: 0;
  width: 50%;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>
