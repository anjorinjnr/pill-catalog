import Vue from 'vue';
import { sync } from 'vuex-router-sync';
import VueResource from 'vue-resource';
import App from './components/App';
import router from './router';
import store from './store/';
import $ from 'jquery';
import select from 'select2';

Vue.use(VueResource);
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
// Vue.directive('dropzone', {
//     inserted: function(el) {
//         console.log(el.id);
//         // new Dropzone(`form#${el.id}`,  {url:  '/file/post'});
//         //  $(el).dropzone({
//         //     url: '/file/post',
//         //     addRemoveLinks: true
//         // });
//     }
// });

Vue.directive('select2', {
    inserted: function(el) {
        var select2parent = $('.select2-parent')[0] ? $('.select2-parent') : $('body');

        $(el).select2({
            dropdownAutoWidth: true,
            width: '100%',
            dropdownParent: select2parent
        });

        $(el).on('change', (val) => {
            // console.log(val);
        });

        $(el).on('select2:select', function(e) {
            console.log(e.params.data.id);
            $(el).val(e.params.data.id).trigger('change');
            // Do something
        });
    }
});

const app = new Vue({
    router,
    store,
    ...App
})

export { app, router, store }