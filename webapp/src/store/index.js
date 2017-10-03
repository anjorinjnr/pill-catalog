import Vue from 'vue';
import Vuex from 'vuex';
import drugs from './modules/drugs'

Vue.use(Vuex);


const store = new Vuex.Store({
  modules: {
    drugs
  }
});

export default store;