import Vue from 'vue';

export default {

    save(drug) {
        return Vue.http.post('drugs', drug)
            .then(response => Promise.resolve(response.data))
            .catch(error => Promise.reject(error.data));
    },

    saveCategory(category) {
        return Vue.http.post('categories', category)
            .then(response => Promise.resolve(response.data))
            .catch(error => Promise.reject(error.data));
    },

    getCategories() {
        return Vue.http.get('categories')
            .then(response => Promise.resolve(response.data))
            .catch(error => Promise.reject(error.data));
    },

    getById(id) {
        return Vue.http.get(`drugs/${id}`)
            .then(response => Promise.resolve(response.data))
            .catch(error => Promise.reject(error.data));
    },

    getAll() {
        return Vue.http.get('drugs')
            .then(response => Promise.resolve(response.data))
            .catch(error => Promise.reject(error.data));
    }

};