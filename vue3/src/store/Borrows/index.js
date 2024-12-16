
import moment from 'moment';


const state = {
    // 管理员接收所有记录
  borrowsList:[],
    //读者只接收自己的借阅记录
  borrows:[]
}

// readerName:'',
// bookName:'',
// date:'',
// content:'',
// prise:0

const actions = {
}

const mutations = {
    INITBORROWSLIST(state,data){
        // 管理员保存借书记录的数组
        state.borrowsList = data.map(item => ({...item,
            reserveID: item.reserveID,
            bookID__title: item.bookID__title,
            userID__name: item.userID__name,
            startTime: moment.utc(item?.startTime).format('YYYY-MM-DD HH:mm:ss'),
            DDL: moment.utc(item?.DDL).format('YYYY-MM-DD HH:mm:ss'),
            endTime: moment.utc(item?.endTime).format('YYYY-MM-DD HH:mm:ss')}))
    },
    INITBORROWS(state,data){
        // 读者保存自己的记录
        state.borrows = data.map(item => ({...item,
            startTime: moment.utc(item?.startTime).format('YYYY-MM-DD HH:mm:ss'),
            DDL: moment.utc(item?.DDL).format('YYYY-MM-DD HH:mm:ss'),
            bookID__title: item.bookID__title,}))
    }
}

const getters = {

}

export default {
    namespaced: true,
    state,
    actions,
    mutations,
    getters
}
