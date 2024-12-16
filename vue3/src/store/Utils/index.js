const state = {
    isIntroduce: false,
}

const actions = {}

const mutations = {
    SET_INTRODUCE(state, value) {
        state.isIntroduce = value
    }
}

const getters = {}

export default {
    namespaced: true, 
    state, 
    actions, 
    mutations, 
    getters
}