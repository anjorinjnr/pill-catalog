import Vue from 'vue';
import Vuex from 'vuex';
import { saveDrug } from './actions/drug';
import { ADD_DRUG } from './mutation_types';
Vue.use(Vuex);

//  mutations


const state = {
    drugs: []
}

const mutations = {

    [ADD_DRUG](state, payload) {
        state.drugs = [...state.drugs, payload];
        console.log(state.drugs);
    },

}

const actions = {
    saveDrug
}


const store = new Vuex.Store({
    state,
    mutations,
    actions
})

export default store