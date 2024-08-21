import { ajaxRequest } from './utils.js';

$(document).ready(function () {

  $("#form").submit(function (event) {
    event.preventDefault();

    const data = JSON.stringify({ token: $("#token").val() });
    const url = 'http://127.0.0.1:5000/ChatWik/v1/auth/verify-email';

    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status == "Success") {
          alert(response.message);
          window.location.href = 'http://127.0.0.1:5000/ChatWik/v1/auth/verify-success';
        } else {
          alert(response.message);
        }
      },
      (error) => {
        console.error("An error occurred:", xhr.responseText);
      }
    );
  });
});
