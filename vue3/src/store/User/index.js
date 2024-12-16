const state = {
   adminInfo:{
    adminID:'',
    adminName:'',
    adminAccount:'',
   },
   readerInfo:{
    readerId:'',
    readerName:'',
    readerPhone:'',
    readerAccount:'',
    borrowTimes:0,
    ovdTimes:0
   },
   readerList:[],
   isAdmin:false
}

const actions = {
    setAdminInfo({commit},data){
        commit('SET_ADMIN', data.isAdmin);
        commit('SET_ADMIN_INFO', data);
    },
    setReaderInfo({commit},data){
        commit('SET_ADMIN', data.isAdmin);
        commit('SET_READER_INFO', data);
    },
    initReaderList({commit}){
        commit('INIT_READER_LIST', data);
    }
}

const mutations = {
    SET_ADMIN(state, isAdmin) {
        state.isAdmin = isAdmin;
    },
    SET_ADMIN_INFO(state,data){
        // 保存管理员用户名
        let {adminID,adminName,adminAccount} = data
        state.adminInfo = {adminID,adminName,adminAccount}
        state.isAdmin = data.isAdmin
    },
    SET_READER_INFO(state,data){
        // 保存读者用户名
    let {readerId,readerName,readerPhone,readerAccount,borrowTimes,ovdTimes} = data
      state.readerInfo = {readerId,readerName,readerPhone,readerAccount,borrowTimes,ovdTimes}
      state.isAdmin = data.isAdmin
    },
    INIT_READER_LIST(state,data){
        state.readerList = data
    }
}

const getters = {
    isAdmin: (state) => state.isAdmin,
    adminInfo: (state) => state.adminInfo,
    readerInfo: (state) => state.readerInfo
}

export default {
    namespaced: true, // 确保启用命名空间
    state,
    actions,
    mutations,
    getters
}