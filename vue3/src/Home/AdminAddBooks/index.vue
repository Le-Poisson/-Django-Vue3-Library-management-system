<template>
	<h2 class="my-form-title">
          {{ isAddBooks === true ? '添加书籍' : '添加作者' }}
        </h2>
	<el-form v-if="isAddBooks===true" ref="form" label-width="80px">
  <el-form-item label="书籍名称" label-width="80px">
	<el-col :span="12">
    	<el-input v-model="bookName"></el-input>
	  </el-col>
  </el-form-item>
  <el-form-item label="书籍作者" label-width="80px">
	  <el-col :span="6">
    	<el-input v-model="author"></el-input>
	  </el-col>
  </el-form-item>
  <el-form-item label="总库存" label-width="80px">
	    <el-col :span="6">
    		<el-input v-model="amount" min="0" type="number"></el-input>
	  </el-col>
  </el-form-item>
  <el-form-item label="图书简介" label-width="80px">
	  <el-col :span="12">
		<el-input v-model="introduce"></el-input>
	  </el-col>	  
	 </el-form-item>  
	 <el-form-item>
	  <el-col :span="6">
    <el-button type="primary" @click="addBook">立即添加</el-button>
	  </el-col>		
	  <el-col :span="6">
    <el-button type="info" @click="swithmode">去添加作者</el-button>
	  </el-col> 
  </el-form-item>
</el-form>
<el-form v-if="isAddBooks===false" ref="form" label-width="80px">
	<el-form-item label="作者名称" label-width="80px">
		<el-col :span="8">
			<el-input v-model="newAuthor"></el-input>
		</el-col>
	</el-form-item>
	<el-form-item label="作者简介" label-width="80px">
		<el-col :span="12">
			<el-input v-model="authotIntroduce"></el-input>
		</el-col>
	</el-form-item>
	<el-form-item>
	  <el-col :span="6">
    <el-button type="primary" @click="addAuthor">立即添加</el-button>
	  </el-col>		
	  <el-col :span="6">
    <el-button type="info" @click="swithmode">去添加图书</el-button>
	  </el-col> 
  </el-form-item>
</el-form>
</template>

<script>
import { mapState } from "vuex";
import axios from 'axios'
import { useStore } from 'vuex';
import store from '@/store';

export default {
	name: 'AdminAddBooks',

  data() {
      return {
		bookName: '',
		author:'',
		amount:'',
        introduce: '',
		isAddBooks: true,
		newAuthor: '',
		authotIntroduce: ''
      }
    },
 computed: {
    ...mapState({
      booksList(state) {
        return state.Books.booksList;
      }
     
    })
  },
	 methods: {
		clear() {
			this.bookName = '';
			this.author = '';
			this.amount = '';
			this.introduce = '';
			this.newAuthor = '';
			this.authotIntroduce = '';
		},
      querySearch(queryString, cb) {
        cb(this.booksList);
      },
      handleSelect(item) {
		// console.log(item);
		this.position = item.position
	  },
	  async addBook(){
		  console.log('添加书籍', this.bookName, this.author, this.amount, this.introduce);
		  try{
			const response = await axios.post('http://127.0.0.1:8000/library/post/', {
				title: this.bookName,
				author: this.author,
				amount: this.amount,
				introduce: this.introduce
			}, {
				headers: {
					'X-Requested-With': 'Add_Book', // 自定义标识
         		 },
		  	});
			  if (response.data.success) {
			this.$message.success('添加成功'); // 使用 Element Plus 的消息提示
			} else {
			this.$message.error(response.data.message || '添加失败'); // 使用 Element Plus 的消息提示
			}
			} catch (error) {
			console.error('错误:', error);
			this.$message.error('添加失败，请重试'); // 通用错误处理
      		} 
		  this.clear();
		  },
	  swithmode(){
		this.isAddBooks = !this.isAddBooks
		console.log(this.isAddBooks);
	  },
	  async addAuthor(){
		console.log('添加作者', this.newAuthor, this.authotIntroduce);
		try{
			const response = await axios.post('http://127.0.0.1:8000/library/post/', {
				name: this.newAuthor,
				introduction: this.authotIntroduce
			}, {
				headers: {
					'X-Requested-With': 'Add_Author', // 自定义标识
         		 },
				});
			if (response.data.success) {
				this.$message.success('添加成功'); // 使用 Element Plus 的消息提示
			} else {
				this.$message.error(response.data.message || '添加失败'); // 使用 Element Plus 的消息提示
			}
		} catch (error) {
			console.error('错误:', error);
			this.$message.error('添加失败，请重试'); // 通用错误处理
		}
	  }
	},
	mounted() {
    // this.showAllBooks();
    this.$nextTick(() => {
      store.commit('Utils/SET_INTRODUCE', false);
  });
  }
}
</script>

<style lang="less" scoped>
.my-autocomplete {
  li {
    line-height: normal;
    padding: 7px;

    .name {
      text-overflow: ellipsis;
      overflow: hidden;
    }
    .addr {
      font-size: 12px;
      color: #b4b4b4;
    }

    .highlighted .addr {
      color: #ddd;
    }
  }
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