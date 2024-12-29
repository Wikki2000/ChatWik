import { ajaxRequest, togglePasswordVisibility, alertBox } from '../global/utils.js';

$(document).ready(function () {

  const API_BASE_URL = '/api/v1';
  const APP_BASE_URL = '/chatwik';
  const alertDivClass = 'auth__alert__msg';

  // Toggle password visibility when click on the eye icon
  togglePasswordVisibility('password', 'pwd1Icon');
  togglePasswordVisibility('confirmPassword', 'pwd2Icon');

  // Ensure password match and meet some criteria.
  $('button').click(function () {

    const pwd1 = $("#password").val();
    const pwd2 = $("#confirmPassword").val();
    const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$/;

    if (pwd1 !== pwd2) {
      event.preventDefault();
      const msg = 'Password must match';
      alertBox(alertDivClass, msg);

    } else if (!passwordPattern.test(pwd1)) {
      event.preventDefault();
      const msg = 'Password must be atleast 8 characters and ' +
                  'contains uper, lowercase and special character';
      alertBox(alertDivClass, msg);
    }
  });

  // Handle User Registration
  $('#reg-form').submit(function (event) {
    event.preventDefault();

    // Show loader and hide button each time form is submitted
    $('.loader').show();
    $('.signup-btn').hide();

    // Clear Previous Message
    $(`.${alertDivClass}`).hide();

    const first_name = $('#firstname').val();
    const last_name = $('#lastname').val();
    const username = $('#username').val();
    const password = $('#password').val();
    const email = $('#email').val();
    const country = $('#country').val();
    const state = $('#state').val();

    const data = JSON.stringify(
      {
        first_name, last_name, country,
        username, password, email, state
      });

    const url = API_BASE_URL + '/account/register';

    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status == "Success") {
          const msg = 'Registration Successfull. Continue to Verify Email';
          alertBox(alertDivClass, msg, false);
          $('.loader').hide();
          setTimeout(() => {
            $('.verification-modal').show();
	    $("P#append-email").append(email);
          }, 2000);
          window.location.href = APP_BASE_URL + '/account/verify'; 
         }
      },
      (error) => {
        const msg = 'This user already exist';
        alertBox(alertDivClass, msg);

        // Hide loader and display button to user on error
        $('.loader').hide();
        $('.signup-btn').show()
      }
    );
  });
});
