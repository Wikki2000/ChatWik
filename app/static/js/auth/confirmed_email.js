import { getBaseUrl } from '../global/utils.js';

$(document).ready(function() {
  const APP_BASE_URL =  getBaseUrl()['appBaseUrl'];
  $('#goto-dashboard').click(function() {
    window.location.href = APP_BASE_URL + '/dashboard';
  });
});
