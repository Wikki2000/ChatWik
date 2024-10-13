import { ajaxRequest, alertBox } from '../global/utils.js';

$(document).ready(function () {
  const API_BASE_URL = '/api/v1';

  $("#verify-form").submit(function (event) {
    event.preventDefault();

    const alertDivClass = 'auth__alert__msg';
    $(`.${alertDivClass}`).hide();
    $('.loader').show();
    $('#signin-btn').hide();

    const data = JSON.stringify({ token: $("#token").val() });
    const url = API_BASE_URL + '/account/verify';

    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status === "Success") {
          alertBox(alertDivClass, response.msg, false);
          setTimeout(() => {
            window.location.href = '/chatwik/account/login';
          }, 2000);
        }
      },
      (error) => {
	const msg = 'Invalid or Expired Token';
        alertBox(alertDivClass, msg);

        $('.loader').hide();
        $('#signin-btn').show();
        console.error(`An error occurred: ${JSON.stringify(error.responseJSON)}`);
      }
    );
  });
});
