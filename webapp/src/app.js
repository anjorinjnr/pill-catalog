import Vue from 'vue';
import { sync } from 'vuex-router-sync';
import VueResource from 'vue-resource';
import App from './components/App';
import router from './router';
import store from './store/';
import $ from 'jquery';
//import select from 'select2';
import VeeValidate from 'vee-validate';

Vue.use(VueResource);
Vue.use(VeeValidate);

const APP_VERSION = '0.0.3';

console.info('Running Version: ' + APP_VERSION);

//Vue.http.options.root = 'https://catalog-service-dot-pharmaplusng.appspot.com/v1/api';

Vue.http.options.root = '/v1/api';

sync(store, router);




Vue.directive('toggle-menu', {
    inserted: function(el) {
        $(el).find('a:first-child').click(e => {
            e.preventDefault();
            let parent = $(e.currentTarget).parent();
            parent.toggleClass(
                'navigation__sub--toggled navigation__sub--active');

            //$(e.currentTarget).next('ul').slideToggle(250);
        });
    }
});

const app = new Vue({
    router,
    store,
    ...App
});

export { app, router, store }