<template>
  <div v-for="item of 500" :key="item" class="snowflake"></div>
    <div class="background">
      <h1 class="page-title">欢迎使用图书管理系统</h1>
      <el-card class="login-card" shadow="hover">
        <h2 class="form-title">
          {{ currentForm === 'login' ? '登录' : (currentForm === 'register' ? '注册' : '管理员登录') }}
        </h2>
        <el-form
          v-if="currentForm === 'login'"
          ref="loginFormRef"
          style="max-width: 400px"
          :model="loginForm"
          status-icon
          :rules="loginRules"
          label-width="auto"
        >
          <el-form-item label="账号" prop="username">
            <el-input v-model="loginForm.username" autocomplete="off" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="loginForm.password" type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitLogin" class="text">登录</el-button>
            <el-button @click="switchToRegister" class="text">去注册</el-button>
            <el-button @click="switchToAdminLogin" class="text">管理员登录</el-button>
          </el-form-item>
        </el-form>
  
        <el-form
          v-if="currentForm === 'register'"
          ref="registerFormRef"
          style="max-width: 400px"
          :model="registerForm"
          status-icon
          :rules="registerRules"
          label-width="auto"
        >
          <el-form-item label="账号" prop="username">
            <el-input v-model="registerForm.username" autocomplete="off" />
          </el-form-item>
          <el-form-item label="用户名" prop="fullName">
            <el-input v-model="registerForm.fullName" autocomplete="off" />
          </el-form-item>
          <el-form-item label="手机号" prop="phone">
            <el-input v-model="registerForm.phone" autocomplete="off" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="registerForm.password" type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitRegister" class="text">注册</el-button>
            <el-button @click="switchToLogin" class="text">去登录</el-button>
            <el-button @click="switchToAdminLogin" class="text">管理员登录</el-button>
          </el-form-item>
        </el-form>
  
        <el-form
          v-if="currentForm === 'adminLogin'"
          ref="adminLoginFormRef"
          style="max-width: 400px"
          :model="adminLoginForm"
          status-icon
          :rules="adminLoginRules"
          label-width="auto"
        >
          <el-form-item label="账号" prop="username">
            <el-input v-model="adminLoginForm.username" autocomplete="off" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="adminLoginForm.password" type="password" autocomplete="off" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitAdminLogin" class="text">登录</el-button>
            <el-button @click="switchToRegister" class="text">去注册</el-button>
            <el-button @click="switchToLogin" class="text">用户登录</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
  </template>
  
  <style lang="scss">
@import '@/assets/font/index.css';

.snowflake {
  --size: 5vw;
  width: var(--size);
  height: var(--size);
  background: url("@/assets/sakura.png") no-repeat;
  background-size: 100% 100%;
  position: fixed;
  top: -5vh;
  z-index: 1;
}

@keyframes snowfall {
  100% {
    transform: translate3d(var(--end), 100vh, 0);
  }
}

@for $i from 0 through 500 {
  .snowflake:nth-child(#{$i}) {
    //每个雪花的大小
    --size: #{random(10) * 0.1}vw;
    //雪花移动目标点 -70后是负数 这样雪花会向左下方飘落
    --end: #{random(20) - 70}vw;
    left: #{random(150)}vw;
    animation: snowfall #{5 + random(8)}s linear infinite;
    animation-delay: -#{random(10)}s;
  }
}

.background {
  background-image: url('@/assets/background/1.jpg'); /* 替换为你的图片路径 */
  background-size: cover; /* 使背景图片覆盖整个容器 */
  background-position: center; /* 使背景图片居中 */
  display: flex;
  flex-direction: column; /* 垂直排列 */
  align-items: center; /* 水平居中 */
  justify-content: center;
  min-height: 100vh; /* 垂直居中 */
  background-repeat: no-repeat; /* 不重复背景图片 */
  animation: zoom 10s infinite alternate; /* 应用动画 */
}
  
  .page-title {
    margin-bottom: 20px;
    font-size: 48px; /* 标题大小 */
    text-align: center; /* 标题居中 */
    background: linear-gradient(90deg, white, lightpink); /* 从白色到浅粉色的渐变 */
    background-clip: text; /* 标准属性 */
    -webkit-background-clip: text; /* 兼容 Chrome 和 Safari */
    -webkit-text-fill-color: transparent; /* 使文本填充为透明，以显示背景 */
    color: transparent; /* 确保兼容性 */
    font-family: 'DaoLiTi', serif;
  }

  .form-title {
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
  
  .login-card {
  padding: 20px;
  width: 100%;
  max-width: 400px; /* 限制卡片宽度 */
  border-radius: 15px; /* 添加圆角 */
  background: rgba(255, 255, 255, 0.7); /* 半透明背景 */
  backdrop-filter: blur(10px); /* 毛玻璃效果 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2); /* 增加阴影效果 */
  }

  .text{
    font-size: 24px;
    font-family: 'DaoLiTi', serif;
  }
  </style>
  
  <script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useStore } from 'vuex';
import { mapGetters } from 'vuex';

const store = useStore(); // 使用 Vuex

const router = useRouter(); // 使用 Vue Router
  const currentForm = ref('login') // 当前表单状态
  const message = ref(''); // 用于显示消息
  
  const loginForm = reactive({
    username: '',
    password: '',
  })
  
  const registerForm = reactive({
    username: '',
    fullName: '',
    phone: '',
    password: '',
  })
  
  const adminLoginForm = reactive({
    username: '',
    password: '',
  })
  
  // 表单验证规则
  const loginRules = {
    username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  }
  
  const registerRules = {
    username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    fullName: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
    phone: [{ required: true, message: '请输入手机号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  }
  
  const adminLoginRules = {
    username: [{ required: true, message: '请输入账号', trigger: 'blur' }],
    password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  }
  
  // 切换表单函数
  const switchToLogin = () => {
    currentForm.value = 'login';
  }
  
  const switchToRegister = () => {
    currentForm.value = 'register';
  }
  
  const switchToAdminLogin = () => {
    currentForm.value = 'adminLogin';
  }
  
  const submitLogin = async () => {
  console.log('登录:', loginForm);
  message.value = ''; // 清空消息

  try {
    const response = await axios.post('http://127.0.0.1:8000/library/post/', loginForm, {
      headers: {
        'X-Requested-With': 'Login', // 自定义标识
      },
    });

    if (response.data.success) {
      message.value = '登录成功';
      setTimeout(() => {
        const userData = {
          readerId: response.data.user.userID,
          readerName: response.data.user.name,
          readerPhone: response.data.user.phoneNum,
          readerAccount: response.data.user.account,
          borrowTimes: response.data.user.borrowTimes,
          ovdTimes: response.data.user.ovdTimes,
          isAdmin: false, // 假设新用户不是管理员
        };

        store.commit('User/SET_READER_INFO', userData); // 提交读者信息
        
        // 打印用户信息
        const storedUserInfo = store.getters['User/readerInfo'];
        console.log('用户信息:', storedUserInfo); // 打印从 store 中获取的信息

        router.push('/home'); // 跳转到主界面
      }, 1000);
    } else {
      message.value = response.data.message || '登录失败';
      console.log(message.value);
      ElMessage({
        message: message.value,
        type: 'error',
      });
    }
  } catch (error) {
    message.value = '登录失败，请重试'; // 通用错误处理
    console.error('登录错误:', error);
    ElMessage({
      message: message.value,
      type: 'error',
    });
  }
}
  
  const submitRegister = async () => {
    console.log('注册:', registerForm);
    message.value = ''; // 清空消息
  try {
    const response = await axios.post('http://127.0.0.1:8000/library/post/', registerForm, {
      headers: {
        'X-Requested-With': 'Registration', // 自定义标识
      },
    });
    if (response.data.success) {
      message.value = '注册成功';
      setTimeout(() => {
        const userData = {
          readerId: response.data.user.userID,
          readerName: response.data.user.name,
          readerPhone: registerForm.phone,
          readerAccount: response.data.user.account,
          borrowTimes: response.data.user.borrowTimes,
          ovdTimes: response.data.user.ovdTimes,
          isAdmin: false, // 假设新用户不是管理员
        };

        store.commit('User/SET_READER_INFO', userData); // 提交读者信息
        
        // 打印用户信息
        const storedUserInfo = store.getters['User/readerInfo'];

        console.log('用户信息:', storedUserInfo); // 打印从 store 中获取的信息

        router.push('/home'); // 跳转到主界面
      }, 1000);
    } else {
      message.value = response.data.message || '注册失败';
      console.log(message.value);
      ElMessage({
        message: message.value,
        type: 'error',
      });
    }
  } catch (error) {
    message.value = '注册失败，请重试'; // 通用错误处理
  }
  }
  
  const submitAdminLogin = async () => {
    console.log('管理员登录:', adminLoginForm);
    message.value = ''; // 清空消息

  try {
    const response = await axios.post('http://127.0.0.1:8000/library/post/', adminLoginForm, {
      headers: {
        'X-Requested-With': 'Admin_Login', // 自定义标识
      },
    });

    if (response.data.success) {
      message.value = '登录成功';
      setTimeout(() => {
        const adminData = {
          adminID: response.data.admin.adminID,
          adminName: response.data.admin.name,
          adminAccount: response.data.admin.account,
          isAdmin: true,
        };

        store.commit('User/SET_ADMIN_INFO', adminData); // 提交读者信息
        
        // 打印用户信息
        const storedAdminInfo = store.getters['User/adminInfo'];
        console.log('管理员信息:', storedAdminInfo); // 打印从 store 中获取的信息

        router.push('/home'); // 跳转到主界面
      }, 1000);
    } else {
      message.value = response.data.message || '登录失败';
      console.log(message.value);
      ElMessage({
        message: message.value,
        type: 'error',
      });
    }
  } catch (error) {
    message.value = '登录失败，请重试'; // 通用错误处理
    console.error('登录错误:', error);
    ElMessage({
      message: message.value,
      type: 'error',
    });
  }
  }
  </script>