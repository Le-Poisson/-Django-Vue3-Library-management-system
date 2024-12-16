<template>
	<h3 class="my-form-title">
          语录管理
    </h3>
    <el-form ref="form" label-width="80px">
  <el-form-item label="语录内容" label-width="80px">
	<el-col :span="24">
    	<el-input v-model="QuotesContent"></el-input>
	  </el-col>
  </el-form-item>
  <el-form-item label="语录作者" label-width="80px">
	<el-col :span="12">
    	<el-input v-model="autohor"></el-input>
	  </el-col>
      <el-button type="primary" @click="addQuotes">立即添加</el-button>
  </el-form-item>
  <el-form-item label="搜索语录" label-width="80px">
	<el-col :span="20">
    	<el-input 
        placeholder="请输入您要搜索的语录/作者"
        v-model="searchQuotesInfo">
    </el-input>
	  </el-col>
      <el-button type="primary" @click="searchQuotes">搜索</el-button>
  </el-form-item>
    </el-form>
    <el-table 
    :data="QuotesList" 
    style="width: 100%"
    height="250"
    v-loading.fullscreen.lock="loading"
      element-loading-text="正在处理..."
      element-loading-spinner="el-icon-loading"
      element-loading-background="rgba(0, 0, 0, 0.8)"
    >
      <el-table-column prop="quotation" label="语录内容"  width="520"/>
      <el-table-column prop="author__name" label="语录作者"  width="100"/>
      <el-table-column label="操作"  width="160">
        <template #default="{row}">
            <el-button 
          @click="editQuote(row)"
          type="warning"
          size="default"
          >修改
        </el-button>

<el-dialog v-model="isEdit" title="请输入修改信息" width="500" >
    <el-form>
      <el-form-item label="语录内容" :label-width="formLabelWidth" style="margin-bottom: 15px;">
        <el-input v-model="editQuoteContent" autocomplete="off" />
      </el-form-item>
      <el-form-item label="语录作者" :label-width="formLabelWidth" style="margin-bottom: 15px;">
        <el-input v-model="editAuthorName" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="isEdit = false">取消</el-button>
        <el-button type="primary" @click="changeQuoteInfo(row)">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>

          <el-button 
          @click="deleteQuote(row)"
          type="danger"
          size="default"
          >删除
        </el-button>
        </template>
      </el-table-column>
    </el-table>

</template>

<script>
import { mapState } from "vuex";
import axios from 'axios';
import store from '@/store';

export default {
  name: "AddQuotations",
  data() {
    return {
        QuotesContent: "",
        autohor: "",
        searchQuotesInfo: "",
        QuotesList: [],
        isEdit: false,
        editQuoteID: "",
        editQuoteContent: "",
        editAuthorName: "",
        loading: false,
        formLabelWidth: '80px',
    };
  },
  methods: {
    async showallQuotes() {
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
    async addQuotes() {
        try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
              Quote: this.QuotesContent,
              Author: this.autohor,
        }, {
          headers: {
            'X-Requested-With': 'AddQuotations', // 自定义标识
          },
        });

        if (response.data.success) {
          this.$message.success('添加成功'); // 使用 Element Plus 的消息提示
        } else {
          this.$message.error(response.data.message || '添加失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('添加错误:', error);
        this.$message.error('添加失败，请重试'); // 通用错误处理
      }
      this.clear()
      this.showallQuotes()
    },
    async deleteQuote(row) {
        try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
            quotationID: row.quotationID
        }, {
          headers: {
            'X-Requested-With': 'Delete_Quotation', // 自定义标识
          },
        });

        if (response.data.success) {
          this.$message.success('删除成功'); // 使用 Element Plus 的消息提示
        } else {
          this.$message.error(response.data.message || '删除失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('删除错误:', error);
        this.$message.error('删除失败，请重试'); // 通用错误处理
      }
      this.showallQuotes()
    },
    async searchQuotes() {
      try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
            searchInfo: this.searchQuotesInfo
        }, {
          headers: {
            'X-Requested-With': 'Search_Quotations', // 自定义标识
          },
        });

        if (response.data.success) {
          this.QuotesList = response.data.quotations;
        } else {
          this.$message.error(response.data.message || '搜索失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('搜索错误:', error);
        this.$message.error('搜索失败，请重试'); // 通用错误处理
      }
    },
    async editQuote(row) {
        this.isEdit = true;
        this.editQuoteID = row.quotationID;
        this.editQuoteContent = row.quotation;
        this.editAuthorName = row.author__name;
        console.log(row)
    },
    async changeQuoteInfo(row) {
        try {
        const response = await axios.post('http://127.0.0.1:8000/library/post/', {
            quotationID: this.editQuoteID,
            quote: this.editQuoteContent,
            author_name: this.editAuthorName,
        }, {
          headers: {
            'X-Requested-With': 'Edit_Quotation', // 自定义标识
          },
        });

        if (response.data.success) {
          this.$message.success('修改成功'); // 使用 Element Plus 的消息提示
        } else {
          this.$message.error(response.data.message || '修改失败'); // 使用 Element Plus 的消息提示
        }
      } catch (error) {
        console.error('修改错误:', error);
        this.$message.error('修改失败，请重试'); // 通用错误处理
      }
      this.isEdit = false;
      this.showallQuotes()
    },
    clear(){
        this.QuotesContent = "";
        this.autohor = "";
        this.searchQuotes = "";
    },
  },
  mounted() {
    // this.showAllBooks();
    this.$nextTick(() => {
      store.commit('Utils/SET_INTRODUCE', false);
      this.showallQuotes(); // 在 DOM 更新后调用
  });
  }
}

</script>

<style lang="less" scoped>

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
.my-form-title {
  margin-top: 0px;
  margin-bottom: 20px;
    font-size: 42px; /* 标题大小 */
    text-align: center; /* 标题居中 */
    background: linear-gradient(10deg, blue, white);
    background-clip: text; /* 标准属性 */
    -webkit-background-clip: text; /* 兼容 Chrome 和 Safari */
    -webkit-text-fill-color: transparent; /* 使文本填充为透明，以显示背景 */
    color: transparent; /* 确保兼容性 */
    font-family: 'DaoLiTi', serif;
}

</style>