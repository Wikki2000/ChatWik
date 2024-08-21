import { togglePasswordVisibility } from './utils.js'; 

$(document).ready(function () {
  apiStatus();
  togglePasswordVisibility('password', 'passwordIconId');
});

/**
 * Check the status of API.
 */
function apiStatus () {
  const url = 'http://127.0.0.1:5001/api/v1/status';
  $.get(url, (response) =>{
    if (response.status === 'OK') {
      $('DIV#api-status').addClass('available');
    } else {
      $('DIV#api-status').removeClass('available');
    }
  });
}
