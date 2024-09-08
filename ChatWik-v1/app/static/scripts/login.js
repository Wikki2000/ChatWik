import { togglePasswordVisibility, ajaxRequest, alertBox } from './utils.js'; 

$(document).ready(function () {
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
    const url = '/chatwik/account/signin';
    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status == "Success") {
          const display_name = response.user.username ? response.user.username : response.user.name;
          
          const msg = 'Login Successfully';
          alertBox(alertDivClass, msg, false);

          setTimeout(() => {
            window.location.href = '/chatwik/dashboard?display_name=' + encodeURIComponent(display_name);
          }, 2000);
        }
      },
      (error) => {
        const msg = 'Invalid Email or Password';
        alertBox(alertDivClass, msg);

        // Hide loader and display button to user on error
        $('.loader').hide();
        $('#signin-btn').show()
      }
    );
  })
});
