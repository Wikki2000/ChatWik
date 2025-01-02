import { ajaxRequest, getBaseUrl } from '../global/utils.js';
/**
 * This JavaScript file handles the main interactions on the dashboard.
 * When the user clicks an item in the sidebar, the corresponding section
 * of the dashboard is loaded.
 */
$(document).ready(function () {

  const API_BASE_URL = getBaseUrl()['apiBaseUrl'];
  const APP_BASE_URL = getBaseUrl()['appBaseUrl'];

  $('.dashboard__nav-item').click(function () {
    // Track exact navbar click by retrieving it ID
    const $clickNavBar = $(this);
    const clickNavBarId = $clickNavBar.attr('id');
    //alert(clickNavBarId);


    // Remove highlight from previously selected navabar and header menu,
    // Empty the content of dashboard section to load another.
    $('.dashboard__nav-item').removeClass('dashboard__highlight-item');
    $('header div .fa').removeClass('header__menu-highlihgt');
    $clickNavBar.addClass('dashboard__highlight-item');
    $('#dashboard__main-dynamic').empty();

    /* ================ Sidebar Navigation =============== */
    switch (clickNavBarId) {
      case 'main__nav-item': {
        alert(clickNavBarId);
        break;
      }
      case 'chat__nav-item': {
        alert(clickNavBarId);
        break;
      }
      case 'freinds__nav-item': {
        alert(clickNavBarId);
        break;
      }
      case 'rooms__nav-item': {
        alert(clickNavBarId);
        break;
      }
      case 'setting__nav-item': {
        alert(clickNavBarId);
        break;
      }
      case 'logout': {
        const url = API_BASE_URL + '/account/logout';
        ajaxRequest(url, 'POST', null,
          (response) => {
            if (response.status === 'Success') {
	      localStorage.clear();
              window.location.href = APP_BASE_URL + '/account/login'; 
            }
          },
          (error) => {
          }
        );
        break;
      }

    }
  });
});
