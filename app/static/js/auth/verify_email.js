import { ajaxRequest, alertBox, getBaseUrl } from '../global/utils.js';

$(document).ready(function () {

  const API_BASE_URL = getBaseUrl()['apiBaseUrl'];
  const APP_BASE_URL = getBaseUrl()['appBaseUrl'];

  // Go back to previous page
  $('#back').click(function() {
    window.history.back();
  });

  // Listen for input event on each code-input field
  $('input[type="text"]').on('input', function() {
    // Check any value is entered and not the end of input field.
    if ($(this).val !== '' && $(this).next().length) {
      $(this).next().focus();
    }
  });

  // Listen for backspace to navigate to the previous input
  $('input[type="text"]').on('keydown', function(e) {
    let $current = $(this);
    if (e.key === 'Backspace' && $current.val() === '' && $current.prev().length) {
      $current.prev().focus();
    }
  });

  $('#verify-form').submit(function (event) {
    event.preventDefault();

    // Show animation and hide butthon
    // while waiting for server response
    $('.loader').show();
    $('.auth-card__button').hide();

    const token = (
      $('#f1').val() + $('#f2').val() + $('#f3').val() +
      $('#f4').val() + $('#f5').val() + $('#f6').val()
    )

    const data = JSON.stringify({ token: token});
    const url = API_BASE_URL  + '/account/verify';

    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status == "Success") {
	  //window.location.href = '/account/verify-success';
	  window.location.href =  APP_BASE_URL + '/pages/email-confirmed';
         }
      },
      (error) => {
	const alertDivClass = 'auth-alert';
        const msg = 'Invalid or Expired Token';
        alertBox(alertDivClass, msg);
        $('.loader').hide();
        $('.auth-card__button').show();
      }
    );
  });
});
