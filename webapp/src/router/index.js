import Vue from 'vue';
import Router from 'vue-router';
import Home from '../components/Home';
import CatalogDrugs from '../components/Catalog__Drugs';
import CatalogDrugForm from '../components/Catalog__Drugs__Form';

Vue.use(Router);

export default new Router({
  mode: 'hash',
  routes: [{
    path: '/',
    component: Home
  },
    {
      path: '/catalog/drugs',
      component: CatalogDrugs
    },
    {
      path: '/catalog/drugs/new',
      component: CatalogDrugForm
    },

    {
      path: '/catalog/drugs/:id',
      component: CatalogDrugForm,
      props: route => {
        return {
          id: parseInt(route.params.id),
          mode: 'edit'
        }
      }
    }
  ]
});
