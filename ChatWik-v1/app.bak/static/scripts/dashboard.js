import { get } from './global/utils.js';

$(document).ready(async function() {

  const apiBaseUrl = '/api/v1';

  const allUsers = await get(apiBaseUrl + '/users');

  console.log('All Users:', allUsers);

  // Handle clicks on the navigation group
  $('.nav-group').click(function() {
    const clickId = $(this).attr('id');

    switch (clickId) {
      case 'all-chat': {
        alert(clickId);
        break;
      }
      case 'private-chat': {
        alert(clickId);
        break;
      }
      case 'group-chat': {
        alert(clickId);
        break;
      }
      default: {
        alert('Unknown option clicked');
      }
    }
  });
});

