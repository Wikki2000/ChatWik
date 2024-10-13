import { togglePasswordVisibility, ajaxRequest, alertBox } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
  togglePasswordVisibility('password', 'passwordIconId');

  const loginForm = document.getElementById('login-form');
  const loader = document.querySelector('.loader');
  const signinBtn = document.getElementById('signin-btn');
  const alertDivClass = 'auth__alert__msg';

  loginForm.addEventListener('submit', (event) => {
    event.preventDefault();

    document.querySelector(`.${alertDivClass}`).style.display = 'none';
    loader.style.display = 'block';
    signinBtn.style.display = 'none';

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const data = JSON.stringify({
      email: email,
      password: password,
    });

    const url = '/account/signin';

    ajaxRequest(url, 'POST', data,
      (response) => {
        if (response.status === "Success") {
          const displayName = response.user.username || response.user.name;

          const msg = 'Login Successfully';
          alertBox(alertDivClass, msg, false);

          setTimeout(() => {
            window.location.href = '/dashboard';
          }, 1000);
        }
      },
      (error) => {
        const msg = 'Invalid Email or Password';
        alertBox(alertDivClass, msg);

        loader.style.display = 'none';
        signinBtn.style.display = 'block';
      });
  });
});
