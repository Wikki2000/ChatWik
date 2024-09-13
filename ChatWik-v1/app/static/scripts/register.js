import { ajaxRequest, togglePasswordVisibility, alertBox } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {

  const alertDivClass = 'auth__alert__msg';

  togglePasswordVisibility('password', 'pwd1Icon');
  togglePasswordVisibility('confirmPassword', 'pwd2Icon');

  document.querySelector('button').addEventListener('click', (event) => {
    const pwd1 = document.querySelector("#password").value;
    const pwd2 = document.querySelector("#confirmPassword").value;
    const passwordPattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}$/;

    if (pwd1 !== pwd2) {
      event.preventDefault();
      const msg = 'Passwords must match';
      alertBox(alertDivClass, msg);
    } else if (!passwordPattern.test(pwd1)) {
      event.preventDefault();
      const msg = 'Password must be at least 8 characters and contain an uppercase letter, a lowercase letter, a number, and a special character';
      alertBox(alertDivClass, msg);
    }
  });

  document.querySelector('#form').addEventListener('submit', (event) => {
    event.preventDefault();

    const token = document.querySelector('#token').value;
    const data = JSON.stringify({ token });

    const url = '/chatwik/account/verify';

    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status === "Success") {
          window.location.href = '/chatwik/account/verify-success';
        }
      },
      (error) => {
        alert("Something Went Wrong");
      }
    );
  });

  document.querySelector('#reg-form').addEventListener('submit', (event) => {
    event.preventDefault();

    document.querySelector('.loader').style.display = 'block';
    document.querySelector('.signup-btn').style.display = 'none';

    document.querySelector(`.${alertDivClass}`).style.display = 'none';

    const firstname = document.querySelector("#firstname").value;
    const lastname = document.querySelector("#lastname").value;
    const username = document.querySelector("#username").value;
    const password = document.querySelector("#password").value;
    const email = document.querySelector("#email").value;

    const data = JSON.stringify({
      first_name: firstname,
      last_name: lastname,
      username: username,
      password: password,
      email: email
    });

    const url = '/chatwik/account/signup';

    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status === "Success") {
          const msg = 'Registration Successful. Continue to Verify Email';
          alertBox(alertDivClass, msg, false);
          document.querySelector('.loader').style.display = 'none';
          
          setTimeout(() => {
            document.querySelector('.verification-modal').style.display = 'block';
            document.querySelector("p#append-email").textContent = email;
          }, 2000);
        }
      },
      (error) => {
        const msg = 'This user already exists';
        alertBox(alertDivClass, msg);
        document.querySelector('.loader').style.display = 'none';
        document.querySelector('.signup-btn').style.display = 'block';
      }
    );
  });
});