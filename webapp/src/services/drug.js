import  Vue from 'vue';

export default  {

  save(drug)  {
    return Vue.http.post('drug', drug)
      .then(response => Promise.resolve(response.data))
      .catch(error => Promise.reject(error));
  }

};