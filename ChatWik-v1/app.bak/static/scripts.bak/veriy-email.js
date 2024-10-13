import { ajaxRequest } from './utils.js';

$(document).ready(function () {

  $("#form").submit(function (event) {
    event.preventDefault();
	  alert("I exectuyg");

    const data = JSON.stringify({ token: $("#token").val() });
    const url = '/chatwik/account/verify';

    ajaxRequest(url, "POST", data,
      (response) => {
        if (response.status == "Success") {
          alert(response.message);
          window.location.href = '/chatwik/account/verify-success';
        } else {
          alert(response.message);
        }
      },
      (error) => {
        console.error("An error occurred");
      }
    );
  });
});
