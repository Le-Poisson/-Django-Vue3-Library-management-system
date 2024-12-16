const state = {
   booksList:[],
}

const actions = {
}

const mutations = {

    INITBOOKSLIST(state, data){
        data = data || []
        state.booksList = data
    }


}

const getters = {

}

export default {
    namespaced: true, // 确保启用命名空间
    state,
    actions,
    mutations,
    getters
}
