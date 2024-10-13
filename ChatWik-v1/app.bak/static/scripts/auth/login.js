import { togglePasswordVisibility, ajaxRequest, alertBox } from '../global/utils.js'; 

$(document).ready(function () {

  const API_BASE_URL = '/api/v1';

  togglePasswordVisibility('password', 'passwordIconId');
  $('#login-form').submit(function (event) {
    event.preventDefault();
    const alertDivClass = 'auth__alert__msg';
    $(`.${alertDivClass}`).hide();
    $('.loader').show();
    $('#signin-btn').hide();

    const data = JSON.stringify(
      {
        email: $('#email').val(),
        password: $('#password').val()
      }
    );
    const url = API_BASE_URL + '/account/login';
    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status == "Success") {
          
          const msg = 'Login Successfully';
          alertBox(alertDivClass, msg, false);

          setTimeout(() => {
            window.location.href = '/chatwik/dashboard';
          }, 2000);
        }
      },
      (error) => {
        const msg = 'Invalid Email or Password';
        alertBox(alertDivClass, msg);

        // Hide loader and display button to user on error
        $('.loader').hide();
        $('#signin-btn').show();
      }
    );
  })
});
