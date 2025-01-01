import { ajaxRequest, getBaseUrl, get } from '../global/utils.js';


$(document).ready(function() {

  // Select and highligt home icon once user logins
  $("#dashboard__main-home").addClass('header__menu-highlihgt');
  $("#dashboard__main-home").siblings().addClass('header__menu-highlihgt');

  $('header div .fa').click(function() {
    const $clickIcon = $(this);
    const clickId = $clickIcon.attr('id');

    // Remove the highlight class from header menu and navbar menu.
    // Empty the dashboard section in readiness to load another one.
    $('header div .fa').removeClass('header__menu-highlihgt');
    $('header div .fa').siblings().removeClass('header__menu-highlihgt');
    $('.dashboard__nav-item').removeClass('dashboard__highlight-item');
    $('#dashboard__main-dynamic').empty();


    // Add highlight class to click header menu icon and,
    // it siblings (The text describing each icon).
    $clickIcon.addClass('header__menu-highlihgt');
    $clickIcon.siblings().addClass('header__menu-highlihgt');

    switch (clickId) {
      case 'dashboard_main-chat': {
        $('#dashboard__main-dynamic').load('/chatwik/pages/chat-dashboard');
        break;
      }
      case 'dashboard__main-freind': {
        $('#dashboard__main-dynamic').load('/chatwik/pages/friends-dashboard');
        break;
      }
    }
  });
})
