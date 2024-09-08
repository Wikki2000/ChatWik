import { ajaxRequest, togglePasswordVisibility, alertBox } from './utils.js';

$(document).ready(function () {

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

  // Handle Confirmation of Email
  $('#form').submit(function (event) {
    event.preventDefault();

    const token = $('#token').val();
    const data = JSON.stringify({ token: token });

    const url = '/chatwik/account/verify';

    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status == "Success") {
          window.location.href = '/chatwik/account/verify-success';
        }
      },
      (error) => {
        alert("Something Went Wrong");
      }
    );
  });

  // Handle User Registration
  $('#reg-form').submit(function (event) {
    event.preventDefault();

    // Show loader and hide button each time form is submitted
    $('.loader').show();
    $('.signup-btn').hide();

    // Clear Previous Message
    $(`.${alertDivClass}`).hide();

    const firstname = $("#firstname").val();
    const lastname = $("#lastname").val();
    const username = $("#username").val();
    const password = $("#password").val();
    const email = $("#email").val();

    const data = JSON.stringify(
      {
        first_name: firstname,
        last_name: lastname,
        username: username,
        password: password,
        email: email
      });

    const url = '/chatwik/account/signup';

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
