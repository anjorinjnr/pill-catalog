import drugService from '../../services/drug';
import * as types from '../mutation_types';

//initial state
const state = {
  all: [],
  categories: []
};

// getters
const getters = {
  drugs: state => state.all,

  drugById: (state) => (id) => {
    return state.all.find(drug => drug.id === id);
  }
};


// actions
const actions = {

  /**
   * Get Drugs from server.
   * @param commit
   * @returns {Promise}
   */
  getDrugs({commit}) {
    return new Promise((resolve, reject) => {
      drugService.getAll()
        .then(drugs => {
          commit(types.RECEIVE_DRUGS, drugs);
          resolve(drugs);
        })
        .catch(error => reject(error));
    });

  },

  /**
   * Get Drug Categories from sever.
   * @param commit
   * @returns {Promise}
   */
  getCategories({commit}) {
    return new Promise((resolve, reject) => {
      drugService.getCategories()
        .then(categories => {
          commit(types.RECEIVE_CATEGORIES, {categories});
          resolve(categories);
        })
        .catch(error => reject(error));

    });

  },


  /**
   * Create or update Drug Category.
   * @param commit
   * @param state
   * @param payload
   * @returns {Promise}
   */
  saveCategory({commit, state}, payload) {
    return new Promise((resolve, reject) => {
      drugService.saveCategory(payload)
        .then(category => {
          commit(types.RECEIVE_CATEGORY, category);
          resolve(category);
        })
        .catch(error => reject(error));
    });
  },

  /**
   * Create or update drug.
   * @param commit
   * @param drug
   * @returns {Promise}
   */
  saveDrug({commit}, drug) {
    return new Promise((resolve, reject) => {
      drugService.save(drug)
        .then(data => {
          commit(types.RECEIVE_DRUG, data);
          resolve(data);
        })
        .catch(error => reject(error));
    });

  },

  /**
   * Get a drug by the id. First check local store, then query server.
   * @param commit
   * @param id
   * @returns {Promise}
   */
  getDrugById({commit}, id) {
    return new Promise((resolve, reject) => {
      let i = state.all.findIndex(d => d.id === id);
      if (i < 0) {
        drugService.getById(id)
          .then(drug => {
            commit(types.RECEIVE_DRUG, {drug});
            resolve(drug);
          })
          .catch(error => reject(error));
      } else {
        resolve(state.all[i]);
      }
    });
  }

};


// mutations
const mutations = {

  [types.RECEIVE_DRUGS](state, drugs) {
    state.all = drugs;
  },

  [types.RECEIVE_CATEGORIES](state, {categories}) {
    state.categories = categories;
  },

  [types.RECEIVE_CATEGORY](state, category) {
    state.categories = [...state.categories, category];
  },

  [types.RECEIVE_DRUG](state, drug) {
    state.all = [...state.all, drug];
  },

  [types.UPDATE_DRUG](state, payload) {
    state.all = state.all.map(drug => {
      if (drug.id === payload.id) {
        return {...drug, ...payload}
      } else {
        return drug;
      }
    });
  }
};

export default {
  state,
  getters,
  actions,
  mutations
};