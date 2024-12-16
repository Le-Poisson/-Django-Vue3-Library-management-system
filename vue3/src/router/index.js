import { createRouter, createWebHashHistory } from 'vue-router'
import login from '../login/login.vue'

import Home from '@/Home'
import Introduce from '@/Home/Introduce'
import SearchBooks from '@/Home/SearchBooks'
import AdminBorrows from '@/Home/AdminBorrows'
import AdminPerson from '@/Home/AdminPerson'
import AdminAddBooks from '@/Home/AdminAddBooks'
import AdminAddQuotations from '@/Home/AdminAddQuotations'

import ReaderBorrows from '@/Home/ReaderBorrows'

const routes = [
  {
    path: '/',
    name: 'login',
    component: login
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/login',
    name: 'l',
    component: login
  },
  {
    path: '/home',
    component: Home,
    children: [
        {
            path: '',
            redirect: 'home/introduce' // 添加重定向
        },
        {
            path: '/',
            component: Introduce,
        },
        {
            //    主页介绍
            path: 'introduce',
            component: Introduce,
        },
        {
            //    书籍查询
            path: 'search',
            component: SearchBooks,
        },
    // 管理员
        {
            //    人员管理
            path: 'person',
            component: AdminPerson,
        },
        {
            //    管理员管理借阅记录
            path: 'adminborrows',
            component: AdminBorrows,
        },
 {
            //    管理员添加图书
            path: 'adminaddbooks',
            component: AdminAddBooks,
        }, 
        {
            path: 'adminaddquotations',
            component: AdminAddQuotations,
        }, 
        {
            path: 'adminmessage',
            component: () => import('@/Home/AdminMessage')
        },
    // 读者
        {
            //    读者借阅记录
            path: 'readerborrows',
            component: ReaderBorrows,
        },
        {
            path: 'readermessage',
            component: () => import('@/Home/ReaderMessage')
        },
    ]
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
