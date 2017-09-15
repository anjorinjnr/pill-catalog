import Vue from 'vue';
import Router from 'vue-router';
import Home from '../components/Home';
import CatalogDrugs from '../components/Catalog__Drugs';
import NewDrug from '../components/Catalog__Drugs__New';

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
            component: NewDrug
        }
    ]
});
``