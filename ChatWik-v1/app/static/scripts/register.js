import { ajaxRequest } from './utils.js';
import { togglePasswordVisibility } from './utils.js';

$(document).ready(function () {

  // Toggle password visibility when click on the eye icon
  togglePasswordVisibility('password', 'pwd1Icon');
  togglePasswordVisibility('confirmPassword', 'pwd2Icon');

  // Ensure password match and meet some criteria.
  $('button').click(function (event) {

    const pwd1 = $("#password").val();
    const pwd2 = $("#confirmPassword").val();
    const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$/;

    if (pwd1 !== pwd2) {
      event.preventDefault();
      const error = '<strong>Error!</strong> Password must match';
      // Show the error div and append msg.
      $("#errorDiv").show();
      $("#errorMsg").html(error);
    } else if (!passwordPattern.test(pwd1)) {
      event.preventDefault();
       const error = '<strong>Error!</strong> Password must be at least 8 characters long, ' +
       	             'and include at least one digit, one lowercase letter, one uppercase letter, ' +
                     'and one special character.';

      $("#errorDiv").show();
      $("#errorMsg").html(error);
    }
  });
});
