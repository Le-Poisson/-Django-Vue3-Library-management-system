import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';

import Books from './Books';
import User from './User';
import Borrows from './Borrows';
import Utils from './Utils'

const store = createStore({
    modules: {
        Books,
        User,
        Borrows,
        Utils,
    },
    plugins: [
        createPersistedState({
            storage: window.sessionStorage,
            paths: ["Books", "User", "Borrows", "Utils"]
        })
    ]
});

export default store;