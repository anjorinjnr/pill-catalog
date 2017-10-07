import  $ from 'jquery';
import notify from 'bootstrap-notify';


const TYPE_DEFAULT = 'inverse';
const TYPE_DANGER = 'danger';
const DELAY = 3000;
const DEFAULT_ERROR_MSG = 'Something went wrong, please try again.';

const alert = function (message, type) {
  $.notify({message},
    {
      element: 'body',
      type: type,
      delay: DELAY,
      offset: {
        x: 20,
        y: 20
      },
      spacing: 10,
      z_index: 1031,
      template: '<div data-notify="container" class="alert alert-dismissible alert-{0} alert--notify" role="alert">' +
      '<span data-notify="icon"></span> ' +
      '<span data-notify="title">{1}</span> ' +
      '<span data-notify="message">{2}</span>' +
      '<div class="progress" data-notify="progressbar">' +
      '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
      '</div>' +
      '<a href="{3}" target="{4}" data-notify="url"></a>' +
      '<button type="button" aria-hidden="true" data-notify="dismiss" class="alert--notify__close">Close</button>' +
      '</div>'
    });
};
export default {
  notify(message) {
    alert(message, TYPE_DEFAULT);
  },

  error(message=DEFAULT_ERROR_MSG) {
    console.error(message);
    alert(message, TYPE_DANGER);
  }

}
